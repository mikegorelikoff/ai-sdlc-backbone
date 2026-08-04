---
name: ai-sdlc-scheduler
description: Deterministic durable StepCard scheduler. Use when an AI assistant needs to create a scheduled run, claim dependency-ready work with leases, recover expired work, reject stale context or workers, replay scheduler state, or coordinate bounded parallel harness workers.
---

# AI SDLC Scheduler

Use `scripts/scheduler.py` to coordinate validated `ai-sdlc-run-plan/v2` tasks.
Read [scheduler-contract.md](references/scheduler-contract.md) before changing
lease, recovery, event-chain, or compare-and-commit semantics.

## 0. Skill Card

- Skill name: `ai-sdlc-scheduler`
- Primary audience: Dev, Delivery
- Supporting audience: Architecture, QA, Security
- SDLC stage: Durable execution orchestration
- Purpose: Lease, recover, dispatch, replay, and compare-and-commit dependency-ready StepCards.
- Output: Canonical scheduler state, dispatch records, isolated runtime runs, and handoff evidence.

## Workflow

1. Prepare: verify authority, repository boundary, immutable plan, run identity,
   injected clock source, and worker budget.
2. Context: verify each ready StepCard still has the compiled context fingerprint.
3. Execute: create or load state, claim only the first deterministic ready task,
   dispatch it through the runtime, and commit with the matching worker and nonce.
4. Validate: replay the event chain, compare state fingerprints, and test expiry
   recovery before trusting external-effect execution.
5. Handoff: report state path, revision, ready tasks, active leases, terminal
   outcomes, and any blocked dependency.

## Safety rules

- Use canonical TOON input and output only.
- Never infer current time inside deterministic operations; pass `--now`.
- Never dispatch stale context, a foreign lease, or an undeclared effect.
- Treat a revision mismatch as contention evidence; reload instead of overwriting.
- Keep credentials outside plans, state, events, and diagnostics.

## Step Selector

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `prepare` | `prepare` | none | `inspect-scheduler-inputs` | [`steps/01-prepare.md`](steps/01-prepare.md) — `required` |
| `context` | `clarify`, `route` | `prepare` | `validate-step-context` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `execute` | `execute` | `context` | `schedule-one-transition` | [`steps/03-execute.md`](steps/03-execute.md) — `on-demand` |
| `validate` | `validate` | `execute` | `replay-and-validate` | [`steps/04-validate.md`](steps/04-validate.md) — `before-completion` |
| `handoff` | `handoff`, `complete` | `validate` | `handoff-scheduler-state` | [`steps/05-handoff.md`](steps/05-handoff.md) — `before-completion` |

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
