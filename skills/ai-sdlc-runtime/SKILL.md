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
- Output: `_ai_sdlc/runs/<run-id>/journal.jsonl`, exact `state.json`, and
  complete token-efficient `state.toon`

## Step Selector

Read `steps/manifest.json` and load only the step selected for the current phase, active role, and action. Treat every selected step as normative.

| Selector | Read when | Step | Load rule |
| --- | --- | --- | --- |
| `prepare` | `prepare`, `clarify`, `route` | [`steps/01-prepare.md`](steps/01-prepare.md) | `required` |
| `execute` | `execute` | [`steps/02-execute.md`](steps/02-execute.md) | `on-demand` |
| `validate-and-handoff` | `validate`, `handoff`, `complete` | [`steps/03-validate-and-handoff.md`](steps/03-validate-and-handoff.md) | `before-completion` |

## Progressive Disclosure Contract

- Read the manifest's required entry selector (`prepare`, or `clarify`/`route` for guided flow) before any command, durable write, or lifecycle transition.
- Read an `execute` selector only when performing the selected skill work.
- Read a `validate`, `handoff`, or `complete` selector before reporting completion.
- Do not broad-load unselected steps. If selectors return no match or a validation error, stop and report the blocker.
- Resolve selectors with the canonical `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.
- In a source checkout use `skills/<skill>/...`; in a consumer install use `.agents/skills/<skill>/...`.
