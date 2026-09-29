#!/usr/bin/env python3
"""Deterministic local gates for the AI SDLC Loop skill."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import re
import shlex
import stat
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SKILLS_ROOT = Path(__file__).resolve().parents[2]
SHARED_SCRIPTS = (
    _SKILLS_ROOT / "ai-sdlc-shared-runtime" / "scripts"
    if (_SKILLS_ROOT / "ai-sdlc-shared-runtime" / "scripts").is_dir()
    else _SKILLS_ROOT / "ai-sdlc-loop-shared-runtime" / "scripts"
)
if SHARED_SCRIPTS.is_dir() and str(SHARED_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SHARED_SCRIPTS))
_CURRENT_DIR = Path(__file__).resolve().parent
if str(_CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(_CURRENT_DIR))

try:
    from toon import ToonDecodeError, decode_toon, encode_toon
except ImportError:
    from ai_sdlc_toon import ToonDecodeError, decode_toon, encode_toon

import ai_sdlc_adaptive as adaptive

SCHEMA = "ai-sdlc-loop/v1"
PROMOTION_SCHEMA = "ai-sdlc-harness-promotion/v1"

_QG_CANDIDATES = (
    _SKILLS_ROOT / "ai-sdlc-engineering-quality-gate" / "scripts" / "engineering_quality_gate.py",
    _SKILLS_ROOT / "ai-sdlc-loop-engineering-quality-gate" / "scripts" / "engineering_quality_gate.py",
)
QUALITY_GATE_SCRIPT = next((p for p in _QG_CANDIDATES if p.is_file()), _QG_CANDIDATES[0])
FEATURE_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
SECRET_RE = re.compile(
    r"(?i)(authorization\s*[:=]\s*bearer\s+|token\s*[:=]\s*|password\s*[:=]\s*|secret\s*[:=]\s*)([^\s\"']+)"
)
PRIVATE_KEY_RE = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S)


class LoopError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return encode_toon(value).encode("utf-8")


def fingerprint(value: dict[str, Any], omit: str = "fingerprint") -> str:
    payload = {key: item for key, item in value.items() if key != omit}
    return "sha256:" + hashlib.sha256(canonical(payload)).hexdigest()


def atomic_toon(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(canonical(value))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def load_toon(path: Path) -> dict[str, Any]:
    try:
        value = decode_toon(path.read_text(encoding="utf-8"))
    except (OSError, ToonDecodeError, ValueError, TypeError) as exc:
        raise LoopError(f"cannot read valid TOON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise LoopError(f"expected a TOON mapping in {path}")
    return value


def normalize_request(value: str) -> str:
    normalized = " ".join(value.split())
    if not normalized:
        raise LoopError("request must not be empty")
    return normalized


def validate_feature(value: str) -> str:
    if not FEATURE_RE.fullmatch(value):
        raise LoopError("feature must match [a-z0-9][a-z0-9-]{0,62}")
    return value


def project_root(value: str) -> Path:
    root = Path(value).resolve()
    if not root.is_dir():
        raise LoopError(f"project root is not a directory: {root}")
    return root


def state_dir(root: Path, feature: str) -> Path:
    directory = root
    for part in (".ai-sdlc-loop", validate_feature(feature)):
        directory = directory / part
        if directory.is_symlink():
            raise LoopError(f"Loop state path contains a symlink: {directory}")
        resolved = directory.resolve(strict=False)
        if root not in resolved.parents:
            raise LoopError(f"Loop state path escapes project root: {directory}")
    return directory


def state_path(root: Path, feature: str, *parts: str) -> Path:
    path = state_dir(root, feature)
    for part in parts:
        if not part or part in {".", ".."} or "/" in part or "\\" in part:
            raise LoopError(f"invalid Loop state component: {part}")
        path = path / part
        if path.is_symlink():
            raise LoopError(f"Loop state path contains a symlink: {path}")
        resolved = path.resolve(strict=False)
        if root not in resolved.parents:
            raise LoopError(f"Loop state path escapes project root: {path}")
    return path


def safe_relative(root: Path, value: str, *, allow_state: bool = False) -> str:
    candidate = Path(value)
    if candidate.is_absolute() or not candidate.parts or ".." in candidate.parts or "\x00" in value:
        raise LoopError(f"unsafe relative path: {value}")
    normalized = candidate.as_posix()
    if not normalized or normalized == ".git" or normalized.startswith(".git/"):
        raise LoopError(f"path overlaps Git metadata: {value}")
    if not allow_state and (normalized == ".ai-sdlc-loop" or normalized.startswith(".ai-sdlc-loop/")):
        raise LoopError(f"path overlaps Loop state: {value}")
    current = root
    for part in Path(normalized).parts:
        current = current / part
        if current.is_symlink():
            raise LoopError(f"path contains a symlink: {value}")
    resolved = (root / normalized).resolve(strict=False)
    if resolved != root and root not in resolved.parents:
        raise LoopError(f"path escapes project root: {value}")
    return normalized


def run_git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    if check and result.returncode:
        raise LoopError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result


def changed_paths(root: Path) -> list[str]:
    if run_git(root, "rev-parse", "--is-inside-work-tree", check=False).returncode:
        raise LoopError("project root must be a Git worktree")
    paths: set[str] = set()
    for args in (("diff", "--name-only", "-z"), ("diff", "--cached", "--name-only", "-z"), ("ls-files", "--others", "--exclude-standard", "-z")):
        result = run_git(root, *args)
        for path in result.stdout.split("\0"):
            if (
                path
                and not path == ".ai"
                and not path.startswith(".ai/")
                and not path == ".ai-sdlc"
                and not path.startswith(".ai-sdlc/")
                and not path == ".ai-sdlc-loop"
                and not path.startswith(".ai-sdlc-loop/")
            ):
                paths.add(safe_relative(root, path))
    return sorted(paths)


def path_allowed(path: str, allowed: list[str]) -> bool:
    return any(path == item or path.startswith(item.rstrip("/") + "/") for item in allowed)


def file_digest(root: Path, path: str) -> dict[str, Any]:
    target = root / path
    if not target.exists():
        return {"path": path, "kind": "deleted"}
    if not target.is_file():
        raise LoopError(f"changed path is not a regular file: {path}")
    mode = "100755" if target.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) else "100644"
    return {
        "path": path,
        "kind": "file",
        "mode": mode,
        "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
    }


def change_snapshot(root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    paths = changed_paths(root)
    outside = [path for path in paths if not path_allowed(path, spec["allowed_paths"])]
    if outside:
        raise LoopError("changes outside approved paths: " + ", ".join(outside))
    value = {"spec_fingerprint": spec["fingerprint"], "files": [file_digest(root, path) for path in paths]}
    value["fingerprint"] = fingerprint(value)
    return value


def require_quality_gate(
    root: Path,
    feature: str,
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    """Fail closed unless the canonical quality report is valid and current."""
    report_path = state_path(root, feature, "quality-gate.toon")
    if not report_path.is_file():
        raise LoopError(
            "current engineering quality-gate evidence is required before Verify: "
            f".ai-sdlc-loop/{feature}/quality-gate.toon"
        )
    if not QUALITY_GATE_SCRIPT.is_file():
        raise LoopError("the Engineering Quality Gate validator is unavailable")
    module_spec = importlib.util.spec_from_file_location(
        "_ai_sdlc_loop_engineering_quality_gate",
        QUALITY_GATE_SCRIPT,
    )
    if module_spec is None or module_spec.loader is None:
        raise LoopError("the Engineering Quality Gate validator cannot be loaded")
    module = importlib.util.module_from_spec(module_spec)
    try:
        module_spec.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError) as exc:
        raise LoopError(f"the Engineering Quality Gate validator cannot be loaded: {exc}") from exc
    validator = getattr(module, "verify_report_current", None)
    validation_error = getattr(module, "QualityGateError", None)
    if not callable(validator) or not isinstance(validation_error, type):
        raise LoopError("the Engineering Quality Gate validator contract is invalid")
    try:
        report = validator(root, report_path)
    except validation_error as exc:
        raise LoopError(f"engineering quality-gate evidence is invalid or stale: {exc}") from exc
    if report.get("status") not in {"PASS", "PASS_WITH_FINDINGS"}:
        raise LoopError("engineering quality gate did not pass")
    decision = report.get("final_decision")
    if not isinstance(decision, dict) or decision.get("ready_for_next_stage") is not True:
        raise LoopError("engineering quality gate is not ready for Verify")
    if report.get("change_fingerprint") != snapshot["fingerprint"]:
        raise LoopError("engineering quality-gate evidence does not match the exact Loop change snapshot")
    return report


def current_spec(root: Path, feature: str) -> dict[str, Any]:
    spec = load_toon(state_path(root, feature, "spec.toon"))
    if spec.get("schema") != SCHEMA or spec.get("feature") != feature:
        raise LoopError("unsupported or mismatched spec")
    if spec.get("fingerprint") != fingerprint(spec):
        raise LoopError("spec fingerprint does not match its content")
    if (not isinstance(spec.get("request"), str) or not spec["request"].strip()
            or not isinstance(spec.get("allowed_paths"), list) or not spec["allowed_paths"]
            or any(not isinstance(path, str) for path in spec["allowed_paths"])
            or not isinstance(spec.get("trace_ids"), list)
            or any(not isinstance(trace, str) or not trace.strip() for trace in spec["trace_ids"])):
        raise LoopError("invalid specification input fields")
    if spec["allowed_paths"] != sorted(set(safe_relative(root, path) for path in spec["allowed_paths"])):
        raise LoopError("specification paths must be canonical and unique")
    return spec


def require_approval(root: Path, feature: str, action: str, subject: str) -> dict[str, Any]:
    receipt = load_toon(state_path(root, feature, "approvals", f"{action}.toon"))
    if receipt.get("schema") != SCHEMA or receipt.get("action") != action:
        raise LoopError(f"invalid {action} approval receipt")
    if receipt.get("decision") != "approve":
        raise LoopError(f"{action} was not approved")
    if receipt.get("subject_fingerprint") != subject:
        raise LoopError(f"stale or mismatched {action} approval")
    return receipt


def redact(value: str) -> str:
    value = PRIVATE_KEY_RE.sub("[REDACTED PRIVATE KEY]", value)
    return SECRET_RE.sub(lambda match: match.group(1) + "[REDACTED]", value)


def split_command(value: str) -> list[str]:
    argv = shlex.split(value, posix=os.name != "nt")
    if os.name == "nt":
        argv = [item[1:-1] if len(item) >= 2 and item[0] == item[-1] and item[0] in {'"', "'"} else item for item in argv]
    return argv


def refresh_task_context(task: dict[str, Any], root: Path, paths: list[str]) -> None:
    """Do not turn optional packing into a ban on existing sensitive-file scopes."""
    selected = []
    for path in paths:
        safe_relative(root, path)
        if adaptive.SECRET_PATH.search(path):
            adaptive.escalate(task, observed={"security": True})
            note = path + ": sensitive source omitted from context; use its owning review"
            questions = task["context_pack"]["unresolved_questions"]
            if note not in questions:
                questions.append(note)
        else:
            selected.append(path)
    adaptive.refresh_context(task, root, selected)


def record_stage_telemetry(
    root: Path,
    feature: str,
    stage: str,
    *,
    status: str = "success",
    duration_ms: int | None = None,
    skill: str | None = None,
    error: dict[str, str] | None = None,
) -> None:
    """Record telemetry event on stage completion fail-open."""
    try:
        import ai_sdlc_telemetry
        skill_name = skill or f"ai-sdlc-loop-{stage}"
        ai_sdlc_telemetry.record_telemetry_event(
            skill=skill_name,
            status=status,
            duration_ms=duration_ms,
            task={"id": feature, "type": "stage", "title": stage, "owner": ""},
            product="ai-sdlc-loop",
            error=error,
            root=root,
        )
    except Exception:
        pass


def cmd_specify(args: argparse.Namespace) -> None:
    started = time.perf_counter()
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    allowed = sorted(set(safe_relative(root, value) for value in args.allow))
    if not allowed:
        raise LoopError("at least one --allow path is required")
    spec: dict[str, Any] = {
        "schema": SCHEMA,
        "feature": feature,
        "request": normalize_request(args.request),
        "allowed_paths": allowed,
        "trace_ids": sorted(set(args.trace)),
    }
    spec["fingerprint"] = fingerprint(spec)
    state_file = state_path(root, feature, "state.toon")
    state = load_toon(state_file) if state_file.exists() else {}
    task = state.get("execution")
    facts = adaptive.signals(args.signal)
    if task:
        if task["request"] != spec["request"]:
            task["request"] = spec["request"]
            task["context_pack"]["task"] = spec["request"]
            task["result"] = "in-progress"
            task["completed_stages"] = []
        adaptive.escalate(task, allowed, facts)
        minimum = "DEEP" if args.full_flow else args.mode
        adaptive.raise_minimum(task, minimum)
    else:
        task = adaptive.new_task(spec["request"], allowed, facts, minimum=args.mode, full=args.full_flow)
    refresh_task_context(task, root, [p for p in allowed if (root / p).is_file()])
    if "context" not in task["completed_stages"]:
        adaptive.complete_stage(task, "context", ["spec.toon"])
        record_stage_telemetry(root, feature, "context", skill="ai-sdlc-loop-specify", duration_ms=int((time.perf_counter() - started) * 1000))
    adaptive.stage_event(task, "classify-context", time.perf_counter() - started,
                         skills=["ai-sdlc-loop-specify"])
    state.update({"schema": SCHEMA, "feature": feature, "stage": "specified",
                  "spec_fingerprint": spec["fingerprint"], "execution": task})
    atomic_toon(state_path(root, feature, "spec.toon"), spec)
    atomic_toon(state_file, state)
    try:
        import usage_journal
        usage_journal.record_event(
            "skill.start",
            {"skill": "ai-sdlc-loop-specify", "phase": "specify", "trigger": "user", "task_kind": "feature", "feature": feature},
            root=root,
        )
        usage_journal.record_skill_end(
            "ai-sdlc-loop-specify",
            status="completed",
            duration_ms=int((time.perf_counter() - started) * 1000),
            feature=feature,
            artifacts=[f".ai-sdlc-loop/{feature}/spec.toon"],
            root=root,
        )
        usage_journal.record_event(
            "artifact.created",
            {"artifact_type": "spec", "artifact_ref": f".ai-sdlc-loop/{feature}/spec.toon", "owning_skill": "ai-sdlc-loop-specify"},
            root=root,
        )
    except Exception:
        pass
    print(spec["fingerprint"])


def cmd_approve(args: argparse.Namespace) -> None:
    started = time.perf_counter()
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    if args.action == "implement":
        expected = current_spec(root, feature)["fingerprint"]
    else:
        evidence = current_evidence(root, feature, current_spec(root, feature))
        expected = evidence.get("verified_fingerprint")
    if args.fingerprint != expected:
        raise LoopError(f"fingerprint does not match current {args.action} subject")
    receipt = {
        "schema": SCHEMA,
        "feature": feature,
        "action": args.action,
        "decision": args.decision,
        "reviewer": args.reviewer.strip(),
        "subject_fingerprint": args.fingerprint,
        "recorded_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    if not receipt["reviewer"]:
        raise LoopError("reviewer must not be empty")
    atomic_toon(state_path(root, feature, "approvals", f"{args.action}.toon"), receipt)
    try:
        import usage_journal
        usage_journal.record_event(
            f"approval.{args.decision}",
            {"feature": feature, "action": args.action, "reviewer": receipt["reviewer"], "subject_fingerprint": receipt["subject_fingerprint"]},
            root=root,
        )
        usage_journal.record_skill_end(
            "ai-sdlc-loop-approvals-sandbox",
            status="completed",
            duration_ms=int((time.perf_counter() - started) * 1000),
            feature=feature,
            root=root,
        )
    except Exception:
        pass
    print(f"{args.action}: {args.decision}")


def cmd_implement_check(args: argparse.Namespace) -> None:
    started = time.perf_counter()
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    spec = current_spec(root, feature)
    require_approval(root, args.feature, "implement", spec["fingerprint"])
    try:
        import usage_journal
        usage_journal.record_skill_end(
            "ai-sdlc-loop-implement",
            status="completed",
            duration_ms=int((time.perf_counter() - started) * 1000),
            feature=feature,
            root=root,
        )
    except Exception:
        pass
    print("implement eligible: " + spec["fingerprint"])


def cmd_verify(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    if args.timeout <= 0 or not 1 <= args.jobs <= 8:
        raise LoopError("verification timeout must be positive and jobs must be 1..8")
    if args.jobs > 1 and not args.independent:
        raise LoopError("parallel checks require --independent after checking shared resources")
    started = time.perf_counter()
    spec = current_spec(root, feature)
    require_approval(root, feature, "implement", spec["fingerprint"])
    snapshot = change_snapshot(root, spec)
    require_quality_gate(root, feature, snapshot)
    state_file = state_path(root, feature, "state.toon")
    state = load_toon(state_file)
    task = state.get("execution") or adaptive.new_task(spec["request"], spec["allowed_paths"])
    paths = [row["path"] for row in snapshot["files"]]
    adaptive.escalate(task, paths)
    refresh_task_context(task, root, paths)
    commands = [split_command(command) for command in args.command]
    if any(not argv for argv in commands):
        raise LoopError("verification command must not be empty")
    if len({tuple(argv) for argv in commands}) != len(commands):
        raise LoopError("duplicate verification commands must be removed")
    action = adaptive.verification_action(task, snapshot["fingerprint"], commands, condition=args.retry_condition)
    if action == "done":
        evidence = current_evidence(root, feature, spec)
        print(evidence["verified_fingerprint"])
        return

    def execute(argv):
        command_start = time.perf_counter()
        try:
            result = subprocess.run(argv, cwd=root, text=True, errors="replace", capture_output=True, timeout=args.timeout, check=False)
            record = {"argv": [redact(item) for item in argv], "exit_code": result.returncode, "timed_out": False, "stdout": redact(result.stdout[-8000:]), "stderr": redact(result.stderr[-8000:])}
        except (OSError, subprocess.TimeoutExpired) as exc:
            record = {"argv": [redact(item) for item in argv], "exit_code": None, "timed_out": isinstance(exc, subprocess.TimeoutExpired), "stdout": "", "stderr": redact(str(exc))}
        record["seconds"] = time.perf_counter() - command_start
        return record

    if args.jobs == 1:
        records = [execute(argv) for argv in commands]
    else:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            records = list(pool.map(execute, commands))
    ready = all(row["exit_code"] == 0 for row in records)
    # A passing command may rewrite the files it checks. Never bind that success
    # to the pre-command snapshot without checking the post-command state.
    drift_reason = ""
    try:
        if current_spec(root, feature)["fingerprint"] != spec["fingerprint"]:
            raise LoopError("specification changed during verification")
        if change_snapshot(root, spec)["fingerprint"] != snapshot["fingerprint"]:
            raise LoopError("changes drifted during verification")
        require_quality_gate(root, feature, snapshot)
    except LoopError as exc:
        ready = False
        drift_reason = str(exc)
    evidence: dict[str, Any] = {
        "schema": SCHEMA,
        "feature": feature,
        "spec_fingerprint": spec["fingerprint"],
        "change_fingerprint": snapshot["fingerprint"],
        "changed_files": snapshot["files"],
        "commands": records,
        "ready": ready,
    }
    if drift_reason:
        evidence["failure_reason"] = drift_reason
    evidence["verified_fingerprint"] = fingerprint(evidence, "verified_fingerprint")
    atomic_toon(state_path(root, feature, "evidence.toon"), evidence)
    adaptive.record_verification(task, snapshot["fingerprint"], commands, ready, condition=args.retry_condition)
    if ready and adaptive.next_stage(task) == "verify":
        adaptive.complete_stage(task, "verify", ["evidence.toon", "quality-gate.toon"])
        record_stage_telemetry(root, feature, "verify", status="success", skill="ai-sdlc-loop-verify", duration_ms=int((time.perf_counter() - started) * 1000))
    elif not ready:
        record_stage_telemetry(root, feature, "verify", status="fail", skill="ai-sdlc-loop-verify", duration_ms=int((time.perf_counter() - started) * 1000), error={"code": "VERIFICATION_FAILED", "message": drift_reason or "command_failed"})
    task["changes"] = snapshot["files"]
    adaptive.stage_event(task, "verify", time.perf_counter() - started,
                         skills=["ai-sdlc-loop-verify"], checks=[row["argv"] for row in records],
                         model_calls=0, tool_calls=len(records), context_tokens=0)
    state.update({"schema": SCHEMA, "feature": feature, "stage": "verified" if ready else "verification-failed",
                  "spec_fingerprint": spec["fingerprint"], "verified_fingerprint": evidence["verified_fingerprint"],
                  "ready": ready, "execution": task})
    atomic_toon(state_file, state)
    if ready:
        try:
            import usage_journal
            usage_journal.record_event(
                "verification.passed",
                {"feature": feature, "verified_fingerprint": evidence["verified_fingerprint"]},
                root=root,
            )
            usage_journal.record_skill_end(
                "ai-sdlc-loop-verify",
                status="completed",
                duration_ms=int((time.perf_counter() - started) * 1000),
                feature=feature,
                artifacts=[f".ai-sdlc-loop/{feature}/evidence.toon"],
                root=root,
            )
        except Exception:
            pass
    else:
        try:
            import usage_journal
            usage_journal.record_event(
                "verification.failed",
                {"feature": feature, "reason": drift_reason or "command_failed"},
                root=root,
            )
            usage_journal.record_skill_end(
                "ai-sdlc-loop-verify",
                status="failed",
                duration_ms=int((time.perf_counter() - started) * 1000),
                feature=feature,
                root=root,
            )
        except Exception:
            pass
    print(evidence["verified_fingerprint"])
    if not ready:
        raise LoopError(drift_reason or "one or more verification commands failed")


def current_evidence(root: Path, feature: str, spec: dict[str, Any]) -> dict[str, Any]:
    """Reuse one readiness gate for approval and commit; hashes are not approval."""
    evidence = load_toon(state_path(root, feature, "evidence.toon"))
    if (evidence.get("schema") != SCHEMA or evidence.get("feature") != feature
            or evidence.get("ready") is not True
            or evidence.get("spec_fingerprint") != spec["fingerprint"]):
        raise LoopError("current passing verification evidence is required")
    if evidence.get("verified_fingerprint") != fingerprint(evidence, "verified_fingerprint"):
        raise LoopError("verification evidence fingerprint is invalid")
    commands = evidence.get("commands")
    if not isinstance(commands, list) or not commands or any(
        not isinstance(command, dict)
        or type(command.get("exit_code")) is not int
        or command["exit_code"] != 0
        or command.get("timed_out") is not False
        or not isinstance(command.get("argv"), list) or not command["argv"]
        for command in commands
    ):
        raise LoopError("verification evidence requires executed passing commands")
    snapshot = change_snapshot(root, spec)
    if (snapshot["fingerprint"] != evidence.get("change_fingerprint")
            or snapshot["files"] != evidence.get("changed_files")):
        raise LoopError("changes drifted after verification")
    require_quality_gate(root, feature, snapshot)
    return evidence


def cmd_commit(args: argparse.Namespace) -> None:
    started = time.perf_counter()
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    spec = current_spec(root, feature)
    evidence = current_evidence(root, feature, spec)
    require_approval(root, feature, "commit", evidence["verified_fingerprint"])
    paths = [item["path"] for item in evidence["changed_files"]]
    if not paths:
        raise LoopError("there are no approved changes to commit")
    prior_index = run_git(root, "write-tree").stdout.strip()
    run_git(root, "add", "--", *paths)
    message = f"{args.message}\n\nAI-SDLC-Loop-Feature: {feature}\nAI-SDLC-Loop-Verified: {evidence['verified_fingerprint']}"
    result = run_git(root, "commit", "-m", message, check=False)
    if result.returncode:
        run_git(root, "read-tree", prior_index, check=False)
        raise LoopError(result.stderr.strip() or "git commit failed")
    try:
        import usage_journal
        usage_journal.record_skill_end(
            "ai-sdlc-loop-commit",
            status="completed",
            duration_ms=int((time.perf_counter() - started) * 1000),
            feature=feature,
            root=root,
        )
    except Exception:
        pass
    print(run_git(root, "rev-parse", "HEAD").stdout.strip())


def cmd_promote(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    spec = current_spec(root, feature)
    payload: dict[str, Any] = {
        "schema": PROMOTION_SCHEMA,
        "source_schema": SCHEMA,
        "feature": feature,
        "request": spec["request"],
        "allowed_paths": spec["allowed_paths"],
        "trace_ids": spec["trace_ids"],
        "spec_fingerprint": spec["fingerprint"],
    }
    for name in ("state", "evidence", "quality-gate"):
        path = state_path(root, feature, f"{name}.toon")
        if path.exists():
            payload[name.replace("-", "_")] = load_toon(path)
    approvals = {}
    for action in ("implement", "commit"):
        path = state_path(root, feature, "approvals", f"{action}.toon")
        if path.exists():
            approvals[action] = load_toon(path)
    payload["approvals"] = approvals
    output = Path(args.output)
    if output.suffix != ".toon":
        raise LoopError("promotion output must use a .toon extension")
    if not output.is_absolute():
        output = root / safe_relative(root, args.output, allow_state=True)
    atomic_toon(output, payload)
    print(output)


def cmd_status(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    result = {"spec": load_toon(state_path(root, feature, "spec.toon")), "state": load_toon(state_path(root, feature, "state.toon"))}
    quality_gate = state_path(root, feature, "quality-gate.toon")
    if quality_gate.exists():
        result["quality_gate"] = load_toon(quality_gate)
    print(encode_toon(result), end="")


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--project-root", default=".")
    commands = value.add_subparsers(dest="command_name", required=True)
    steps = commands.add_parser("steps", help="select dependency-ready nodes in a compact Loop stage graph; read-only")
    steps.add_argument("--skill", required=True)
    steps.add_argument("--phase", required=True)
    steps.add_argument("--completed-step", action="append", default=[])
    steps.set_defaults(handler=cmd_steps)
    specify = commands.add_parser("specify", help="persist a bounded deterministic specification")
    specify.add_argument("--feature", required=True)
    specify.add_argument("--request", required=True)
    specify.add_argument("--allow", action="append", required=True)
    specify.add_argument("--trace", action="append", default=[])
    specify.add_argument("--mode", choices=adaptive.MODES, default="FAST", help="minimum execution depth; risk can raise it")
    specify.add_argument("--signal", action="append", default=[], help="observed key=true/false or files/modules=count")
    specify.add_argument("--full-flow", action="store_true")
    specify.add_argument("--quick-flow", action="store_true")
    specify.set_defaults(handler=cmd_specify)
    approve = commands.add_parser("approve", help="record an explicit reviewer decision")
    approve.add_argument("--feature", required=True)
    approve.add_argument("--action", choices=("implement", "commit"), required=True)
    approve.add_argument("--decision", choices=("approve", "reject"), required=True)
    approve.add_argument("--fingerprint", required=True)
    approve.add_argument("--reviewer", required=True)
    approve.set_defaults(handler=cmd_approve)
    implement = commands.add_parser("implement-check", help="verify Implement authority")
    implement.add_argument("--feature", required=True)
    implement.set_defaults(handler=cmd_implement_check)
    evidence = commands.add_parser("evidence-check", help="verify current passing evidence without granting commit authority")
    evidence.add_argument("--feature", required=True)
    evidence.set_defaults(handler=cmd_evidence_check)
    verify = commands.add_parser("verify", help="run explicit checks and persist evidence")
    verify.add_argument("--feature", required=True)
    verify.add_argument("--command", action="append", required=True)
    verify.add_argument("--timeout", type=int, default=300)
    verify.add_argument("--jobs", type=int, default=1)
    verify.add_argument("--independent", action="store_true", help="assert commands have no shared mutable resources")
    verify.add_argument("--retry-condition", default="", help="evidence of a changed environment enabling retry")
    verify.set_defaults(handler=cmd_verify)
    commit = commands.add_parser("commit", help="create one separately approved commit")
    commit.add_argument("--feature", required=True)
    commit.add_argument("--message", required=True)
    commit.set_defaults(handler=cmd_commit)
    promote = commands.add_parser("promote", help="emit a Harness-compatible artifact")
    promote.add_argument("--feature", required=True)
    promote.add_argument("--output", required=True)
    promote.set_defaults(handler=cmd_promote)
    adapt = commands.add_parser("adapt", help="reuse task context, record plan and escalate from new observations")
    adapt.add_argument("--feature", required=True)
    adapt.add_argument("--signal", action="append", default=[])
    adapt.add_argument("--context-file", action="append", default=[])
    adapt.add_argument("--plan-step", action="append", default=[])
    adapt.add_argument("--complete-stage", choices=("planning", "readiness", "sdd", "implement"))
    adapt.add_argument("--evidence", action="append", default=[])
    adapt.add_argument("--record-stage")
    adapt.add_argument("--elapsed", type=float)
    adapt.add_argument("--model-calls", type=int)
    adapt.add_argument("--tool-calls", type=int)
    adapt.add_argument("--context-tokens", type=int)
    adapt.add_argument("--skill", action="append", default=[])
    adapt.set_defaults(handler=cmd_adapt)
    advance = commands.add_parser("next", help="select missing adaptive work; never execute or approve it")
    advance.add_argument("--feature", required=True)
    advance.set_defaults(handler=cmd_next)
    status = commands.add_parser("status", help="show current local Loop state")
    status.add_argument("--feature", required=True)
    status.set_defaults(handler=cmd_status)
    return value


def cmd_adapt(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    spec = current_spec(root, feature)
    path = state_path(root, feature, "state.toon")
    state = load_toon(path)
    task = state.get("execution") or adaptive.new_task(spec["request"], spec["allowed_paths"])
    # Escalation changes process depth, never the approved source scope.
    adaptive.escalate(task, args.context_file, adaptive.signals(args.signal))
    adaptive.refresh_context(task, root, args.context_file)
    if args.plan_step:
        task["plan"] = args.plan_step
        if adaptive.next_stage(task) == "compact-plan":
            adaptive.complete_stage(task, "compact-plan", ["state.toon:execution.plan"])
            record_stage_telemetry(root, feature, "compact-plan", skill="ai-sdlc-loop-planning")
    if args.complete_stage:
        if args.complete_stage == "implement":
            require_approval(root, feature, "implement", spec["fingerprint"])
            change_snapshot(root, spec)
        for evidence in args.evidence:
            if not (root / safe_relative(root, evidence, allow_state=True)).is_file():
                raise LoopError("stage evidence file is missing: " + evidence)
        adaptive.complete_stage(task, args.complete_stage, args.evidence)
        stage_dur = int(args.elapsed * 1000) if getattr(args, "elapsed", None) else None
        stage_skill = args.skill[0] if getattr(args, "skill", None) else None
        record_stage_telemetry(root, feature, args.complete_stage, duration_ms=stage_dur, skill=stage_skill)
    if args.record_stage:
        if args.elapsed is None:
            raise LoopError("record-stage requires measured --elapsed")
        adaptive.stage_event(task, args.record_stage, args.elapsed, skills=args.skill,
                             model_calls=args.model_calls, tool_calls=args.tool_calls, context_tokens=args.context_tokens)
    state["execution"] = task
    atomic_toon(path, state)
    print(encode_toon(task), end="")


def cmd_next(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    spec = current_spec(root, feature)
    state = load_toon(state_path(root, feature, "state.toon"))
    task = state.get("execution")
    if task is None:
        print(encode_toon({"next_stage": "legacy", "owning_skill": "ai-sdlc-loop-orchestrate", "authorizes_execution": False}), end="")
        return
    stage = adaptive.next_stage(task)
    owner = {"context": "specify", "compact-plan": "specify", "planning": "specify",
             "readiness": "requirements-review", "sdd": "specify", "implement": "implement",
             "verify": "verify", "done": "", "human-diagnosis": ""}[stage]
    if stage == "verify":
        try:
            require_quality_gate(root, feature, change_snapshot(root, spec))
        except LoopError:
            stage, owner = "quality-gate", "engineering-quality-gate"
    if stage == "done":
        current_evidence(root, feature, spec)
    print(encode_toon({"mode": task["decision"]["mode"], "next_stage": stage,
                      "owning_skill": "ai-sdlc-loop-" + owner if owner else "",
                      "context_ref": "state.toon:execution.context_pack", "authorizes_execution": False}), end="")


def cmd_steps(args: argparse.Namespace) -> None:
    try:
        from loop_steps import select_steps
    except ImportError:
        _peer_scripts = Path(__file__).resolve().parents[3] / "products" / "ai-sdlc-loop" / "skills" / "ai-sdlc-loop-shared-runtime" / "scripts"
        if _peer_scripts.is_dir() and str(_peer_scripts) not in sys.path:
            sys.path.insert(0, str(_peer_scripts))
        from loop_steps import select_steps
    try:
        skills_root = (
            SHARED_SCRIPTS.parents[1]
            if (SHARED_SCRIPTS.parents[1] / args.skill).is_dir()
            else Path(__file__).resolve().parents[3] / "products" / "ai-sdlc-loop" / "skills"
        )
        result = select_steps(skills_root, args.skill, args.phase, args.completed_step)
    except (OSError, ValueError) as exc:
        raise LoopError(str(exc)) from exc
    print(encode_toon(result), end="")


def cmd_evidence_check(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    feature = validate_feature(args.feature)
    evidence = current_evidence(root, feature, current_spec(root, feature))
    print(encode_toon({"schema": SCHEMA, "feature": feature, "ready": True,
                       "verified_fingerprint": evidence["verified_fingerprint"],
                       "authorizes_commit": False}), end="")


def main() -> int:
    args = parser().parse_args()
    try:
        args.handler(args)
    except (LoopError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
