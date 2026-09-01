---
name: ai-sdlc-engineering-quality-gate
description: AI SDLC post-implementation engineering quality gate. Use after an AI or human implementation when the assistant must inspect the current diff in repository context, compare representative local implementations, review correctness and repository fit adversarially, run deterministic verification, safely fix evidence-backed High and localized Medium findings, rerun checks, and issue a current evidence-based readiness report. Supports `--quick-flow` for bounded focused review and `--full-flow` for stricter trace and verification coverage.
---

# ai-sdlc-engineering-quality-gate: Repository-Grounded Engineering Gate

> Internal AI SDLC skill, not client-facing by default.
> Evaluate whether the implementation is correct for this repository, never in isolation.
> Findings must exist before fixes. Verification claims require executed evidence.

## 0. Skill Card

- Skill name: `ai-sdlc-engineering-quality-gate`
- Primary audience: Dev
- Supporting audience: QA, Architecture, Security
- Audience tags: Dev, QA, Architecture, Security
- SDLC stage: Mandatory post-implementation engineering quality gate
- Purpose: Inspect a bounded implementation against repository evidence, remediate safe material defects, rerun relevant checks, and decide whether the current diff is ready for the next stage.
- Output: Canonical TOON context and quality report plus a concise evidence-based presentation

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
- Read `references/quality-gate-contract.md` before review or mutation. Read the
  schemas before drafting durable TOON; load usage examples only when needed.
- Explore is read-only. After Apply, journal every selected owning-skill step,
  including analysis and validation nodes, before advancing the graph.
- In source use `skills/<skill>/...`; use `.agents/skills/<skill>/...` for
  Codex, `.claude/skills/<skill>/...` for Claude Code, or the project skills
  root recorded in `.ai-sdlc/harness-install.toon` for `agent-project`.
