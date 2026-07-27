---
name: ai-sdlc-flow
description: Guided AI SDLC Explore then Apply workflow. Use when a contributor needs one readable entrypoint that classifies intent before feature selection, explains context, rigor, roles, workspaces, blockers, and planned writes, then revalidates and starts exactly one lifecycle checkpoint.
---

# ai-sdlc-flow: Guided Explore and Apply

> Internal AI SDLC skill and the recommended repository workflow entrypoint.
> Explore is always read-only. Apply never broadens user, sandbox, policy, or
> owning-skill authority.

## 0. Skill Card

- Skill name: `ai-sdlc-flow`
- Primary audience: Contributor, Dev
- Supporting audience: Product, BA, QA, Engineering, Security, Operations
- Audience tags: Contributor, Dev, Product, BA, QA, Security, Operations
- SDLC stage: Cross-lifecycle guided entry
- Purpose: Replace skill-order guesswork with one auditable Explore decision card and one fingerprinted Apply checkpoint.
- Output: `ai-sdlc-flow/v2` Markdown, TOON, or JSON decision card and one bounded Apply result

## Step Selector

Read `steps/manifest.json` and load only the step selected for the current phase, active role, and action. Treat every selected step as normative.

| Selector | Read when | Step | Load rule |
| --- | --- | --- | --- |
| `clarify` | `clarify` | [`steps/clarify.md`](steps/clarify.md) | `required` |
| `route` | `route` | [`steps/route.md`](steps/route.md) | `required` |
| `execute` | `execute` | [`steps/execute.md`](steps/execute.md) | `on-demand` |
| `handoff` | `handoff` | [`steps/handoff.md`](steps/handoff.md) | `on-demand` |
| `validate` | `validate` | [`steps/validate.md`](steps/validate.md) | `before-completion` |
| `complete` | `complete` | [`steps/complete.md`](steps/complete.md) | `before-completion` |

## Progressive Disclosure Contract

- Read the manifest's required entry selector (`prepare`, or `clarify`/`route` for guided flow) before any command, durable write, or lifecycle transition.
- Read an `execute` selector only when performing the selected skill work.
- Read a `validate`, `handoff`, or `complete` selector before reporting completion.
- Do not broad-load unselected steps. If selectors return no match or a validation error, stop and report the blocker.
- Resolve selectors with the canonical `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.
- In a source checkout use `skills/<skill>/...`; in a consumer install use `.agents/skills/<skill>/...`.
