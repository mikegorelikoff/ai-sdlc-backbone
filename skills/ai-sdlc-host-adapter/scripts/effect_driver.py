#!/usr/bin/env python3
"""Execute allowlisted host effects with durable idempotent TOON receipts."""

from __future__ import annotations

import argparse
import copy
import fcntl
import hashlib
import os
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
import ai_sdlc_toon as toon  # noqa: E402

REQUEST_SCHEMA = "ai-sdlc-effect-request/v1"
RECEIPT_SCHEMA = "ai-sdlc-effect-receipt/v1"
NEGOTIATION_SCHEMA = "ai-sdlc-capability-negotiation/v2"
REQUEST_FIELDS = {
    "schema", "driver", "adapter_id", "negotiation_fingerprint",
    "step_fingerprint", "context_fingerprint", "operation", "side_effect",
    "capabilities", "approval_ref", "arguments", "idempotency_key",
}
DRIVERS = {"workspace.write-text", "external.toon-post"}
HASH = re.compile(r"^[a-f0-9]{64}$")
SENSITIVE = re.compile(r"(?:authorization|cookie|credential|password|private[_-]?key|secret|token)", re.I)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Reject redirects so an allowlisted host cannot redirect the effect."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def digest(value: Any) -> str:
    text = value if isinstance(value, str) else toon.encode_toon(value)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read(path: Path, label: str) -> Any:
    try:
        return toon.loads(path.read_text(encoding="utf-8"))
    except (OSError, toon.ToonDecodeError) as exc:
        raise ValueError(f"cannot read {label}: {exc}") from exc


def atomic_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(toon.encode_toon(value))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def exclusive(path: Path) -> Iterator[None]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def contains_sensitive_key(value: Any) -> bool:
    if isinstance(value, dict):
        return any(SENSITIVE.search(str(key)) or contains_sensitive_key(item) for key, item in value.items())
    if isinstance(value, list):
        return any(contains_sensitive_key(item) for item in value)
    return False


