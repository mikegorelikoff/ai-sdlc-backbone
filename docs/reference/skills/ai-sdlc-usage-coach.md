---
title: Usage Coach
description: Human-facing operating guide for ai-sdlc-usage-coach, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-usage-coach`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Behavioral feedback and continuous workflow improvement | Dev, Tech Lead, Architect | PM, QA | `core` | Structured usage reports, signal derivations, and evidence-backed coaching suggestions. |

## Why it exists

Provide local, event-sourced behavioral feedback and actionable workflow recommendations.

## Use it when

Observe real workflow behavior across sessions, identify recurring patterns and friction motifs (rework cycles, evidence lag, handoff discoverability), and provide evidence-backed interactive suggestions at the right moment. Local, repository-native, event-sourced feedback loop without remote telemetry or productivity scoring. Supports report, analyze, suggest, feedback, and explain.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use behavioral feedback or usage coaching as formal productivity scoring, performance management, or delivery enforcement. Use retrospective and process evaluation instead.
- Do not use it to bypass lifecycle quality gates or commit approval. Use `ai-sdlc-engineering-quality-gate` and `ai-sdlc-commit-prep` instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Active repository root or target project path.
- Local append-only session event journal directory (`.ai-sdlc/usage/sessions/`).
- Optional session identifier or window threshold in days (default: 30 days, 10 sessions).

## Tell your agent

```text
Use ai-sdlc-usage-coach for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report Structured usage reports, signal derivations, and evidence-backed coaching suggestions., preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Active repository root or target project path.
- Local append-only session event journal directory (`.ai-sdlc/usage/sessions/`).
- Optional session identifier or window threshold in days (default: 30 days, 10 sessions).

## What it may write

- Usage events are recorded into append-only local files under `.ai-sdlc/usage/sessions/<date>/<session_id>.toon`.
- Feedback records are appended to `.ai-sdlc/usage/feedback.toon`.
- Read-only coaching reports are presented in chat output without mutating project source code.

## Human checkpoints

- Derive observations strictly from recorded session events; never invent historical actions.
- When no session logs are present, report a clean zero-event status with guidance rather than blocking.
- Present actionable suggestions with evidence, pattern description, and value rationale.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.

## Procedural step selectors

The router loads these skill-owned procedures just in time. Read only the selector matching the current phase, active role, and action; a selected step is normative and an unselected step stays out of context.

| Selector | Type | Phases | Roles | Dependencies | Operation | Side effect | Load rule | Step | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `preflight` | `analysis` | `prepare` | `product-manager`, `software-engineer` | none | `inspect-and-route` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-usage-coach/steps/01-prepare.md) | establish inputs, authority, session identity, and safe journal discovery |
| `context` | `context` | `clarify`, `route` | `product-manager`, `software-engineer` | `preflight` | `compile-context` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-usage-coach/steps/02-context.md) | scan append-only session journals and compile behavioral event context |
| `execute` | `action` | `execute` | `product-manager`, `software-engineer` | `context` | `derive-and-coach` | `none` | `on-demand` | [`steps/03-coach.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-usage-coach/steps/03-coach.md) | derive workflow signals and formulate evidence-backed suggestions |
| `validate` | `validation` | `validate` | `product-manager`, `software-engineer` | `execute` | `validate-evidence` | `none` | `before-completion` | [`steps/04-validate.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-usage-coach/steps/04-validate.md) | validate suggestions against event evidence and enforce non-blocking advice |
| `handoff` | `handoff` | `handoff`, `complete` | `product-manager`, `software-engineer` | `validate` | `handoff-result` | `none` | `before-completion` | [`steps/05-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-usage-coach/steps/05-handoff.md) | return prioritized suggestions and record user feedback into journal |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` or `.claude/skills/<skill>/...` path reported by your profile. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`coach.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-usage-coach/scripts/coach.py) | Interactive Usage Coach for AI SDLC Loop. | `python3 skills/ai-sdlc-usage-coach/scripts/coach.py --help` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage



## Success criteria

A successful result produces Structured usage reports, signal derivations, and evidence-backed coaching suggestions. and satisfies every output rule and blocker check below.

## Blockers and recovery

- Derive observations strictly from recorded session events; never invent historical actions.
- When no session logs are present, report a clean zero-event status with guidance rather than blocking.
- Present actionable suggestions with evidence, pattern description, and value rationale.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Keep output structured with clear summary, coverage, transition motifs, and suggestions.
- Return deterministic findings without remote telemetry or productivity grading.
- Before final response, emit the `ai-sdlc-handoff/v2` contract.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"


??? info "Artifact metadata"


??? info "Specs index"


## Example

### Usage report example

```text

## Source contract

This page is generated from [`skills/ai-sdlc-usage-coach/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-usage-coach/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
