---
name: ai-sdlc-usage-coach
description: Observe real workflow behavior across sessions, identify recurring patterns and friction motifs (rework cycles, evidence lag, handoff discoverability), and provide evidence-backed interactive suggestions at the right moment. Local, repository-native, event-sourced feedback loop without remote telemetry or productivity scoring. Supports report, analyze, suggest, feedback, and explain.
---

# ai-sdlc-usage-coach: Usage Coach & Behavioral Feedback Assistant

Use this skill to observe how the team actually works with the Harness across sessions,
identify recurring workflow patterns and friction, and receive evidence-backed interactive
suggestions at the right moment.

The coach never invents historical behavior from model memory. It derives observations
strictly from the local append-only event journal (`.ai-sdlc/usage/sessions/<date>/<session_id>.toon`)
and existing AI SDLC artifacts.

Use `scripts/coach.py` for report generation, single-session inspection, recommendation derivation,
feedback logging, and signal explanations.

## 0. Skill Card

- Skill name: `ai-sdlc-usage-coach`
- Primary audience: Dev, Tech Lead, Architect
- Supporting audience: PM, QA
- Audience tags: Dev, Tech Lead, Architect, PM, QA
- SDLC stage: Behavioral feedback and continuous workflow improvement
- Purpose: Provide local, event-sourced behavioral feedback and actionable workflow recommendations.
- Output: Structured usage reports, signal derivations, and evidence-backed coaching suggestions.

## Chat Output Contract

Primary: Suggestion ID / Pattern / Evidence / Suggestion / Value rationale; secondary: Signal / Meaning / Impact / Action.
Rows represent actionable recommendations backed by factual session journal events. Show the user observation before recommendation.
Summary: Status / Total Sessions / Key Motif. Failure: Command / Status / Reason / Evidence / Required action.
Clarification: Signal / Unknown context / Options. Next action: Owner / Next action / Expected benefit.
Use PASS, FAIL, WARNING, BLOCKED, PENDING, N/A only for chat statuses; preserve native domain states.
At most six columns, eight preview rows and 180 characters per cell; link full evidence and state omitted totals.
No duplicate prose. Keep code, commands, commit messages and machine handoffs native.
Apply [this skill’s schema and examples](references/chat-output.toon) before any user-facing result, warning or recommendation.
Use the sibling `ai-sdlc-loop-shared-runtime/scripts/chat_output.py` to render/check.

## Deterministic Execution Contract

- D: use [the owning Python entry point](scripts/coach.py) with explicit subcommands (`report`, `analyze`, `suggest`, `feedback`, `explain`); success covers executed checks.
- S: interpret local session journals in `.ai-sdlc/usage/sessions/`; cite exact session IDs, event sequence numbers, and transition counts.
- H: validate advice before handoff. Runtime owns session IDs, sequence numbers, and event records; coaching advice is advisory and grants no execution or bypass authority.
- Read explicit paths; never invent historical events. Fail open: logging issues never interrupt user delivery.

## Step Selector

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `preflight` | `prepare` | none | `inspect-and-route` | [`steps/01-prepare.md`](steps/01-prepare.md) — `required` |
| `context` | `clarify`, `route` | `preflight` | `compile-context` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `execute` | `execute` | `context` | `derive-and-coach` | [`steps/03-coach.md`](steps/03-coach.md) — `on-demand` |
| `validate` | `validate` | `execute` | `validate-evidence` | [`steps/04-validate.md`](steps/04-validate.md) — `before-completion` |
| `handoff` | `handoff`, `complete` | `validate` | `handoff-result` | [`steps/05-handoff.md`](steps/05-handoff.md) — `before-completion` |

## Progressive Disclosure Contract

- Resolve the phase entrypoint and dependency-ready set with
  `skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.
- Read only the emitted StepCard and its selected context. Pass completed step
  IDs back to the selector before requesting the next ready node.
- Treat `direct_read` as an explicit context strategy.
- Explore is read-only. Coach writes only to append-only journals or feedback records.
- In source use `skills/<skill>/...`; use `.agents/skills/<skill>/...` for
  Codex, `.claude/skills/<skill>/...` for Claude Code, or the project skills
  root recorded in `.ai-sdlc/install/<profile>.toon` for `agent-project`.
