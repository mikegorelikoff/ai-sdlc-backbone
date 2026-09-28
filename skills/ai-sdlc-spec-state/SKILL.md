---
name: ai-sdlc-spec-state
description: Maintain persistent specification state, repository index freshness, baseline specifications, and decision rotation across feature development and multi-repository delivery. Operates against declarative .sdlc.toon configuration.
---

# ai-sdlc-spec-state: Specification State & Lifecycle Management

`ai-sdlc-spec-state` is a reusable, configuration-driven state management primitive. It connects local feature development to a shared specification storage repository (such as `agent-planning-docs` or internal Git mirrors).

The `.sdlc.toon` configuration file is a **declarative policy file** (similar in spirit to `.customization.toon`) that governs how specification state, baselines, decision knowledgebases, and repository indexes are maintained.

## 0. Skill Card

- Skill name: `ai-sdlc-spec-state`
- Primary audience: Software Architect, Software Engineer, Tech Lead
- Supporting audience: BA, PM, PO, QA
- Audience tags: Architect, Dev, Lead, BA, QA
- SDLC stage: Cross-lifecycle specification state persistence and rotation
- Purpose: Keep repository specification context synchronized, compact, fresh, and deterministically accessible for downstream SDD skills without token bloat.
- Output: Synchronized specification context hierarchy (index, baseline, decision archive, incremental specs), published feature artifacts, rotated baselines, and status reports.

## Operations

The skill exposes focused operations:
- `init`: Scaffold a declarative `.sdlc.toon` configuration file.
- `fetch`: Retrieve the compact specification context hierarchy from storage.
- `publish`: Prepare, format, and publish feature artifacts (spec, plan, decisions, readable spec).
- `status`: Display human-readable and machine-readable state metrics and sync health.
- `refresh-index`: Generate or update the compact structural repository index.
- `rotate`: Execute atomic baseline and decision archive rotation when thresholds are reached.
- `cleanup`: Apply configurable retention policies to historical archived artifacts.

## Step Selector

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `preflight` | `prepare` | none | `validate-configuration` | [`steps/01-prepare.md`](steps/01-prepare.md) — `required` |
| `context` | `clarify`, `route` | `preflight` | `fetch-spec-hierarchy` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `execute` | `execute` | `context` | `synchronize-spec-state` | [`steps/03-execute.md`](steps/03-execute.md) — `on-demand` |
| `handoff` | `validate`, `complete` | `execute` | `report-status-and-handoff` | [`steps/04-validate-and-handoff.md`](steps/04-validate-and-handoff.md) — `before-completion` |

## Progressive Disclosure Contract

- Read `.sdlc.toon` for declarative storage and lifecycle rules; never hardcode external repository names or fixed branches.
- Use `scripts/spec_state.py` for all deterministic calculations (age, counts, baseline resolution, Git sync).
- Expose Python library APIs (`fetch_spec_state`, `publish_spec_state`, `status_spec_state`, `check_rotation`) so sibling skills (`ai-sdlc-sdd`, `ai-sdlc-requirements-discovery`, `ai-sdlc-flow`) can consume state programmatically.
