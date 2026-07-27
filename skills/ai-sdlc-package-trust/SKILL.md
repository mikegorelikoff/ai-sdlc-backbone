---
name: ai-sdlc-package-trust
description: AI SDLC package trust and privacy-preserving local metrics workflow. Use when an AI assistant needs to verify package origin, file integrity, harness compatibility, declared capabilities, provenance evidence, or generate reproducible aggregate run, retry, budget, coverage, and freshness metrics without collecting source, prompts, commands, or diffs. Supports `--quick-flow` and `--full-flow`.
---

# ai-sdlc-package-trust: Trusted Packages And Private Metrics

> Internal AI SDLC skill, not client-facing by default.
> Integrity and provenance evidence do not grant install or execution authority.

## 0. Skill Card

- Skill name: `ai-sdlc-package-trust`
- Primary audience: Security, Delivery, Release
- Supporting audience: Dev, Architecture
- Audience tags: Security, Delivery, Release, Dev
- SDLC stage: Package trust and local observability
- Purpose: Fail closed on untrusted packages and measure delivery without content collection.
- Output: `_ai_sdlc/trust/<package-id>/decision.{toon,json,md}` or `_ai_sdlc/metrics/local.{toon,json,md}`

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
