---
name: ai-sdlc-evidence-council
description: Optional AI SDLC evidence-council workflow. Use when an AI assistant needs to review a high-impact topic through several explicit perspectives, orchestrate simulated lenses or truly independent reviewer executions, and synthesize evidence-backed agreements, conflicts, proposals, owners, and unresolved questions without allowing panel members to rewrite authoritative artifacts. Supports `--quick-flow` for labeled simulated review and `--full-flow` for stricter panel and evidence coverage.
---

# ai-sdlc-evidence-council: Authority-Safe Review Orchestration

> Optional review capability, not required by the core module.
> Every rule below is important to follow. None of it can be skipped.
> A council advises accountable owners; it never becomes approval authority.

## 0. Skill Card

- Skill name: `ai-sdlc-evidence-council`
- Primary audience: Delivery, Architecture, QA, Dev, BA
- Supporting audience: PM, UX, Research, Security
- Audience tags: Delivery, Architecture, QA, Dev, BA, PM
- SDLC stage: Cross-lifecycle high-impact review
- Purpose: Combine multiple evidence perspectives while preserving authority.
- Output: `evidence-council.md` and `_ai_sdlc/evidence-council.toon`

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
- In source use `skills/<skill>/...`; use `.agents/skills/<skill>/...` for
  Codex, `.claude/skills/<skill>/...` for Claude Code, or the project skills
  root recorded in `.ai-sdlc/harness-install.toon` for `agent-project`.
