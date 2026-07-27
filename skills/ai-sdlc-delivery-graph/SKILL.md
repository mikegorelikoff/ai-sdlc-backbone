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
  `_ai_sdlc/delivery-graph.json` for schema/interoperability and
  `_ai_sdlc/delivery-graph.md` for human review when `--write` is requested

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
