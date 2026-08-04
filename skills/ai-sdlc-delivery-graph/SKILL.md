---
name: ai-sdlc-delivery-graph
description: AI SDLC repository delivery-graph and evidence-freshness workflow. Use when an AI assistant needs to index lifecycle traceability, resolve end-to-end paths, report gaps or orphans, register evidence identity, propagate stale dependencies, or calculate fresh evidence coverage. Supports `--quick-flow` for deterministic local analysis and `--full-flow` for strict trace and evidence review.
---

# ai-sdlc-delivery-graph: Repository Traceability

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> The graph is a generated projection; repository artifacts and Git remain authoritative.

## 0. Skill Card

- Skill name: `ai-sdlc-delivery-graph`
- Primary audience: Delivery, Dev, QA, Architecture
- Supporting audience: PM, BA, Security, Release
- Audience tags: Delivery, Dev, QA, Architecture, BA
- SDLC stage: Traceability and readiness
- Purpose: Build a deterministic repository-wide lifecycle graph and answer
  trace, gap, coverage, and orphan questions from stable evidence anchors.
- Output: complete `_ai_sdlc/delivery-graph.toon` for agents, plus
  `_ai_sdlc/delivery-graph.toon` for schema/interoperability and
  `_ai_sdlc/delivery-graph.md` for human review when `--write` is requested

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
