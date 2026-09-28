#!/usr/bin/env python3
"""Interactive Usage Coach for AI SDLC Loop.

Analyzes local event journals, identifies workflow patterns and friction motifs,
and provides evidence-backed interactive suggestions at the right moment.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

# Ensure shared runtime scripts are in sys.path
_SHARED_HARNESS = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
_SHARED_LOOP = Path(__file__).resolve().parents[2] / "ai-sdlc-loop-shared-runtime" / "scripts"
for _p in (_SHARED_HARNESS, _SHARED_LOOP):
    if _p.is_dir() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

try:
    import usage_journal
    try:
        from ai_sdlc_toon import decode_toon, encode_toon
    except ImportError:
        from toon import decode_toon, encode_toon
except ImportError:
    usage_journal = None  # type: ignore
    decode_toon = None  # type: ignore
    encode_toon = None  # type: ignore


SIGNAL_EXPLANATIONS = {
    "evidence-lag": (
        "Evidence Lag measures the distance (in workflow steps or elapsed time) between "
        "completing code implementation and executing quality or verification gates. "
        "A large evidence lag indicates issues may be caught late rather than immediately."
    ),
    "rework-cycle": (
        "Rework Cycles detect recurring cyclical transitions such as implement -> gate -> implement "
        "or verify -> implement -> verify. High repetition may point to ambiguous requirements, "
        "brittle tests, or lack of local pre-commit checks."
    ),
    "handoff-discoverability": (
        "Handoff Discoverability distinguishes between skills invoked directly by the user versus "
        "skills reached exclusively via handoffs or router selection. It reveals whether capabilities "
        "are easily discoverable."
    ),
    "decision-churn": (
        "Decision Churn identifies requirement or design artifacts that are repeatedly modified "
        "across consecutive steps, indicating potential ambiguity or exploration."
    ),
    "gate-timing": (
        "Gate Timing analyzes when verification and security checks occur relative to implementation. "
        "Earlier timing saves verification and review rework."
    ),
    "capability-gap": (
        "Capability Gap aggregates user manual overrides or blocked statuses where no standard "
        "skill could resolve the bottleneck."
    ),
}


def cmd_report(
    sessions_limit: int = 10,
    window_days: int = 30,
    output_format: str = "text",
    root: Path | None = None,
) -> int:
    """Generate an executive report from local session journals."""
    if not usage_journal:
        sys.stderr.write("Error: usage_journal runtime not available\n")
        return 1

    sessions = usage_journal.scan_sessions(root=root, limit=sessions_limit, since_days=window_days)
    signals = usage_journal.derive_signals(sessions)

    summary = signals.get("summary", {})
    coverage = signals.get("skill_coverage", {})
    transitions = signals.get("transitions", {})
    rework = signals.get("rework_cycles", [])
    evidence_lags = signals.get("evidence_lags", [])
    ignored = signals.get("ignored_recommendations", [])
    gaps = signals.get("capability_gaps", [])

    if output_format == "toon":
        if encode_toon:
            print(encode_toon(signals))
        else:
            print(signals)
        return 0

    print("# AI SDLC Loop Usage & Behavioral Report\n")
    print(f"- Total Scanned Sessions: {summary.get('total_sessions', 0)}")
    print(f"- Total Recorded Events: {summary.get('total_events', 0)}")
    print(f"- Scanned At: {summary.get('scanned_at', 'N/A')}\n")

    print("## 1. Skill Coverage & Invocations")
    if coverage:
        for skill, data in sorted(coverage.items(), key=lambda x: x[1]["count"], reverse=True):
            status_summary = ", ".join(f"{k}:{v}" for k, v in data["statuses"].items() if v > 0)
            print(f"- **{skill}**: {data['count']} invocations (last used: {data['last_used']}) [{status_summary}]")
    else:
        print("No skill invocations recorded in this window.")
    print()

    print("## 2. Common Transitions & Workflow Motifs")
    if transitions:
        for trans, count in sorted(transitions.items(), key=lambda x: x[1], reverse=True)[:8]:
            print(f"- `{trans}`: {count} times")
    else:
        print("No transitions recorded.")
    print()

    print("## 3. Rework & Friction Motifs")
    if rework:
        pattern_counts: dict[str, int] = {}
        for r in rework:
            pat = r.get("pattern", "unknown")
            pattern_counts[pat] = pattern_counts.get(pat, 0) + 1
        for pat, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"- Cycle: `{pat}` (observed {count} times)")
    else:
        print("No significant rework cycles detected.")
    print()

    print("## 4. Evidence Lag & Timing")
    if evidence_lags:
        avg_lag = sum(l.get("steps", 0) for l in evidence_lags) / len(evidence_lags)
        print(f"- Average steps from implementation to verification: {avg_lag:.1f} steps ({len(evidence_lags)} samples)")
    else:
        print("No evidence lag samples recorded.")
    print()

    time_analytics = signals.get("time_analytics", {})
    task_durations = time_analytics.get("task_durations", {})
    skill_durations = time_analytics.get("skill_durations", {})
    rework_time = time_analytics.get("rework_time_loss", {})

    print("## 5. Task & Workflow Time Tracking")
    if task_durations:
        for t_id, t_info in sorted(task_durations.items(), key=lambda x: x[1]["total_ms"], reverse=True):
            skill_parts = []
            for s_name, s_data in t_info.get("skills", {}).items():
                skill_parts.append(f"{s_name}: {s_data.get('formatted', '0s')}")
            skills_str = f" ({', '.join(skill_parts)})" if skill_parts else ""
            print(f"- **Task `{t_id}`**: {t_info.get('formatted_total', '0s')} across {t_info.get('events_count', 0)} events{skills_str}")
    else:
        print("No task durations recorded yet.")
    print()

    print("## 6. Skill Execution Durations")
    if skill_durations:
        for s_name, s_info in sorted(skill_durations.items(), key=lambda x: x[1]["total_ms"], reverse=True):
            print(
                f"- **{s_name}**: total {s_info.get('formatted_total', '0s')} | "
                f"avg {s_info.get('formatted_avg', '0s')} ({s_info.get('count', 0)} runs) | "
                f"min: {usage_journal.format_duration_ms(s_info.get('min_ms'))} / max: {usage_journal.format_duration_ms(s_info.get('max_ms'))}"
            )
    else:
        print("No skill durations recorded yet.")
    print()

    if rework_time.get("total_rework_ms", 0) > 0:
        print(f"## 7. Rework Time Overhead: {rework_time.get('formatted_rework')} spent in {rework_time.get('cycles_count')} rework cycles\n")

    if ignored:
        print(f"## 8. Ignored Recommendations: {len(ignored)} occurrences\n")
    if gaps:
        print(f"## 9. Capability Gaps / Manual Overrides: {len(gaps)} occurrences\n")

    return 0


def cmd_analyze(session_id: str | None = None, root: Path | None = None) -> int:
    """Analyze a single session's event stream in detail."""
    if not usage_journal:
        sys.stderr.write("Error: usage_journal runtime not available\n")
        return 1

    repo_root = root or usage_journal.find_repository_root()
    sid = session_id or usage_journal.get_active_session_id(repo_root)
    sessions = usage_journal.scan_sessions(root=repo_root, session_id=sid)

    if not sessions:
        print(f"No recorded journal found for session: {sid}")
        return 0

    session = sessions[0]
    events = session.get("events", {})
    print(f"# Session Analysis: {sid}\n")
    print(f"- Started: {session.get('started_at', 'N/A')}")
    print(f"- Project: {session.get('project_ref', 'N/A')}")
    print(f"- Version: {session.get('runtime_version', 'N/A')}")
    print(f"- Event Count: {len(events)}\n")

    print("## Event Stream")
    sorted_events = sorted(events.values(), key=lambda x: int(x.get("seq", 0)))
    for ev in sorted_events:
        seq = ev.get("seq", "?")
        ts = ev.get("ts", "")
        etype = ev.get("type", "")
        skill = ev.get("skill", "")
        status = ev.get("status", "")
        dur = ev.get("duration_ms")
        dur_str = f" duration={usage_journal.format_duration_ms(dur)}" if dur is not None else ""
        detail = f" skill={skill}" if skill else ""
        if status:
            detail += f" status={status}"
        print(f"[{seq:03d}] {ts} - {etype}{detail}{dur_str}")

    return 0


