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
