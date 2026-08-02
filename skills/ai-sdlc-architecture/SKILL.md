---
name: ai-sdlc-architecture
description: Optional AI SDLC architecture workflow. Use when an AI assistant needs to define system boundaries, components, interfaces, architectural constraints, alternatives, decisions, tradeoffs, risks, or validation for a feature and produce routed human and machine artifacts linked to requirements and durable decisions. Supports `--quick-flow` for focused design and `--full-flow` for strict decision, risk, and validation coverage.
---

# ai-sdlc-architecture: Traceable System Design

> Optional domain skill, not required by the core module.
> Every rule below is important to follow. None of it can be skipped.
> Architecture artifacts support SDD; they do not replace requirements or ADR authority.

## 0. Skill Card

- Skill name: `ai-sdlc-architecture`
- Primary audience: Architecture, Dev
- Supporting audience: QA, Security, Delivery, BA
- Audience tags: Architecture, Dev, QA, Security
- SDLC stage: Design and implementation planning
- Purpose: Preserve traceable architecture boundaries, decisions, and risks.
- Output: `architecture.md` and `_ai_sdlc/architecture.toon`

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