def cmd_suggest(
    current_skill: str | None = None,
    task_kind: str | None = None,
    confidence_threshold: float = 0.7,
    session_id: str | None = None,
    root: Path | None = None,
) -> int:
    """Evaluate signals and generate evidence-backed recommendations."""
    if not usage_journal:
        sys.stderr.write("Error: usage_journal runtime not available\n")
        return 1

    repo_root = root or usage_journal.find_repository_root()
    sessions = usage_journal.scan_sessions(root=repo_root, limit=15)
    signals = usage_journal.derive_signals(sessions)

    rework = signals.get("rework_cycles", [])
    evidence_lags = signals.get("evidence_lags", [])
    discoverability = signals.get("discoverability", {})
    coverage = signals.get("skill_coverage", {})

    suggestions: list[dict[str, Any]] = []

    # Rule 1: Recurring rework cycle detection (>= 3 times)
    pattern_counts: dict[str, list[str]] = {}
    for r in rework:
        pat = r.get("pattern", "")
        sid = r.get("session_id", "")
        if pat:
            pattern_counts.setdefault(pat, []).append(sid)

    for pat, sids in pattern_counts.items():
        if len(sids) >= 3:
            s_unique = sorted(list(set(sids)))
            suggestions.append(
                {
                    "id": f"sug-rework-{len(suggestions)+1}",
                    "title": f"Recurring rework cycle detected ({pat})",
                    "observation": f"You repeated transition sequence '{pat}' {len(sids)} times across {len(s_unique)} sessions.",
                    "pattern": "Rework Cycle",
                    "evidence": f"{len(sids)} occurrences in sessions: {', '.join(s_unique[:3])}",
                    "suggestion": "Run engineering quality checks or unit verification in smaller increments before re-implementing.",
                    "alternative": "Continue iterative exploration if refining experimental code.",
                    "value_rationale": "Reduces repetitive validation cycles and catches regressions earlier.",
                    "confidence": 0.85,
                }
            )

    # Rule 2: Evidence lag (average lag > 3 steps)
    if evidence_lags:
        avg_lag = sum(l.get("steps", 0) for l in evidence_lags) / len(evidence_lags)
        if avg_lag >= 3.0:
            suggestions.append(
                {
                    "id": f"sug-lag-{len(suggestions)+1}",
                    "title": "Verification evidence lag between code changes and quality checks",
                    "observation": f"Verification evidence is usually produced {avg_lag:.1f} workflow steps after implementation.",
                    "pattern": "Evidence Lag",
                    "evidence": f"{len(evidence_lags)} verified cycles with average lag of {avg_lag:.1f} steps.",
                    "suggestion": "Invoke ai-sdlc-loop-engineering-quality-gate immediately after implementation changes.",
                    "alternative": "Batch related multi-file edits before running gate if scope spans several components.",
                    "value_rationale": "Prevents late-stage surprises and isolates fault locations quickly.",
                    "confidence": 0.75,
                }
            )

    # Rule 3: Handoff-only discoverability
    for skill, triggers in discoverability.items():
        handoffs = triggers.get("handoff", 0)
        user_invocations = triggers.get("user", 0)
        if handoffs >= 3 and user_invocations == 0:
            suggestions.append(
                {
                    "id": f"sug-disc-{len(suggestions)+1}",
                    "title": f"Skill '{skill}' is relied on via handoffs but rarely invoked directly",
                    "observation": f"Skill '{skill}' was selected {handoffs} times via handoff and 0 times directly by user.",
                    "pattern": "Handoff Discoverability",
                    "evidence": f"{handoffs} handoffs across recent workflows.",
                    "suggestion": f"You can directly invoke '{skill}' for targeted tasks without walking through earlier stages.",
                    "alternative": "Continue using standard upstream entry points.",
                    "value_rationale": "Saves orchestrator turns when the required action is already known.",
                    "confidence": 0.70,
                }
            )

    # Filter by confidence
    filtered = [s for s in suggestions if s["confidence"] >= confidence_threshold]

    if not filtered:
        print("No high-confidence suggestions at this time. Current workflow looks healthy.")
        return 0

    # Emit coach.suggest event to active journal for tracking
    active_sid = session_id or usage_journal.get_active_session_id(repo_root)
    for sug in filtered:
        usage_journal.record_event(
            "coach.suggest",
            {
                "suggestion_id": sug["id"],
                "pattern": sug["pattern"],
                "confidence": sug["confidence"],
            },
            session_id=active_sid,
            root=repo_root,
        )

    print("# AI SDLC Loop Usage Coach Suggestions\n")
    for s in filtered:
        print(f"### Suggestion [{s['id']}]: {s['title']}")
        print(f"- **Observation**: {s['observation']}")
        print(f"- **Pattern**: {s['pattern']}")
        print(f"- **Evidence**: {s['evidence']}")
        print(f"- **Suggestion**: {s['suggestion']}")
        print(f"- **Alternative**: {s['alternative']}")
        print(f"- **Value Rationale**: {s['value_rationale']}")
        print(f"- **Confidence**: {s['confidence']:.2f}\n")

    return 0


