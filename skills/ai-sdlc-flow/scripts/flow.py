#!/usr/bin/env python3
"""Explore an AI SDLC route and optionally apply one revalidated checkpoint."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import fields
from pathlib import Path


def load_runtime() -> object:
    """Import the canonical source helper or installed runtime mirror."""
    skill_root = Path(__file__).resolve().parents[2]
    candidates = (
        skill_root / "_shared",
        skill_root / "ai-sdlc-shared-runtime" / "scripts",
    )
    for candidate in candidates:
        if (candidate / "ai_sdlc_flow.py").is_file():
            sys.path.insert(0, str(candidate))
            import ai_sdlc_flow

            return ai_sdlc_flow
    raise RuntimeError("ai-sdlc-flow requires ai-sdlc-shared-runtime")


FLOW = load_runtime()


def card_from_json(payload: str) -> object:
    """Parse one complete JSON DecisionCard."""
    values = json.loads(payload)
    economics = FLOW.ContextEconomics(**values.pop("context_economics"))
    allowed = {field.name for field in fields(FLOW.DecisionCard)}
    unknown = sorted(set(values) - allowed)
    if unknown:
        raise ValueError("unknown DecisionCard fields: " + ", ".join(unknown))
    return FLOW.DecisionCard(context_economics=economics, **values)


def current_card(card: object, root: Path) -> object:
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
    return FLOW.build_card(
        root=root,
        intent=card.intent,
        feature=card.feature,
        requested_rigor=card.rigor,
        sources=refreshed_sources,
        project_context=card.project_context,
        economics=card.context_economics,
    )


def state_command(card: object, root: Path) -> list[str]:
    """Return one exact allow-listed lifecycle transition command."""
    allowed = {
        "ai-sdlc-working-backwards-discovery",
        "ai-sdlc-sdd",
        "ai-sdlc-code-review",
        "ai-sdlc-validation",
    }
    if card.skill not in allowed:
        raise ValueError(f"FLOW_UNSUPPORTED_ACTION: {card.skill}")
    helper = root / "skills" / "_shared" / "state_machine.py"
    if not helper.is_file():
        helper = (
            Path(__file__).resolve().parents[2]
            / "ai-sdlc-shared-runtime"
            / "scripts"
            / "state_machine.py"
        )
    return [
        sys.executable,
        str(helper),
        "begin",
        "--feature",
        card.feature,
        "--workspace",
        card.workspace,
        "--skill",
        card.skill,
        "--" + card.rigor + "-flow",
        "--decision-ref",
        "DEC-008",
    ]


def parser() -> argparse.ArgumentParser:
    """Create the CLI parser."""
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--quick-flow", action="store_true", help="Request quick rigor")
    result.add_argument("--full-flow", action="store_true", help="Request full rigor")
    result.add_argument("--state-check", action="store_true", help="Verify state without mutation")
    result.add_argument("--begin-state", action="store_true", help="Mutation-shaped compatibility flag")
    result.add_argument("--complete-state", action="store_true", help="Unsupported completion flag")
    sub = result.add_subparsers(dest="action", required=True)
    explore = sub.add_parser("explore", help="Build a read-only decision card")
    explore.add_argument("--root", type=Path, default=Path.cwd())
    explore.add_argument("--intent", required=True)
    explore.add_argument("--feature", required=True)
    explore.add_argument("--format", choices=("markdown", "toon", "json"), default="markdown")
    modes = explore.add_mutually_exclusive_group()
    modes.add_argument("--quick-flow", action="store_true")
    modes.add_argument("--full-flow", action="store_true")
    explore.add_argument("--state-check", action="store_true", help="Explicit read-only state verification")
    explore.add_argument("--begin-state", action="store_true", help="Unsupported during Explore")
    explore.add_argument("--complete-state", action="store_true", help="Unsupported during Explore")
    explore.add_argument("--raw-tokens", type=int, default=0)
    explore.add_argument("--packed-tokens", type=int, default=0)
    explore.add_argument("--reread-tokens", type=int, default=0)
    explore.add_argument("--critical-total", type=int, default=0)
    explore.add_argument("--critical-retained", type=int, default=0)
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
    apply.add_argument("--card", required=True, help="JSON card path or - for stdin")
    apply.add_argument("--execute", action="store_true", help="Explicitly start the state transition")
    apply.add_argument("--state-check", action="store_true", help="Verify without executing")
    apply.add_argument("--begin-state", action="store_true", help="Alias for explicit --execute")
    apply.add_argument("--complete-state", action="store_true", help="Unsupported: Apply cannot complete stages")
    return result


def main() -> int:
    """Run Explore or Apply."""
    args = parser().parse_args()
    root = args.root.resolve()
    if args.action == "explore":
        if args.begin_state or args.complete_state:
            print("FLOW_READ_ONLY: Explore cannot begin or complete lifecycle state", file=sys.stderr)
            return 2
        rigor = "full" if args.full_flow else "quick" if args.quick_flow else None
        try:
            economics = FLOW.choose_context(
                raw_tokens=args.raw_tokens,
                packed_tokens=args.packed_tokens,
                reread_tokens=args.reread_tokens,
                critical_total=args.critical_total,
                critical_retained=args.critical_retained,
            )
            sources = FLOW.discover_sources(
                root,
                args.feature,
                tuple(root / source for source in args.source),
            )
        except (OSError, ValueError) as exc:
            print(f"FLOW_INVALID_SOURCE: {exc}", file=sys.stderr)
            return 2
        card = FLOW.build_card(
            root=root,
            intent=args.intent,
            feature=args.feature,
            requested_rigor=rigor,
            sources=sources,
            project_context=FLOW.project_context_status(root, args.project_context),
            economics=economics,
        )
        if args.format == "markdown":
            sys.stdout.write(FLOW.render_markdown(card))
        elif args.format == "toon":
            sys.stdout.write(FLOW.render_toon(card))
        else:
            print(json.dumps(FLOW.semantic_dict(card), ensure_ascii=False, sort_keys=True))
        return 1 if card.blockers else 0

    payload = sys.stdin.read() if args.card == "-" else Path(args.card).read_text(encoding="utf-8")
    try:
        accepted = card_from_json(payload)
        rebuilt = current_card(accepted, root)
        if accepted.fingerprint != rebuilt.fingerprint:
            print("FLOW_ROUTE_DRIFT: fingerprint inputs changed; no mutation performed", file=sys.stderr)
            return 2
        if rebuilt.blockers:
            print("; ".join(rebuilt.blockers), file=sys.stderr)
            return 2
        command = state_command(rebuilt, root)
        if args.complete_state:
            print("FLOW_UNSUPPORTED_ACTION: Apply cannot complete lifecycle state", file=sys.stderr)
            return 2
        execute = args.execute or args.begin_state
        if not execute:
            print(json.dumps({"status": "verified", "fingerprint": rebuilt.fingerprint, "action": command}))
            return 0
        completed = subprocess.run(command, cwd=root, check=False, text=True)
        return completed.returncode
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"FLOW_INVALID_CARD: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
