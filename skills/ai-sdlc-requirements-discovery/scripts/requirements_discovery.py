#!/usr/bin/env python3
"""Prepare, scaffold, validate, finalize and verify sourced discovery packets.

Product-local offline implementation. Imports only the sibling TOON runtime;
business judgment remains explicit draft data, never a deterministic heuristic.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path, PurePosixPath

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL = SKILL_ROOT.name
PREFIX = {
    "ai-sdlc-requirements-discovery": "ai-sdlc",
    "ai-sdlc-loop-requirements-discovery": "ai-sdlc-loop",
}[SKILL]
sys.path.insert(0, str(SKILL_ROOT.parent / f"{PREFIX}-shared-runtime" / "scripts"))
import ai_sdlc_toon as codec  # noqa: E402

CONTEXT_SCHEMA = "ai-sdlc-requirements-discovery-context/v1"
DRAFT_SCHEMA = "ai-sdlc-requirements-discovery-draft/v1"
REPORT_SCHEMA = f"{PREFIX}-requirements-discovery/v1"
RESULT_SCHEMA = "ai-sdlc-requirements-discovery-check/v1"
MAX_SOURCE_BYTES = 64 * 1024
MAX_TOTAL_BYTES = 256 * 1024
MAX_ARTIFACT_BYTES = 2 * 1024 * 1024
MAX_SOURCES = 16


class Invalid(ValueError):
    """A bounded input or output contract failed."""


def normalize(value):
    """Canonicalize semantic sets; workflow order remains explicit prose."""
    if isinstance(value, dict):
        return {key: normalize(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        items = [normalize(item) for item in value]
        if all(isinstance(item, str) for item in items):
            return sorted(items)
        if all(isinstance(item, dict) and "id" in item for item in items):
            return sorted(items, key=lambda item: item["id"])
        return items
    return value


def encoded(value) -> bytes:
    """One canonical encoding for fingerprints, stdout and durable output."""
    return (codec.dumps(normalize(value)).rstrip() + "\n").encode("utf-8")


def digest(value) -> str:
    return hashlib.sha256(encoded(value)).hexdigest()


def feature(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) or len(value) > 80:
        raise Invalid("feature must be a lowercase hyphenated slug of at most 80 characters")
    return value


def safe_path(root: Path, relative: str) -> Path:
    """Reject nonportable paths and every symlink component before access."""
    if not isinstance(relative, str) or not relative or len(relative) > 1024:
        raise Invalid("path must be a nonempty project-relative path")
    path = PurePosixPath(relative)
    if (path.is_absolute() or path.as_posix() != relative or
            any(part in {".", "..", ".git"} for part in path.parts) or
            any(char in relative for char in ("\\", ":")) or
            any(ord(char) < 32 for char in relative)):
        raise Invalid("path must be normalized, contained and outside .git")
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise Invalid(f"symlink path is not allowed: {relative}")
    if not current.resolve().is_relative_to(root):
        raise Invalid("path escapes the project")
    return current


def read_bytes(root: Path, relative: str, limit: int) -> bytes:
    path = safe_path(root, relative)
    if not path.is_file():
        raise Invalid(f"input file is missing: {relative}")
    # Read at most the bound plus one, including if the file grows after stat.
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise Invalid(f"input exceeds {limit} bytes: {relative}")
    return data


def load(root: Path, relative: str):
    if not relative.endswith(".toon"):
        raise Invalid("machine input must use .toon")
    return codec.loads(read_bytes(root, relative, MAX_ARTIFACT_BYTES).decode("utf-8"))


def shape(value, schema, label="input") -> None:
    """Validate the small declared schema subset without executing schema text."""
    kind = schema["type"]
    if kind == "object":
        if not isinstance(value, dict) or set(value) != set(schema["properties"]):
            raise Invalid(f"{label}: expected exactly the declared fields")
        for key, child in schema["properties"].items():
            shape(value[key], child, f"{label}.{key}")
    elif kind == "array":
        if not isinstance(value, list) or len(value) < schema.get("minItems", 0):
            raise Invalid(f"{label}: expected an array with required entries")
        if len(value) > 256:
            raise Invalid(f"{label}: too many entries")
        for i, item in enumerate(value):
            shape(item, schema["items"], f"{label}[{i}]")
        if schema.get("uniqueItems") and len(value) != len(set(value)):
            raise Invalid(f"{label}: duplicate references or values")
    elif kind == "boolean":
        if type(value) is not bool:
            raise Invalid(f"{label}: expected a boolean")
    elif kind == "string":
        if not isinstance(value, str) or (schema.get("minLength", 0) and not value.strip()):
            raise Invalid(f"{label}: expected nonempty text")
        if len(value) > MAX_SOURCE_BYTES or any(ord(c) < 32 and c not in "\n\r\t" for c in value):
            raise Invalid(f"{label}: text is too large or contains control characters")
        if "enum" in schema and value not in schema["enum"]:
            raise Invalid(f"{label}: unsupported value")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            raise Invalid(f"{label}: malformed identifier or digest")
    else:
        raise Invalid("unsupported contract schema type")


def schemas():
    contract = codec.loads((SKILL_ROOT / "references/discovery.schema.toon").read_text(encoding="utf-8"))
    if contract.get("schema") != "ai-sdlc-requirements-discovery-contract/v1":
        raise Invalid("unsupported packaged discovery contract")
    return contract


def locations(name: str) -> dict[str, str]:
    name = feature(name)
    if PREFIX == "ai-sdlc":
        base = f"specs-refiniment/{name}"
        machine = base + "/_ai_sdlc"
    else:
        base = machine = f".ai-sdlc-loop/{name}"
    result = {kind: f"{machine}/requirements-discovery{suffix}.toon" for kind, suffix in
              (("context", "-context"), ("draft", "-draft"), ("report", ""))}
    if PREFIX == "ai-sdlc":
        result["markdown"] = base + "/requirements-discovery.md"
    return result


def prepare(root: Path, name: str, request: str, paths: list[str], mode: str, request_text=None):
    """Bind stable path-derived source IDs to exact UTF-8 source bytes."""
    owned = set(locations(name).values())
    selected = sorted(set(([request] if request_text is None else []) + paths))
    if len(selected) + (request_text is not None) > MAX_SOURCES:
        raise Invalid(f"select at most {MAX_SOURCES} source files")
    sources, total = [], 0
    if request_text is not None:
        raw = request_text.encode("utf-8")
        if not request_text.strip() or len(raw) > MAX_SOURCE_BYTES:
            raise Invalid("stdin request must be nonempty and within the source byte limit")
        sources.append({"id": "SRC-" + hashlib.sha256(b"snapshot:request").hexdigest()[:12],
                        "kind": "snapshot", "path": "stdin:request", "content": request_text,
                        "sha256": hashlib.sha256(raw).hexdigest()})
        total = len(raw)
    for relative in selected:
        if relative in owned:
            raise Invalid("generated discovery output cannot also be its own source")
        raw = read_bytes(root, relative, MAX_SOURCE_BYTES)
        content = raw.decode("utf-8")
        if not content.strip():
            raise Invalid(f"source is empty: {relative}")
        total += len(raw)
        if total > MAX_TOTAL_BYTES:
            raise Invalid(f"source set exceeds {MAX_TOTAL_BYTES} bytes")
        sources.append({"id": "SRC-" + hashlib.sha256(("file:" + relative).encode("utf-8")).hexdigest()[:12],
                        "kind": "file", "path": relative, "sha256": hashlib.sha256(raw).hexdigest(), "content": content})
    value = {"schema": CONTEXT_SCHEMA, "feature": feature(name), "flow_mode": mode,
             "request_source_id": next(s["id"] for s in sources if s["path"] == (request if request_text is None else "stdin:request")),
             "sources": sources}
    value["fingerprint"] = digest(value)
    shape(value, schemas()["context"], "context")
    return normalize(value)


def check_context(root: Path, value):
    shape(value, schemas()["context"], "context")
    sources = value["sources"]
    if len({s["id"] for s in sources}) != len(sources) or len({s["path"] for s in sources}) != len(sources):
        raise Invalid("context contains duplicate source IDs or paths")
    request = [s for s in sources if s["id"] == value["request_source_id"]]
    if len(request) != 1:
        raise Invalid("context request source is not registered")
    snapshots = [s for s in sources if s["kind"] == "snapshot"]
    if snapshots and (len(snapshots) != 1 or snapshots[0] != request[0] or snapshots[0]["path"] != "stdin:request"):
        raise Invalid("only the raw stdin request may be an embedded snapshot")
    current = prepare(root, value["feature"], request[0]["path"],
                      [s["path"] for s in sources if s["kind"] == "file"], value["flow_mode"],
                      request_text=request[0]["content"] if snapshots else None)
    if encoded(current) != encoded(value):
        raise Invalid("context is stale or tampered; prepare it from current sources")
    return current


def scaffold(context, as_of: str):
    """Emit an intentionally incomplete draft; never fabricate business fields."""
    if date.fromisoformat(as_of).isoformat() != as_of:
        raise Invalid("as-of must use YYYY-MM-DD")
    return {"schema": DRAFT_SCHEMA, "context_fingerprint": context["fingerprint"], "as_of": as_of,
            "problem": {"summary": "", "current_process": "", "actors": [], "desired_outcome": "",
                        "constraints": [], "success_measures": []},
            "evidence_limits": [], "observations": [], "precedents": [], "options": [], "questions": [],
            "recommendation": {"preferred_option_id": "", "criteria": [], "rationale": "",
                               "change_conditions": [], "single_option_reason": "", "next_owner": "",
                               "next_action": "", "expected_evidence": ""},
            "decision": {"status": "awaiting-answers", "selected_option_id": "", "owner": "",
                         "source_ids": [], "decided_at": ""}}


def validate_draft(context, draft):
    shape(draft, schemas()["draft"], "draft")
    if draft["context_fingerprint"] != context["fingerprint"]:
        raise Invalid("draft references a different source context")
    date.fromisoformat(draft["as_of"])
    groups = {}
    for field in ("observations", "precedents", "options", "questions"):
        groups[field] = {item["id"]: item for item in draft[field]}
        if len(groups[field]) != len(draft[field]):
            raise Invalid(f"{field}: duplicate IDs")
    sources = {item["id"] for item in context["sources"]}

    def refs(item, field, allowed):
        if not set(item[field]) <= set(allowed):
            raise Invalid(f"{item.get('id', 'decision')}.{field}: unregistered reference")

    for observation in draft["observations"]:
        refs(observation, "source_ids", sources)
        if observation["kind"] in {"fact", "contradiction"} and not observation["source_ids"]:
            raise Invalid(f"{observation['id']}: sourced claims need source evidence")
    for precedent in draft["precedents"]:
        refs(precedent, "source_ids", sources)
        refs(precedent, "outcome_source_ids", sources)
        if bool(precedent["outcome"].strip()) != bool(precedent["outcome_source_ids"]):
            raise Invalid(f"{precedent['id']}: outcome claims need outcome evidence")
        if precedent["status"] == "outcome-measured" and not precedent["outcome_source_ids"]:
            raise Invalid(f"{precedent['id']}: measured outcomes need evidence")
    candidates = {item["id"] for item in draft["options"] if item["status"] == "candidate"}
    if not candidates:
        raise Invalid("at least one conditional candidate business option is required")
    for option in draft["options"]:
        refs(option, "source_ids", sources)
        refs(option, "precedent_ids", groups["precedents"])
        refs(option, "observation_ids", groups["observations"])
        if option["evidence_kind"] == "sourced" and not (option["source_ids"] or option["precedent_ids"]):
            raise Invalid(f"{option['id']}: sourced option needs evidence")
        if option["status"] == "rejected" and not option["rejection_reason"].strip():
            raise Invalid(f"{option['id']}: rejected option needs a reason")
    covered_observations, covered_options = set(), set()
    for question in draft["questions"]:
        refs(question, "observation_ids", groups["observations"])
        refs(question, "option_ids", groups["options"])
        refs(question, "answer_source_ids", sources)
        answered = question["response_status"] == "answered"
        if answered != bool(question["answer"].strip()) or answered != bool(question["answer_source_ids"]):
            raise Invalid(f"{question['id']}: answered questions need an answer and source evidence")
        covered_observations.update(question["observation_ids"])
        covered_options.update(question["option_ids"])
    material = {o["id"] for o in draft["observations"] if o["material"] and
                o["kind"] in {"assumption", "unknown", "contradiction"}}
    if not material <= covered_observations:
        raise Invalid("material assumptions, gaps or contradictions lack stakeholder questions")
    if not candidates <= covered_options:
        raise Invalid("candidate options lack targeted stakeholder questions")
    recommendation = draft["recommendation"]
    if recommendation["preferred_option_id"] and recommendation["preferred_option_id"] not in candidates:
        raise Invalid("preferred option must reference a candidate")
    if len(candidates) == 1 and not recommendation["single_option_reason"].strip():
        raise Invalid("a single candidate option needs a constraint-based explanation")
    decision = draft["decision"]
    refs(decision, "source_ids", sources)
    if decision["status"] == "accepted":
        if not decision["owner"].strip() or not decision["source_ids"] or decision["selected_option_id"] not in candidates:
            raise Invalid("accepted direction needs owner, candidate option and decision evidence")
        date.fromisoformat(decision["decided_at"])
        if decision["decided_at"] > draft["as_of"]:
            raise Invalid("decision date cannot be later than the packet date")
        if any(q["priority"] == "before-selection" and q["response_status"] == "open" for q in draft["questions"]):
            raise Invalid("accepted direction still has unanswered option-selection questions")
    elif decision["selected_option_id"] or decision["source_ids"] or decision["decided_at"]:
        raise Invalid("unaccepted direction cannot carry an accepted decision record")
    return normalize(draft)


def finalize(context, draft):
    analysis = validate_draft(context, draft)
    report = {"schema": REPORT_SCHEMA, "skill": SKILL, "feature": context["feature"],
              "flow_mode": context["flow_mode"], "packet_status": "complete",
              "decision_status": analysis["decision"]["status"], "context": context,
              "analysis": analysis, "trust": "local-structural-not-authenticated"}
    report["fingerprint"] = digest(report)
    if len(encoded(report)) > MAX_ARTIFACT_BYTES:
        raise Invalid("final report exceeds the artifact byte limit; narrow the analysis")
    return normalize(report)


def verify(root: Path, report):
    if not isinstance(report, dict) or set(report) != {
        "schema", "skill", "feature", "flow_mode", "packet_status", "decision_status",
        "context", "analysis", "trust", "fingerprint",
    }:
        raise Invalid("report must contain exactly the declared fields")
    context = check_context(root, report["context"])
    expected = finalize(context, report["analysis"])
    if encoded(expected) != encoded(report):
        raise Invalid("report identity, fingerprint or content is invalid")
    return expected


def escaped(value: str) -> str:
    value = html.escape(value, quote=False)
    for char in ("\\", "|", "`", "*", "_", "[", "]", "#"):
        value = value.replace(char, "\\" + char)
    return value.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def render_markdown(report) -> bytes:
    """Render every source/analysis field, with untrusted text escaped as data."""
    name, as_of = report["feature"], report["analysis"]["as_of"]
    base = f"specs-refiniment/{name}"
    ids = sorted(item["id"] for field in ("observations", "precedents", "options", "questions")
                 for item in report["analysis"][field])
    lines = ["---", "artifact_metadata:", "  schema: ai-sdlc-artifact-metadata/v1",
             f"  feature: {name}", "  artifact: requirements-discovery.md",
             f"  path: {base}/requirements-discovery.md", "  workspace: refinement",
             f"  skill: {SKILL}", f"  flow_mode: {report['flow_mode']}",
             f"  state_file: {base}/_ai_sdlc/state.toon", f"  decision_log: {base}/decision-log.md",
             "  status: review", "  owner: discovery assistant", f"  created_at: '{as_of}'",
             f"  updated_at: '{as_of}'", "  trace_ids:", *[f"    - {item}" for item in ids],
             f"  related_artifacts: ['{base}/_ai_sdlc/requirements-discovery.toon']",
             "  validation: [structural-check-passed]",
             f"  metatags: [ai-sdlc, refinement, {SKILL}, requirements-discovery, review]",
             "---", "", f"# Requirements discovery: {name}", "",
             "Packet complete means structurally checked; business acceptance and execution authority remain separate.",
             "", f"Decision status: {report['decision_status']}. Local evidence is not authenticated approval.", ""]

    def rows(value, label=""):
        if isinstance(value, dict):
            for key, child in value.items():
                yield from rows(child, f"{label}.{key}" if label else key)
        elif isinstance(value, list):
            if not value:
                yield label, "None recorded"
            for i, child in enumerate(value):
                yield from rows(child, f"{label}[{i + 1}]")
        else:
            yield label, str(value) if value != "" else "Not provided"

    for title, value in [("Sources", report["context"]), ("Analysis", report["analysis"])]:
        lines.extend([f"## {title}", "", "| Field | Value |", "| --- | --- |"])
        lines.extend(f"| {escaped(label)} | {escaped(text)} |" for label, text in rows(value))
        lines.append("")
    lines.extend([f"Report fingerprint: {report['fingerprint']}", ""])
    return "\n".join(lines).encode("utf-8")


def atomic_write_many(root: Path, outputs: dict[str, bytes], replace: bool = False) -> None:
    """Preflight all collisions, stage bytes and restore prior outputs on failure."""
    paths = {relative: safe_path(root, relative) for relative in outputs}
    original, modes, staged, committed = {}, {}, {}, []
    try:
        for relative, path in paths.items():
            if len(outputs[relative]) > MAX_ARTIFACT_BYTES:
                raise Invalid("output exceeds the artifact byte limit; narrow the analysis")
            if path.exists() and not path.is_file():
                raise Invalid(f"output is not a regular file: {relative}")
            old = read_bytes(root, relative, MAX_ARTIFACT_BYTES) if path.exists() else None
            original[relative] = old
            modes[relative] = path.stat().st_mode & 0o777 if old is not None else 0o600
            if old == outputs[relative]:
                continue
            if old is not None and not replace:
                raise Invalid(f"different output exists; review it and use --replace: {relative}")
        for relative, path in paths.items():
            if original[relative] == outputs[relative]:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            fd, temporary = tempfile.mkstemp(prefix=".discovery-", dir=path.parent)
            staged[relative] = Path(temporary)
            with os.fdopen(fd, "wb") as stream:
                os.chmod(temporary, modes[relative])
                stream.write(outputs[relative])
                stream.flush()
                os.fsync(stream.fileno())
        for relative, temporary in staged.items():
            path = safe_path(root, relative)
            current = read_bytes(root, relative, MAX_ARTIFACT_BYTES) if path.exists() else None
            if current != original[relative]:
                raise Invalid("output changed during finalization; retry after review")
            os.replace(temporary, path)
            committed.append(relative)
    except Exception:
        for relative in reversed(committed):
            path = paths[relative]
            if original[relative] is None:
                path.unlink()
            else:
                fd, temporary = tempfile.mkstemp(prefix=".discovery-rollback-", dir=path.parent)
                try:
                    with os.fdopen(fd, "wb") as stream:
                        os.chmod(temporary, modes[relative])
                        stream.write(original[relative])
                    os.replace(temporary, path)
                finally:
                    Path(temporary).unlink(missing_ok=True)
        raise
    finally:
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Pass --root, --quick-flow, --full-flow and --state-check after the command. "
               "Every command rejects --begin-state and --complete-state: discovery owns no lifecycle stage.",
    )
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", type=Path, default=Path.cwd())
    common.add_argument("--quick-flow", action="store_true")
    common.add_argument("--full-flow", action="store_true")
    common.add_argument("--state-check", action="store_true", help="Check that existing state is readable and belongs to this feature; no readiness approval")
    common.add_argument("--begin-state", action="store_true", help="Unsupported: discovery owns no lifecycle stage")
    common.add_argument("--complete-state", action="store_true", help="Unsupported: discovery owns no lifecycle stage")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("prepare", "scaffold", "validate", "finalize", "verify"):
        child = sub.add_parser(command, parents=[common])
        if command == "prepare":
            child.add_argument("--feature", required=True)
            request = child.add_mutually_exclusive_group(required=True)
            request.add_argument("--request", help="Project-relative UTF-8 raw request file")
            request.add_argument("--request-stdin", action="store_true", help="Read a fixed UTF-8 conversation snapshot from stdin")
            child.add_argument("--source", action="append", default=[])
        elif command == "verify":
            child.add_argument("--report", required=True)
        else:
            child.add_argument("--context", required=True)
            if command == "scaffold":
                child.add_argument("--as-of", required=True, help="Explicit YYYY-MM-DD date; no wall-clock default")
            else:
                child.add_argument("--draft", required=True)
        if command in {"prepare", "scaffold", "finalize"}:
            child.add_argument("--write", action="store_true", help="Write only the canonical feature outputs")
            child.add_argument("--replace", action="store_true", help="Replace reviewed differing outputs")
    args = parser.parse_args()
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        root = args.root.resolve(strict=True)
        if not root.is_dir():
            raise Invalid("root must be an existing project directory")
        if args.begin_state or args.complete_state:
            raise Invalid("discovery cannot begin or complete lifecycle state")
        if getattr(args, "replace", False) and not args.write:
            raise Invalid("--replace requires --write")
        mode = "full" if args.full_flow else "quick" if args.quick_flow else "default"
        if args.command == "prepare":
            name = feature(args.feature)
            snapshot = sys.stdin.buffer.read(MAX_SOURCE_BYTES + 1).decode("utf-8") if args.request_stdin else None
            result = prepare(root, args.feature, args.request or "", args.source, mode, request_text=snapshot)
            outputs = {locations(args.feature)["context"]: encoded(result)}
        elif args.command == "verify":
            report = verify(root, load(root, args.report))
            name = report["feature"]
            if mode != "default" and mode != report["flow_mode"]:
                raise Invalid("requested flow differs from the report; rebuild its context")
            if PREFIX == "ai-sdlc":
                relative = locations(report["feature"])["markdown"]
                if read_bytes(root, relative, MAX_ARTIFACT_BYTES) != render_markdown(report):
                    raise Invalid("Markdown projection is missing, stale or tampered")
            result = {"schema": RESULT_SCHEMA, "result": "valid", "fingerprint": report["fingerprint"]}
        else:
            context = check_context(root, load(root, args.context))
            name = context["feature"]
            if mode != "default" and mode != context["flow_mode"]:
                raise Invalid("requested flow differs from the context; prepare it again")
            if args.command == "scaffold":
                result = scaffold(context, args.as_of)
                outputs = {locations(context["feature"])["draft"]: encoded(result)}
            else:
                result = finalize(context, load(root, args.draft))
                if args.command == "validate":
                    result = {"schema": RESULT_SCHEMA, "result": "valid", "fingerprint": result["fingerprint"]}
                else:
                    target = locations(context["feature"])
                    outputs = {target["report"]: encoded(result)}
                    if PREFIX == "ai-sdlc":
                        outputs[target["markdown"]] = render_markdown(result)
        if args.state_check:
            relative = (f"specs-refiniment/{name}/_ai_sdlc/state.toon" if PREFIX == "ai-sdlc"
                        else f".ai-sdlc-loop/{name}/state.toon")
            state = load(root, relative)
            if not isinstance(state, dict) or state.get("feature") != name:
                raise Invalid("existing state belongs to a different feature or is malformed")
        if getattr(args, "write", False):
            atomic_write_many(root, outputs, args.replace)
        sys.stdout.write(encoded(result).decode("utf-8"))
        return 0
    except (OSError, ValueError, codec.ToonDecodeError, RecursionError) as exc:
        sys.stdout.write(encoded({"schema": RESULT_SCHEMA, "result": "invalid", "errors": [str(exc)]}).decode("utf-8"))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
