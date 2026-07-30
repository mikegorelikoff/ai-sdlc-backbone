---
name: ai-sdlc-runtime
description: AI SDLC resumable task-runtime workflow. Use when an AI assistant needs to start or resume a versioned delivery run, select dependency-ready work, enforce step, failure, and token budgets, retry safely, persist exact stop reasons, recover state from an append-only journal, or require commit evidence at task boundaries. Supports `--quick-flow` for deterministic local runs and `--full-flow` for strict transition review.
---

# ai-sdlc-runtime: Resumable Delivery Runs

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> The journal is the local structural source for recovery; it is not authenticated evidence. A user with workspace write access can rewrite entries and recompute the SHA-256 chain. Independent assurance requires protected Git history, trusted continuous-integration records, or an external audit log.

## 0. Skill Card

- Skill name: `ai-sdlc-runtime`
- Primary audience: Dev, Delivery
- Supporting audience: QA, Release, Architecture
- Audience tags: Dev, Delivery, QA, Release
- SDLC stage: Controlled execution
- Purpose: Persist task selection and outcomes so interrupted delivery can
  resume without duplicate work or unsupported completion claims.
- Output: immutable `plan.toon`, append-only `journal/*.toon`, and the
  replay-derived `state.toon` projection below `_ai_sdlc/runs/<run-id>/`

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
- In a source checkout use `skills/<skill>/...`; in a project-scoped install
  use `.agents/skills/<skill>/...`.
