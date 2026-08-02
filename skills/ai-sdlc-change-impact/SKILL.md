---
name: ai-sdlc-change-impact
description: AI SDLC change-impact and lifecycle recovery workflow. Use when a requirement, acceptance criterion, decision, API contract, risk assumption, or other traced source changed after downstream artifacts were created and an AI assistant must identify stale artifacts, affected lifecycle stages, and evidence-backed reopen or revalidation actions without silently rewriting authoritative state. Supports `--quick-flow` for focused trace scanning and `--full-flow` for strict state and source-evidence gates.
---

# ai-sdlc-change-impact: Evidence-Backed Lifecycle Recovery

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Analysis proposes recovery actions; the owning lifecycle skill applies them.

## 0. Skill Card

- Skill name: `ai-sdlc-change-impact`
- Primary audience: Delivery, Dev, BA, QA
- Supporting audience: PM, Architecture, Security
- Audience tags: Delivery, Dev, BA, QA
- SDLC stage: Cross-lifecycle change recovery
- Purpose: Trace changed sources to stale artifacts and safe reopen actions.
- Output: `change-impact.md` and `_ai_sdlc/change-impact.toon`

## Step Selector

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `preflight` | `prepare` | none | `inspect-and-route` | [`steps/01-prepare.md`](steps/01-prepare.md) — `required` |
| `context` | `clarify`, `route` | `preflight` | `compile-context` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `execute` | `execute` | `context` | `execute-procedure` | [`steps/02-execute.md`](steps/02-execute.md) — `on-demand` |
| `validate` | `validate` | `execute` | `validate-evidence` | [`steps/03-validate-and-handoff.md`](steps/03-validate-and-handoff.md) — `before-completion` |
| `handoff` | `handoff`, `complete` | `validate` | `handoff-result` | [`steps/04-handoff.md`](steps/04-handoff.md) — `before-completion` |

## Progressive Disclosure Contract

- Resolve the phase entrypoint and dependency-ready set with
  `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.
- Read only the emitted StepCard and its selected context. Pass completed step
  IDs back to the selector before requesting the next ready node.
- Treat `direct_read` as an explicit context strategy. Block only when mandatory
  evidence or critical anchors are missing.
- Explore is read-only. After Apply, journal every selected owning-skill step,
  including analysis and validation nodes, before advancing the graph.
- In a source checkout use `skills/<skill>/...`; in a Codex project install
  use `.agents/skills/<skill>/...`, and in a Claude Code project install use
  `.claude/skills/<skill>/...`.
