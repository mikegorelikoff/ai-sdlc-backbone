---
name: ai-sdlc-policy
description: AI SDLC versioned policy-as-code workflow. Use when an AI assistant needs to resolve layered delivery policy, evaluate an action with explainable rules and gates, protect organization minimums from weaker overrides, apply or reject an expiring waiver, or select a reusable assurance profile. Supports `--quick-flow` for deterministic evaluation and `--full-flow` for strict owner and exception review.
---

# ai-sdlc-policy: Explainable Delivery Controls

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Unknown or invalid policy inputs fail closed when they could weaken protection.

## 0. Skill Card

- Skill name: `ai-sdlc-policy`
- Primary audience: Delivery, Security, Architecture, Release
- Supporting audience: Dev, QA, PM, BA
- Audience tags: Delivery, Security, Architecture, Release, Dev
- SDLC stage: Governance and control evaluation
- Purpose: Resolve policy layers with provenance and evaluate actions against
  protected, versioned, waiver-aware rules.
- Output: `_ai_sdlc/policy-resolution.{toon,json}` or fingerprint-addressed TOON/JSON records
  below `_ai_sdlc/policy-decisions/` when `--write` is requested

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