def semantic_request(request: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(request)
    value.pop("idempotency_key", None)
    return value


def validate_request(request: Any, negotiation: Any) -> dict[str, Any]:
    if not isinstance(request, dict) or set(request) != REQUEST_FIELDS:
        raise ValueError("effect request fields are invalid")
    if request["schema"] != REQUEST_SCHEMA:
        raise ValueError(f"effect request schema must be {REQUEST_SCHEMA}")
    if request["driver"] not in DRIVERS:
        raise ValueError("effect driver is not registered")
    for field in ("negotiation_fingerprint", "step_fingerprint", "context_fingerprint", "idempotency_key"):
        if not isinstance(request[field], str) or not HASH.fullmatch(request[field]):
            raise ValueError(f"effect request {field} is invalid")
    if not isinstance(negotiation, dict) or negotiation.get("schema") != NEGOTIATION_SCHEMA:
        raise ValueError("effect execution requires a v2 negotiation")
    if not negotiation.get("compatible"):
        raise ValueError("incompatible negotiation cannot execute")
    if request["negotiation_fingerprint"] != negotiation.get("fingerprint"):
        raise ValueError("negotiation fingerprint mismatch")
    if request["adapter_id"] != negotiation.get("adapter", {}).get("id"):
        raise ValueError("adapter identity mismatch")
    if request["step_fingerprint"] != negotiation.get("step", {}).get("step_fingerprint"):
        raise ValueError("step fingerprint mismatch")
    if request["side_effect"] != negotiation.get("side_effect"):
        raise ValueError("side-effect class mismatch")
    if request["operation"] != negotiation.get("mapping", {}).get("host_operation"):
        raise ValueError("host operation was not negotiated")
    if not isinstance(request["capabilities"], list) or sorted(request["capabilities"]) != sorted(negotiation.get("required_capabilities", [])):
        raise ValueError("effect capabilities differ from negotiation")
    if request["side_effect"] in {"external-write", "destructive"} and not request["approval_ref"]:
        raise ValueError("external or destructive effect requires approval evidence")
    if not isinstance(request["arguments"], dict) or contains_sensitive_key(request["arguments"]):
        raise ValueError("effect arguments are invalid or contain secret-bearing keys")
    if request["idempotency_key"] != digest(semantic_request(request)):
        raise ValueError("effect idempotency key mismatch")
    return copy.deepcopy(request)


def confined(root: Path, relative: Any) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError("effect path must be a non-empty repository-relative path")
    candidate = root / relative
    if any(part in {"", ".", ".."} for part in Path(relative).parts):
        raise ValueError("effect path contains traversal")
    resolved_root = root.resolve()
    resolved_parent = candidate.parent.resolve()
    if resolved_parent != resolved_root and resolved_root not in resolved_parent.parents:
        raise ValueError("effect path escapes repository")
    cursor = root
    linked_component = root.is_symlink()
    for part in Path(relative).parts[:-1]:
        cursor = cursor / part
        linked_component = linked_component or cursor.is_symlink()
    if candidate.is_symlink() or linked_component:
        raise ValueError("effect path contains a symlink")
    return candidate


def workspace_write(root: Path, arguments: dict[str, Any]) -> dict[str, Any]:
    if set(arguments) != {"path", "content", "expected_sha256"}:
        raise ValueError("workspace.write-text arguments are invalid")
    if not isinstance(arguments["content"], str):
        raise ValueError("workspace.write-text content must be text")
    path = confined(root, arguments["path"])
    expected = arguments["expected_sha256"]
    if expected and (not isinstance(expected, str) or not HASH.fullmatch(expected)):
        raise ValueError("expected_sha256 must be empty or a SHA-256 value")
    current = digest(path.read_text(encoding="utf-8")) if path.is_file() else ""
    if current != expected:
        raise ValueError("workspace precondition fingerprint mismatch")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(arguments["content"])
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return {"path": str(path.relative_to(root)), "sha256": digest(arguments["content"]), "status_code": 0}


def external_toon_post(arguments: dict[str, Any], key: str) -> dict[str, Any]:
    if set(arguments) != {"url", "allowed_hosts", "payload", "timeout_seconds"}:
        raise ValueError("external.toon-post arguments are invalid")
    parsed = urllib.parse.urlsplit(str(arguments["url"]))
    allowed = arguments["allowed_hosts"]
    timeout = arguments["timeout_seconds"]
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
        raise ValueError("external URL must be credential-free HTTPS")
    if not isinstance(allowed, list) or parsed.hostname not in allowed or len(allowed) != len(set(allowed)):
        raise ValueError("external host is not allowlisted")
    if not isinstance(timeout, int) or isinstance(timeout, bool) or not 1 <= timeout <= 30:
        raise ValueError("external timeout must be 1..30 seconds")
    body = toon.encode_toon(arguments["payload"]).encode("utf-8")
    request = urllib.request.Request(
        arguments["url"], data=body, method="POST",
        headers={"Content-Type": "application/toon", "Idempotency-Key": key},
    )
    try:
        opener = urllib.request.build_opener(NoRedirect())
        with opener.open(request, timeout=timeout) as response:
            response_body = response.read(1_048_577)
            if len(response_body) > 1_048_576:
                raise ValueError("external response exceeds one MiB")
            if not 200 <= response.status < 300:
                raise ValueError(f"external effect returned status {response.status}")
            return {"path": "", "sha256": hashlib.sha256(response_body).hexdigest(), "status_code": response.status}
    except urllib.error.URLError as exc:
        raise ValueError(f"external effect transport failed: {exc.reason}") from exc


def execute(root: Path, request: dict[str, Any], negotiation: dict[str, Any]) -> dict[str, Any]:
    validated = validate_request(request, negotiation)
    key = validated["idempotency_key"]
    receipt_path = root / "_ai_sdlc" / "effects" / f"{key}.toon"
    with exclusive(receipt_path.with_suffix(".lock")):
        if receipt_path.exists():
            receipt = read(receipt_path, "effect receipt")
            if receipt.get("request_fingerprint") != digest(validated):
                raise ValueError("idempotency receipt belongs to a different request")
            return receipt
        if validated["driver"] == "workspace.write-text":
            evidence = workspace_write(root, validated["arguments"])
        else:
            evidence = external_toon_post(validated["arguments"], key)
        semantic = {
            "schema": RECEIPT_SCHEMA,
            "driver": validated["driver"],
            "adapter_id": validated["adapter_id"],
            "operation": validated["operation"],
            "side_effect": validated["side_effect"],
            "idempotency_key": key,
            "request_fingerprint": digest(validated),
            "outcome": "succeeded",
            "evidence": evidence,
        }
        receipt = {**semantic, "fingerprint": digest(semantic)}
        atomic_write(receipt_path, receipt)
        return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--negotiation", type=Path, required=True)
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    args = parser.parse_args()
    if args.begin_state or args.complete_state:
        print("ERROR: effect execution cannot mutate feature lifecycle state", file=sys.stderr)
        return 1
    try:
        repository = args.repository.resolve(strict=True)
        receipt = execute(repository, read(args.request, "effect request"), read(args.negotiation, "negotiation"))
        sys.stdout.write(toon.encode_toon(receipt))
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
