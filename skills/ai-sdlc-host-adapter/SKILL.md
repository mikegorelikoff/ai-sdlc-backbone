---
name: ai-sdlc-host-adapter
description: AI SDLC host adapter and capability negotiation workflow. Use when an AI assistant needs to validate a host adapter manifest, map portable workflow operations to host-native operations, negotiate capabilities and limits, select deterministic semantic-preserving fallbacks, or explain why a host cannot run a plan. Supports `--quick-flow` and `--full-flow`.
---

# ai-sdlc-host-adapter: Portable Host Negotiation

> Internal AI SDLC skill, not client-facing by default.
> Negotiation describes host behavior; it never invokes the host.

## 0. Skill Card

- Skill name: `ai-sdlc-host-adapter`
- Primary audience: Dev, Delivery, Architecture
- Supporting audience: Security, QA
- Audience tags: Dev, Delivery, Architecture, Security
- SDLC stage: Portable execution handoff
- Purpose: Preserve workflow semantics across hosts with explicit mappings and safe fallbacks.
- Output: `_ai_sdlc/adapters/<adapter-id>/negotiation.{toon,json,md}`

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
