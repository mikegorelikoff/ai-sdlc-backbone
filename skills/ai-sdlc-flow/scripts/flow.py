#!/usr/bin/env python3
"""Explore an AI SDLC route and optionally apply one revalidated checkpoint."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from dataclasses import fields
from pathlib import Path

_TOON_RUNTIME = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if str(_TOON_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_TOON_RUNTIME))
import ai_sdlc_toon as toon_codec  # noqa: E402


def load_runtime() -> object:
    """Import the single canonical installable runtime."""
    skill_root = Path(__file__).resolve().parents[2]
    candidate = skill_root / "ai-sdlc-shared-runtime" / "scripts"
    if not (candidate / "ai_sdlc_flow.py").is_file():
        raise RuntimeError("ai-sdlc-flow requires the installed ai-sdlc-shared-runtime skill")
    sys.path.insert(0, str(candidate))
    import ai_sdlc_flow

    return ai_sdlc_flow


FLOW = load_runtime()


def card_from_toon(payload: str) -> object:
    """Parse one complete TOON DecisionCard."""
    values = toon_codec.loads(payload)
    if values.get("schema") != FLOW.SCHEMA:
        found = values.get("schema", "<missing>")
        raise ValueError(
            f"unsupported DecisionCard schema {found}; run Explore again to regenerate {FLOW.SCHEMA}"
        )
    economics = FLOW.ContextEconomics(**values.pop("context_economics"))
    allowed = {field.name for field in fields(FLOW.DecisionCard)}
    unknown = sorted(set(values) - allowed)
    if unknown:
        raise ValueError("unknown DecisionCard fields: " + ", ".join(unknown))
    return FLOW.DecisionCard(context_economics=economics, **values)


def current_card(
    card: object,
    root: Path,
    team: Path | None = None,
    user: Path | None = None,
) -> object:
    """Rebuild the semantic route from current repository evidence."""
    source_paths: list[Path] = []
    for record in card.sources:
        relative, separator, _digest = record.rpartition(":")
        if not separator:
            raise ValueError(f"malformed source evidence: {record}")
        path = (root / relative).resolve()
        path.relative_to(root)
        source_paths.append(path)
    refreshed_sources = FLOW.discover_sources(root, card.feature, source_paths)
    runtime_root = Path(FLOW.__file__).resolve().parent
    sys.path.insert(0, str(runtime_root))
    import ai_sdlc_config

    layers = []
    config_errors = []
    for path, name in (
        (ai_sdlc_config.packaged_defaults(), "base"),
        (team, "team"),
        (user, "user"),
    ):
        layer, errors = ai_sdlc_config.load_layer(path, name, path is not None)
        layers.append(layer)
        config_errors.extend(errors)
    values, _provenance, errors = ai_sdlc_config.resolve(*layers)
    config_errors.extend(errors)
    config_errors.extend(ai_sdlc_config.validate_interaction(values))
    config_errors.extend(ai_sdlc_config.validate_flow(values))
    if config_errors:
        raise ValueError("; ".join(config_errors))
    return FLOW.build_card(
        root=root,
        intent=card.intent,
        feature=card.feature,
        requested_rigor=card.rigor,
        sources=refreshed_sources,
        project_context=card.project_context,
        requested_role=card.requested_role or None,
        requested_action=card.intent_class if card.intent_class != "ambiguous" else None,
        flow_config=values.get("flow", {}),
    )


def runtime_command(
    root: Path,
    run_id: str,
    plan_path: Path,
) -> list[str]:
    """Return the one exact runtime start command authorized by Apply."""
    helper = root / "skills" / "ai-sdlc-runtime" / "scripts" / "runtime.py"
    if not helper.is_file() or helper.is_symlink():
        helper = (
            Path(__file__).resolve().parents[2]
            / "ai-sdlc-runtime"
            / "scripts"
            / "runtime.py"
        )
    if not helper.is_file() or helper.is_symlink():
        raise ValueError("FLOW_MISSING_RUNTIME: ai-sdlc-runtime is unavailable")
    return [
        sys.executable,
        str(helper),
        str(root),
        "--start",
        "--run-id",
        run_id,
        "--plan",
        str(plan_path),
        "--format",
        "toon",
    ]


def parser() -> argparse.ArgumentParser:
    """Create the CLI parser."""
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--quick-flow", action="store_true", help="Request quick rigor")
    result.add_argument("--full-flow", action="store_true", help="Request full rigor")
    result.add_argument("--state-check", action="store_true", help="Verify state without mutation")
    result.add_argument("--begin-state", action="store_true", help="Mutation-shaped compatibility flag")
    result.add_argument("--complete-state", action="store_true", help="Unsupported completion flag")
    sub = result.add_subparsers(dest="command", required=True)
    explore = sub.add_parser("explore", help="Build a read-only decision card")
    explore.add_argument("--root", type=Path, default=Path.cwd())
    explore.add_argument("--intent", required=True)
    explore.add_argument("--feature", required=True)
    explore.add_argument("--role", help="Explicit canonical role id or configured alias")
    explore.add_argument("--action", help="Explicit stable action id from the deterministic menu")
    explore.add_argument("--team", type=Path, help="Optional team configuration layer")
    explore.add_argument("--user", type=Path, help="Optional user configuration layer")
    explore.add_argument("--format", choices=("markdown", "toon"), default="markdown")
    modes = explore.add_mutually_exclusive_group()
    modes.add_argument("--quick-flow", action="store_true")
    modes.add_argument("--full-flow", action="store_true")
    explore.add_argument("--state-check", action="store_true", help="Explicit read-only state verification")
    explore.add_argument("--begin-state", action="store_true", help="Unsupported during Explore")
    explore.add_argument("--complete-state", action="store_true", help="Unsupported during Explore")
    explore.add_argument(
        "--source",
        type=Path,
        action="append",
        default=[],
        help="Repository-relative evidence file to hash; repeat as needed",
    )
    explore.add_argument(
        "--project-context",
        default="auto",
        help="Project-context freshness label included in the route fingerprint",
    )
    apply = sub.add_parser("apply", help="Revalidate and start one checkpoint")
    apply.add_argument("--root", type=Path, default=Path.cwd())
    apply.add_argument("--card", required=True, help="TOON card path or - for stdin")
    apply.add_argument("--team", type=Path, help="Team configuration used during Explore")
    apply.add_argument("--user", type=Path, help="User configuration used during Explore")
    apply.add_argument("--execute", action="store_true", help="Explicitly start the state transition")
    apply.add_argument("--run-id", default="preview", help="Safe runtime identity used by Apply")
    apply.add_argument("--state-check", action="store_true", help="Verify without executing")
    apply.add_argument("--begin-state", action="store_true", help="Alias for explicit --execute")
    apply.add_argument("--complete-state", action="store_true", help="Unsupported: Apply cannot complete stages")
    return result


def main() -> int:
    """Run Explore or Apply."""
    args = parser().parse_args()
    root = args.root.resolve()
    if args.command == "explore":
        if args.begin_state or args.complete_state:
            print("FLOW_READ_ONLY: Explore cannot begin or complete lifecycle state", file=sys.stderr)
            return 2
        rigor = "full" if args.full_flow else "quick" if args.quick_flow else None
        try:
            runtime_root = Path(FLOW.__file__).resolve().parent
            sys.path.insert(0, str(runtime_root))
            import ai_sdlc_config

            layers = []
            config_errors = []
            for path, name in (
                (ai_sdlc_config.packaged_defaults(), "base"),
                (args.team, "team"),
                (args.user, "user"),
            ):
                layer, errors = ai_sdlc_config.load_layer(path, name, path is not None)
                layers.append(layer)
                config_errors.extend(errors)
            values, _provenance, errors = ai_sdlc_config.resolve(*layers)
            config_errors.extend(errors)
            config_errors.extend(ai_sdlc_config.validate_interaction(values))
            config_errors.extend(ai_sdlc_config.validate_flow(values))
            if config_errors:
                raise ValueError("; ".join(config_errors))
            flow_config = values.get("flow", {})
            sources = FLOW.discover_sources(
                root,
                args.feature,
                tuple(root / source for source in args.source),
            )
        except (OSError, ValueError) as exc:
            print(f"FLOW_INVALID_SOURCE: {exc}", file=sys.stderr)
            return 2
        try:
            card = FLOW.build_card(
                root=root,
                intent=args.intent,
                feature=args.feature,
                requested_rigor=rigor,
                sources=sources,
                project_context=FLOW.project_context_status(
                    root, args.project_context
                ),
                requested_role=args.role,
                requested_action=args.action,
                flow_config=flow_config,
            )
        except (OSError, ValueError, TypeError) as exc:
            print(f"FLOW_INVALID_ROUTE: {exc}", file=sys.stderr)
            return 2
        if args.format == "markdown":
            sys.stdout.write(FLOW.render_markdown(card))
        elif args.format == "toon":
            sys.stdout.write(FLOW.render_toon(card))
        else:
            print(toon_codec.dumps(FLOW.semantic_dict(card), ensure_ascii=False, sort_keys=True))
        return 1 if card.blockers else 0

    payload = sys.stdin.read() if args.card == "-" else Path(args.card).read_text(encoding="utf-8")
    try:
        accepted = card_from_toon(payload)
        rebuilt = current_card(accepted, root, args.team, args.user)
        if accepted.fingerprint != rebuilt.fingerprint:
            print("FLOW_ROUTE_DRIFT: fingerprint inputs changed; no mutation performed", file=sys.stderr)
            return 2
        if rebuilt.blockers:
            print("; ".join(rebuilt.blockers), file=sys.stderr)
            return 2
        if args.complete_state:
            print("FLOW_UNSUPPORTED_ACTION: Apply cannot complete lifecycle state", file=sys.stderr)
            return 2
        execute = args.execute or args.begin_state
        if not execute:
            print(
                toon_codec.encode_toon(
                    {
                        "schema": "ai-sdlc-flow-apply/v3",
                        "status": "verified",
                        "decision_fingerprint": rebuilt.fingerprint,
                        "run_plan_fingerprint": rebuilt.run_plan_fingerprint,
                        "run_id": args.run_id,
                        "planned_tasks": len(rebuilt.run_plan.get("tasks", [])),
                    }
                ),
                end="",
            )
            return 0
        if not rebuilt.run_plan:
            raise ValueError("FLOW_MISSING_RUN_PLAN: Explore did not compile a run")
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-flow-apply-") as temporary:
            plan_path = Path(temporary) / "run-plan.toon"
            plan_path.write_text(
                toon_codec.encode_toon(rebuilt.run_plan),
                encoding="utf-8",
            )
            completed = subprocess.run(
                runtime_command(root, args.run_id, plan_path),
                cwd=root,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        if completed.returncode:
            message = completed.stdout.strip() or completed.stderr.strip()
            print(f"FLOW_RUNTIME_START_FAILED: {message}", file=sys.stderr)
            return 2
        runtime_result = toon_codec.loads(completed.stdout)
        print(
            toon_codec.encode_toon(
                {
                    "schema": "ai-sdlc-flow-apply/v3",
                    "status": "started",
                    "decision_fingerprint": rebuilt.fingerprint,
                    "run_plan_fingerprint": rebuilt.run_plan_fingerprint,
                    "run_id": args.run_id,
                    "runtime_result": runtime_result,
                }
            ),
            end="",
        )
        return 0
    except (OSError, ValueError, TypeError, toon_codec.ToonDecodeError) as exc:
        print(f"FLOW_INVALID_CARD: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
