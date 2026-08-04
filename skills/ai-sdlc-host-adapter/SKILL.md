---
name: ai-sdlc-host-adapter
description: AI SDLC host adapter negotiation and bounded effect execution workflow. Use when an AI assistant needs to validate a host adapter, map portable StepCard operations, negotiate capabilities, execute a registered workspace or external effect with approval and idempotency, replay an effect receipt, or explain why a host cannot run a plan. Supports `--quick-flow` and `--full-flow`.
---

# ai-sdlc-host-adapter: Portable Host Negotiation

> Internal AI SDLC skill, not client-facing by default.
> Negotiate first. Execute only an approved registered driver whose request is
> bound to that negotiation and whose durable receipt prevents duplicate effects.

## 0. Skill Card

- Skill name: `ai-sdlc-host-adapter`
- Primary audience: Dev, Delivery, Architecture
- Supporting audience: Security, QA
- Audience tags: Dev, Delivery, Architecture, Security
- SDLC stage: Portable execution handoff
- Purpose: Preserve workflow semantics across hosts, then execute only bounded
  negotiated effects with deterministic idempotency.
- Output: `_ai_sdlc/adapters/<adapter-id>/negotiation.toon`, its human
  projection, and `_ai_sdlc/effects/<idempotency-key>.toon` after execution

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
