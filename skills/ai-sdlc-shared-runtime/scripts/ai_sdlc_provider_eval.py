#!/usr/bin/env python3
"""Validate genuine provider execution observations into a TOON receipt."""

from __future__ import annotations

import argparse
import copy
import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from ai_sdlc_safe_io import atomic_write_text, bounded_path  # noqa: E402
from ai_sdlc_toon import encode_toon, loads, ToonDecodeError  # noqa: E402

OBSERVATION_SCHEMA = "ai-sdlc-provider-execution/v1"
RECEIPT_SCHEMA = "ai-sdlc-live-eval-receipt/v1"
EVAL_SCHEMA = "ai-sdlc-eval-receipt/v1"
OBSERVATION_FIELDS = {
    "schema", "execution_mode", "protocol_fingerprint", "provider", "host",
    "model", "execution_id", "executed_at", "scenario_version", "agent_attested",
    "scenario_results", "effect_receipts", "recovery_evidence",
}
SCENARIO_FIELDS = {"id", "status", "score", "evidence"}


def digest(value: Any) -> str:
    return hashlib.sha256(encode_toon(value).encode("utf-8")).hexdigest()


def read(path: Path, label: str) -> Any:
    try:
        return loads(path.read_text(encoding="utf-8"))
    except (OSError, ToonDecodeError) as exc:
        raise ValueError(f"cannot read {label}: {exc}") from exc


def strings(value: Any, field: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{field} must be a unique string array")
    if len(value) != len(set(value)):
        raise ValueError(f"{field} must be unique")
    return list(value)


def validate_protocol(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema") != EVAL_SCHEMA or value.get("mode") != "live-protocol":
        raise ValueError("provider evaluation requires an ai-sdlc live-protocol receipt")
    if value.get("result") != "passed" or value.get("failed") != 0:
        raise ValueError("offline protocol validation must pass before provider execution")
    protocol = value.get("protocol")
    if not isinstance(protocol, dict) or not protocol.get("provider_neutral"):
        raise ValueError("live protocol is invalid")
    return copy.deepcopy(value)


def validate_timestamp(value: str) -> None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("provider execution timestamp must be RFC 3339") from exc
    if parsed.tzinfo is None:
        raise ValueError("provider execution timestamp must include an offset")


def receipt(protocol_receipt: Any, observations: Any) -> dict[str, Any]:
    protocol_receipt = validate_protocol(protocol_receipt)
    protocol = protocol_receipt["protocol"]
    expected_protocol = digest(protocol)
    if not isinstance(observations, dict) or set(observations) != OBSERVATION_FIELDS:
        raise ValueError("provider execution observation fields are invalid")
    if observations["schema"] != OBSERVATION_SCHEMA or observations["execution_mode"] != "provider":
        raise ValueError("execution must be explicitly provider mode")
    if observations["protocol_fingerprint"] != expected_protocol:
        raise ValueError("provider observation protocol fingerprint mismatch")
    if observations["scenario_version"] != protocol.get("scenario_version"):
        raise ValueError("provider observation scenario version mismatch")
    identities = ("provider", "host", "model", "execution_id", "executed_at")
    identity_complete = all(isinstance(observations[field], str) and observations[field].strip() for field in identities)
    if observations["agent_attested"] is not True or not identity_complete:
        semantic = {
            "schema": RECEIPT_SCHEMA,
            "protocol_fingerprint": expected_protocol,
            "execution_mode": "offline-or-unattested",
            "provider": str(observations.get("provider", "")),
            "host": str(observations.get("host", "")),
            "model": str(observations.get("model", "")),
            "execution_id": str(observations.get("execution_id", "")),
            "executed_at": str(observations.get("executed_at", "")),
            "scenario_version": str(observations.get("scenario_version", "")),
            "agent_attested": False,
            "status": "pending",
            "scenario_results": [],
            "scores": {},
            "thresholds": copy.deepcopy(protocol["thresholds"]),
            "effect_receipts": [],
            "recovery_evidence": [],
        }
        return {**semantic, "fingerprint": digest(semantic)}
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", observations["execution_id"]):
        raise ValueError("provider execution identity is invalid")
    validate_timestamp(observations["executed_at"])
    effect_receipts = strings(observations["effect_receipts"], "effect_receipts")
    recovery_evidence = strings(observations["recovery_evidence"], "recovery_evidence", nonempty=True)
    expected = {item["id"]: item["criterion"] for item in protocol["scenarios"]}
    thresholds = protocol["thresholds"]
    results = observations["scenario_results"]
    if not isinstance(results, list) or not results:
        raise ValueError("provider scenario_results must be non-empty")
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(results):
        if not isinstance(item, dict) or set(item) != SCENARIO_FIELDS:
            raise ValueError(f"scenario_results[{index}] fields are invalid")
        scenario_id = item["id"]
        if scenario_id not in expected or scenario_id in seen:
            raise ValueError(f"scenario result identity is unknown or duplicate: {scenario_id}")
        seen.add(scenario_id)
        score = item["score"]
        if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 100:
            raise ValueError(f"scenario score is invalid: {scenario_id}")
        evidence = strings(item["evidence"], f"scenario {scenario_id} evidence", nonempty=True)
        passed = score >= thresholds[expected[scenario_id]]
        if item["status"] != ("passed" if passed else "failed"):
            raise ValueError(f"scenario status contradicts score: {scenario_id}")
        normalized.append({"id": scenario_id, "criterion": expected[scenario_id], "status": item["status"], "score": score, "evidence": evidence})
    if seen != set(expected):
        raise ValueError("provider execution does not cover the complete scenario set")
    normalized.sort(key=lambda item: item["id"])
    scores = {item["criterion"]: item["score"] for item in normalized}
    status = "passed" if all(item["status"] == "passed" for item in normalized) else "failed"
    semantic = {
        "schema": RECEIPT_SCHEMA,
        "protocol_fingerprint": expected_protocol,
        "execution_mode": "provider",
        "provider": observations["provider"],
        "host": observations["host"],
        "model": observations["model"],
        "execution_id": observations["execution_id"],
        "executed_at": observations["executed_at"],
        "scenario_version": observations["scenario_version"],
        "agent_attested": True,
        "status": status,
        "scenario_results": normalized,
        "scores": scores,
        "thresholds": copy.deepcopy(thresholds),
        "effect_receipts": effect_receipts,
        "recovery_evidence": recovery_evidence,
    }
    return {**semantic, "fingerprint": digest(semantic)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--observations", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--format", choices=("toon",), default="toon")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    args = parser.parse_args()
    if args.begin_state or args.complete_state:
        parser.error("provider evaluation cannot mutate feature lifecycle state")
    try:
        value = receipt(read(args.protocol, "live protocol"), read(args.observations, "provider observations"))
        content = encode_toon(value)
        if args.output:
            root = args.root.resolve()
            output = args.output if args.output.is_absolute() else root / args.output
            atomic_write_text(root, bounded_path(root, output), content)
        else:
            sys.stdout.write(content)
        return 0 if value["status"] == "passed" else 2
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
