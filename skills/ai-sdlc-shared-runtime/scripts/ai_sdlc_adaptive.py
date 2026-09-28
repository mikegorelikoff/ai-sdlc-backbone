#!/usr/bin/env python3
"""Risk-proportional execution policy and reusable task evidence; never approval.

The host supplies semantic observations, not a desired low-risk verdict. Unknown
facts prevent FAST. Runtime-owned receipts remain the authority for completion.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import time
from pathlib import Path

from ai_sdlc_toon import decode_toon, encode_toon
from ai_sdlc_safe_io import bounded_path, atomic_write_text

MODES = ("FAST", "STANDARD", "DEEP")
BOOLEAN_SIGNALS = {
    "architecture", "security", "migration", "production_critical", "irreversible",
    "ambiguous", "external_integration", "dependency_change", "assumptions_failed",
    "familiar", "covered", "confident", "boundary_behavior", "installation_failure",
    "repeated_defect", "independent_review", "specialized_qa",
}
NUMBER_SIGNALS = {"files", "modules"}
CONTEXT_SECTIONS = ("relevant_symbols", "architecture_context", "dependencies",
                    "constraints", "conventions", "tests", "assumptions", "unresolved_questions")
HIGH_RISK = r"\b(architectur\w*|migrat\w*|security|auth\w*|crypt\w*|schema|cross-cutting|data.loss)\b"
SENSITIVE_PATH = r"(^|/)(auth\w*|security|migrations?|schemas?|crypto)(/|\.|$)"
SECRET_PATH = re.compile(r"(^|/)(\.env(?:\..*)?|.*\.(?:pem|key)|credentials[^/]*|secrets?[^/]*)$", re.I)


def digest(value: object) -> str:
    return hashlib.sha256(encode_toon(value).encode()).hexdigest()


def signals(values: list[str]) -> dict:
    result = {}
    for value in values:
        key, separator, raw = value.partition("=")
        if not separator or key not in BOOLEAN_SIGNALS | NUMBER_SIGNALS:
            raise ValueError(f"unknown risk signal: {value}")
        if key in BOOLEAN_SIGNALS:
            if raw not in {"true", "false"}:
                raise ValueError(f"{key} must be true or false")
            result[key] = raw == "true"
        else:
            if not raw.isdigit():
                raise ValueError(f"{key} must be a nonnegative integer")
            result[key] = int(raw)
    return result


def classify(request: str, paths=(), observed=None, *, minimum="FAST", full=False) -> dict:
    if not isinstance(request, str) or not request.strip() or minimum not in MODES:
        raise ValueError("nonempty request and valid minimum mode required")
    observed = dict(observed or {})
    for key, value in observed.items():
        if key not in BOOLEAN_SIGNALS | NUMBER_SIGNALS:
            raise ValueError(f"unknown risk signal: {key}")
        if key in BOOLEAN_SIGNALS and type(value) is not bool:
            raise ValueError(f"{key} must be boolean")
        if key in NUMBER_SIGNALS and (type(value) is not int or value < 0):
            raise ValueError(f"{key} must be nonnegative integer")
    paths = sorted(set(paths))
    if any(not isinstance(p, str) or not p for p in paths):
        raise ValueError("paths must be nonempty strings")
    count = max(len(paths), observed.get("files", 0))
    modules = max(len({p.split('/')[0] for p in paths if '/' in p}), observed.get("modules", 0))
    high = [key for key in ("architecture", "security", "migration", "production_critical", "irreversible", "ambiguous") if observed.get(key)]
    if re.search(HIGH_RISK, request, re.I):
        high.append("request contains architectural, security or data-change signal")
    if any(re.search(SENSITIVE_PATH, p, re.I) for p in paths):
        high.append("sensitive source path")
    if count > 15 or modules > 4:
        high.append("broad change surface")
    docs = bool(paths) and all(p.endswith(('.md', '.rst')) or p.startswith('docs/') and p.endswith('.txt') for p in paths)
    small = bool(re.search(r"\b(tiny|typo|localized bug|small (?:bug|config)|test.only)\b", request, re.I))
    known = all(observed.get(key) is True for key in ("familiar", "covered", "confident"))
    moderate = [key for key in ("external_integration", "dependency_change", "assumptions_failed") if observed.get(key)]
    if high:
        mode, reasons = "DEEP", high
    elif moderate or count > 3 or modules > 1:
        mode, reasons = "STANDARD", moderate or ["multiple files or modules require an explicit plan"]
    elif count and (docs or small and known):
        mode, reasons = "FAST", ["bounded documentation surface" if docs else "local change with confirmed path, familiarity and coverage"]
    else:
        mode, reasons = "STANDARD", ["implementation reasoning or missing scope/confidence evidence"]
    required = "DEEP" if full else minimum
    if MODES.index(required) > MODES.index(mode):
        mode = required
        reasons.append("explicit full workflow or protected minimum")
    return {"mode": mode, "reasons": reasons, "signals": observed,
            "change_surface": {"files": count, "modules": modules, "paths": paths}}


def strategy(decision: dict) -> dict:
    mode, facts = decision["mode"], decision["signals"]
    stages = ["context"]
    if mode == "STANDARD":
        stages += ["compact-plan"]
    elif mode == "DEEP":
        stages += ["planning", "readiness", "sdd"]
    stages += ["implement", "verify"]
    capabilities = {}
    for name, signal, reason in (
        ("doctor", "installation_failure", "installation or environment failure"),
        ("bug-hunter", "repeated_defect", "recurring defect unexplained by checks"),
        ("edge-case-hunter", "boundary_behavior", "changed boundary behavior"),
        ("blind-case-hunter", "independent_review", "independent assumptions review required"),
        ("specialized-qa", "specialized_qa", "domain acceptance needs specialized review"),
    ):
        if facts.get(signal):
            capabilities[name] = reason
    if mode == "DEEP":
        capabilities["hierarchical-decomposition"] = "high-risk scope or uncertainty"
    if facts.get("security") or any("security" in r or "sensitive" in r for r in decision["reasons"]):
        capabilities["security-testing"] = "security-sensitive change"
    return {"stages": stages, "capabilities": capabilities,
            "checks": ["targeted-tests", "diff-check"] + ([] if mode == "FAST" else ["affected-integration-checks"]),
            "semantic_review": "acceptance and changed behavior" if mode != "DEEP" else "full risk and acceptance strategy",
            "parallelism": "only declared independent checks after implementation settles",
            "attempt_limit": 3, "authorizes_execution": False}


def new_task(request: str, paths=(), observed=None, *, minimum="FAST", full=False) -> dict:
    decision = classify(request, paths, observed, minimum=minimum, full=full)
    return {"schema": "ai-sdlc-adaptive-task/v1", "request": request,
            "decision": decision, "strategy": strategy(decision), "decisions": [],
            "context_pack": {"task": request, "relevant_files": {}, "change_surface": decision["change_surface"],
                             **{key: [] for key in CONTEXT_SECTIONS}},
            "plan": [], "changes": [], "verification": [], "result": "in-progress",
            "completed_stages": [], "evidence_refs": {},
            "metrics": {"started_at": time.time(), "total_seconds": 0.0, "stages": [],
                        "model_calls": None, "tool_calls": None, "context_tokens": None,
                        "context_token_estimate": 0, "context_reads": 0, "context_reuses": 0,
                        "duplicate_context_reads": 0, "verification_iterations": 0,
                        "escalations": 0, "skills_invoked": [], "deterministic_checks": []}}


def escalate(task: dict, paths=(), observed=None) -> bool:
    merged = {**task["decision"]["signals"], **(observed or {})}
    # Risk observations are sticky within a task; fresh confidence cannot erase them.
    for key in BOOLEAN_SIGNALS - {"familiar", "covered", "confident"}:
        if task["decision"]["signals"].get(key):
            merged[key] = True
    all_paths = sorted(set(paths) | set(task["decision"]["change_surface"]["paths"]))
    before = task["decision"]["mode"]
    decision = classify(task["request"], all_paths, merged, minimum=before)
    changed = before != decision["mode"]
    if changed:
        task["decisions"].append({"from": before, "to": decision["mode"], "reasons": decision["reasons"]})
        task["metrics"]["escalations"] += 1
        task["result"] = "in-progress"
    task["decision"], task["strategy"] = decision, strategy(decision)
    task["context_pack"]["change_surface"] = decision["change_surface"]
    return changed


def next_stage(task: dict) -> str:
    """Escalation adds only missing work; completed implementation is preserved."""
    if task["result"] == "blocked":
        return "human-diagnosis"
    if task["result"] == "needs-repair":
        return "implement"
    for stage in task["strategy"]["stages"]:
        if stage not in task["completed_stages"]:
            return stage
    return "done" if task["result"] == "done" else "verify"


def raise_minimum(task: dict, mode: str, reason='explicit full workflow or protected minimum') -> None:
    if mode not in MODES:
        raise ValueError("invalid minimum mode")
    before = task['decision']['mode']
    if MODES.index(mode) <= MODES.index(before):
        return
    task['decision']['mode'] = mode
    task['decision']['reasons'].append(reason)
    task['decisions'].append({'from': before, 'to': mode, 'reasons': [reason]})
    task['metrics']['escalations'] += 1
    task['strategy'] = strategy(task['decision'])
    task['result'] = 'in-progress'


def complete_stage(task: dict, stage: str, evidence: list[str]) -> None:
    if stage != next_stage(task) or not evidence or any(not isinstance(v, str) or not v.strip() for v in evidence):
        raise ValueError("complete only the next stage with its owning evidence references")
    if stage == "verify" and task["result"] != "done":
        raise ValueError("verification requires executed passing owning-gate evidence")
    task["completed_stages"] = list(dict.fromkeys([*task["completed_stages"], stage]))
    task["evidence_refs"][stage] = evidence
    if stage == "implement" and task["result"] == "needs-repair":
        task["result"] = "in-progress"
        task["completed_stages"] = [s for s in task["completed_stages"] if s != "verify"]


def safe_file(root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or not path.parts or '..' in path.parts or '.git' in path.parts or SECRET_PATH.search(relative):
        raise ValueError(f"unsafe context path: {relative}")
    current = root.resolve()
    for part in path.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f"symlink context path: {relative}")
    if not current.is_relative_to(root.resolve()):
        raise ValueError("context escapes repository")
    return current


def refresh_context(task: dict, root: Path, paths=(), sections=None) -> None:
    """Refresh only selected source records. Hash on resume; never trust mtime alone.

    Keep source references and bounded symbol names, not a second copy of source
    content. Existing graph/StepCard packs supply the actual selected excerpts.
    """
    pack, metrics = task["context_pack"], task["metrics"]
    updates = {}
    for relative in sorted(set(paths) | set(pack["relevant_files"])):
        path = safe_file(root, relative)
        old = pack["relevant_files"].get(relative)
        if not path.exists():
            record = {"sha256": "missing", "bytes": 0, "symbols": []}
        else:
            if not path.is_file():
                raise ValueError(f"context requires regular file: {relative}")
            if path.stat().st_size > 262144:
                updates[relative] = {"sha256": "not-packed", "bytes": path.stat().st_size, "symbols": []}
                question = f"{relative}: oversized source requires its owning reader and freshness evidence"
                if question not in pack['unresolved_questions']:
                    pack['unresolved_questions'].append(question)
                continue
            data = path.read_bytes()
            sha = hashlib.sha256(data).hexdigest()
            metrics["context_reads"] += 1
            if old and old["sha256"] == sha:
                metrics["context_reuses"] += 1
                # A freshness read is detectable duplicate I/O, not rediscovery.
                metrics["duplicate_context_reads"] += 1
                continue
            names = [] if b'\0' in data else re.findall(r"^\s*(?:async\s+)?(?:def|class|function|func)\s+(\w+)", data.decode('utf-8', errors='replace'), re.M)
            record = {"sha256": sha, "bytes": len(data), "symbols": names[:80]}
        updates[relative] = record
    if sections:
        for key, value in sections.items():
            if key not in CONTEXT_SECTIONS or not isinstance(value, list) or any(not isinstance(v, str) for v in value):
                raise ValueError(f"invalid context section: {key}")
        for key, value in sections.items():
            pack[key] = list(dict.fromkeys([*pack[key], *value]))
    pack["relevant_files"].update(updates)
    discovered = [symbol for record in updates.values() for symbol in record['symbols']]
    if any(re.search(r'auth|crypt|permission|credential', symbol, re.I) for symbol in discovered):
        escalate(task, observed={'security': True})
    if any(re.search(r'migrat|schema', symbol, re.I) for symbol in discovered):
        escalate(task, observed={'migration': True})
    metrics["context_token_estimate"] = (len(encode_toon(pack)) + 3) // 4


def stage_event(task: dict, stage: str, elapsed: float, *, skills=(), checks=(), model_calls=None, tool_calls=None, context_tokens=None) -> None:
    if elapsed < 0 or any(v is not None and (type(v) is not int or v < 0) for v in (model_calls, tool_calls, context_tokens)):
        raise ValueError("metrics must be nonnegative; unavailable counters are null")
    metrics = task["metrics"]
    metrics["stages"].append({"stage": stage, "seconds": elapsed, "model_calls": model_calls, "tool_calls": tool_calls, "context_tokens": context_tokens})
    for name, value in (("model_calls", model_calls), ("tool_calls", tool_calls), ("context_tokens", context_tokens)):
        # Total is known only when every stage supplied this counter.
        values = [r[name] for r in metrics["stages"]]
        metrics[name] = sum(values) if all(v is not None for v in values) else None
    metrics["skills_invoked"] = sorted(set(metrics["skills_invoked"]) | set(skills))
    metrics["deterministic_checks"].extend(checks)
    metrics["total_seconds"] = max(0.0, time.time() - metrics["started_at"])


def verification_action(task: dict, fingerprint: str, commands: list, *, condition="") -> str:
    """Require a changed source, check plan, or evidenced environment to retry."""
    key = digest({"change": fingerprint, "commands": commands, "condition": condition})
    previous = task["verification"]
    if previous and previous[-1]["key"] == key:
        if previous[-1]["passed"]:
            return "done"
        raise ValueError("unchanged failed verification: repair or supply changed environment evidence")
    if len(previous) >= task["strategy"]["attempt_limit"]:
        raise ValueError("verification attempt limit exhausted; human diagnosis required")
    return "run"


def record_verification(task: dict, fingerprint: str, commands: list, passed: bool, *, condition="") -> None:
    if verification_action(task, fingerprint, commands, condition=condition) != "run":
        raise ValueError("successful unchanged state is already complete")
    task["verification"].append({"key": digest({"change": fingerprint, "commands": commands, "condition": condition}),
                                 "change_fingerprint": fingerprint, "passed": passed})
    task["metrics"]["verification_iterations"] += 1
    if not passed:
        escalate(task, observed={'assumptions_failed': True})
        if len(task['verification']) >= 2:
            escalate(task, observed={'repeated_defect': True})
            raise_minimum(task, 'DEEP', 'repeated verification failures require deeper diagnosis')
    task["result"] = "done" if passed else "needs-repair" if len(task["verification"]) < task["strategy"]["attempt_limit"] else "blocked"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True)
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--signal", action="append", default=[])
    parser.add_argument("--minimum-mode", choices=MODES, default="FAST")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--task-file", type=Path, help="canonical adaptive evidence record; not a lifecycle approval")
    parser.add_argument("--write", action="store_true", help="explicitly persist task evidence")
    parser.add_argument("--context-file", action="append", default=[])
    parser.add_argument("--plan-step", action="append", default=[])
    parser.add_argument("--record-stage", help="record host timing without claiming stage completion")
    parser.add_argument("--elapsed", type=float)
    parser.add_argument("--model-calls", type=int)
    parser.add_argument("--tool-calls", type=int)
    parser.add_argument("--context-tokens", type=int)
    parser.add_argument("--skill", action="append", default=[])
    args = parser.parse_args()
    try:
        if args.begin_state or args.complete_state or args.state_check and args.write:
            raise ValueError("adaptive evidence cannot begin/complete lifecycle state; state-check is read-only")
        if args.write and not args.task_file:
            raise ValueError("--write requires --task-file")
        if args.task_file:
            path = bounded_path(args.root, args.task_file)
            if path.suffix != '.toon':
                raise ValueError("task file must use canonical TOON")
            if path.is_file():
                task = decode_toon(path.read_text(encoding='utf-8'))
                if not isinstance(task, dict) or task.get('schema') != 'ai-sdlc-adaptive-task/v1' or task.get('request') != args.request:
                    raise ValueError("task record schema/request mismatch; do not reset an existing run")
                escalate(task, args.path, signals(args.signal))
                raise_minimum(task, 'DEEP' if args.full_flow else args.minimum_mode)
            else:
                task = new_task(args.request, args.path, signals(args.signal), minimum=args.minimum_mode, full=args.full_flow)
            refresh_context(task, args.root, args.context_file)
            if args.plan_step:
                task['plan'] = args.plan_step
            if args.record_stage:
                if args.elapsed is None:
                    raise ValueError("recording a stage requires measured --elapsed seconds")
                stage_event(task, args.record_stage, args.elapsed, skills=args.skill,
                            model_calls=args.model_calls, tool_calls=args.tool_calls, context_tokens=args.context_tokens)
            if args.write:
                atomic_write_text(args.root, path, encode_toon(task))
            print(encode_toon({**task, 'next_stage': next_stage(task)}), end='')
        else:
            decision = classify(args.request, args.path, signals(args.signal), minimum=args.minimum_mode, full=args.full_flow)
            print(encode_toon({"schema": "ai-sdlc-adaptive-decision/v1", **decision, "strategy": strategy(decision)}), end="")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