def cmd_feedback(
    suggestion_id: str,
    outcome: str,
    notes: str | None = None,
    session_id: str | None = None,
    root: Path | None = None,
) -> int:
    """Record user feedback regarding a recommendation."""
    if not usage_journal:
        sys.stderr.write("Error: usage_journal runtime not available\n")
        return 1

    repo_root = root or usage_journal.find_repository_root()
    active_sid = session_id or usage_journal.get_active_session_id(repo_root)

    usage_journal.record_event(
        "coach.feedback",
        {
            "suggestion_id": suggestion_id,
            "outcome": outcome,
            "notes": notes or "",
        },
        session_id=active_sid,
        root=repo_root,
    )
    print(f"Feedback recorded for suggestion '{suggestion_id}': {outcome}")
    return 0


def cmd_explain(signal_name: str) -> int:
    """Explain a specific behavioral signal or metric."""
    clean_name = signal_name.strip().lower()
    explanation = SIGNAL_EXPLANATIONS.get(clean_name)
    if explanation:
        print(f"## Signal: {clean_name}\n")
        print(explanation)
        return 0

    print(f"Unknown signal: '{signal_name}'. Available signals:")
    for sig in sorted(SIGNAL_EXPLANATIONS.keys()):
        print(f"- {sig}")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="coach.py",
        description="AI SDLC Usage Coach & Behavioral Feedback Assistant",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # report subcommand
    p_report = subparsers.add_parser("report", help="Generate usage & friction report")
    p_report.add_argument("--sessions", type=int, default=10, help="Number of recent sessions to scan")
    p_report.add_argument("--window", type=int, default=30, help="Window in days to scan")
    p_report.add_argument("--format", choices=["text", "toon"], default="text", help="Output format")

    # analyze subcommand
    p_analyze = subparsers.add_parser("analyze", help="Analyze single session event stream")
    p_analyze.add_argument("--session", type=str, default=None, help="Session ID to analyze")

    # suggest subcommand
    p_suggest = subparsers.add_parser("suggest", help="Generate actionable recommendations")
    p_suggest.add_argument("--current-skill", type=str, default=None, help="Active skill")
    p_suggest.add_argument("--task-kind", type=str, default=None, help="Current task kind")
    p_suggest.add_argument("--threshold", type=float, default=0.7, help="Minimum confidence threshold")
    p_suggest.add_argument("--session", type=str, default=None, help="Target session ID")

    # feedback subcommand
    p_feedback = subparsers.add_parser("feedback", help="Record feedback for a suggestion")
    p_feedback.add_argument("--suggestion-id", required=True, help="Suggestion ID")
    p_feedback.add_argument(
        "--outcome",
        required=True,
        choices=["accepted", "rejected", "deferred"],
        help="Feedback outcome",
    )
    p_feedback.add_argument("--notes", type=str, default=None, help="Optional user feedback notes")
    p_feedback.add_argument("--session", type=str, default=None, help="Target session ID")

    # explain subcommand
    p_explain = subparsers.add_parser("explain", help="Explain a behavioral signal or metric")
    p_explain.add_argument("signal", help="Signal name to explain")

    args = parser.parse_args(argv)

    if args.command == "report":
        return cmd_report(sessions_limit=args.sessions, window_days=args.window, output_format=args.format)
    elif args.command == "analyze":
        return cmd_analyze(session_id=args.session)
    elif args.command == "suggest":
        return cmd_suggest(
            current_skill=args.current_skill,
            task_kind=args.task_kind,
            confidence_threshold=args.threshold,
            session_id=args.session,
        )
    elif args.command == "feedback":
        return cmd_feedback(
            suggestion_id=args.suggestion_id,
            outcome=args.outcome,
            notes=args.notes,
            session_id=args.session,
        )
    elif args.command == "explain":
        return cmd_explain(args.signal)

    return 0


if __name__ == "__main__":
    sys.exit(main())
