---
name: ai-sdlc-shared-runtime
description: Portable AI SDLC shared-helper runtime. Use when an AI assistant installs, verifies, diagnoses, or repairs project-scoped AI SDLC skills whose deterministic scripts depend on shared state, artifact, context, path, TOON, migration, or index modules. This is an installation dependency, not a lifecycle entry point.
---

# ai-sdlc-shared-runtime: Portable Helper Dependency

> Internal AI SDLC dependency, not a client-facing lifecycle skill.
> Do not select it instead of the guided flow or an owning workflow.
> Every installed capability that imports shared helpers must resolve this
> sibling package before it executes.

## 0. Skill Card

- Skill name: `ai-sdlc-shared-runtime`
- Primary audience: agent runners, platform engineers, harness maintainers
- Supporting audience: AI assistants and repository owners diagnosing install failures
- Audience tags: Platform, Maintainer, Dev
- SDLC stage: Installation and cross-lifecycle runtime support
- Purpose: Provide the single deterministic Python runtime used by source checkouts and installed skill sets.
- Output: Read-only runtime verification or an explicit installation blocker

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
