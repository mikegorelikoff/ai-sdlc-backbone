---
title: Host Adapter
description: Human-facing operating guide for ai-sdlc-host-adapter, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-host-adapter`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Portable execution handoff | Dev, Delivery, Architecture | Security, QA | `core` | `_ai_sdlc/adapters/<adapter-id>/negotiation.toon`, its human projection, and `_ai_sdlc/effects/<idempotency-key>.toon` after execution |

## Why it exists

Preserve workflow semantics across hosts, then execute only bounded negotiated effects with deterministic idempotency.

## Use it when

AI SDLC host adapter negotiation and bounded effect execution workflow. Use when an AI assistant needs to validate a host adapter, map portable StepCard operations, negotiate capabilities, execute a registered workspace or external effect with approval and idempotency, replay an effect receipt, or explain why a host cannot run a plan. Supports `--quick-flow` and `--full-flow`.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use it before a validated workflow declares the host capability it needs. Use `ai-sdlc-workflow` to define that contract instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Versioned adapter manifest and capability request.
- One complete context-ready StepCard, desired concurrency, and isolation need.

## Tell your agent

```text
Use ai-sdlc-host-adapter for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `_ai_sdlc/adapters/<adapter-id>/negotiation.toon`, its human projection, and `_ai_sdlc/effects/<idempotency-key>.toon` after execution, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Versioned adapter manifest and capability request.
- One complete context-ready StepCard, desired concurrency, and isolation need.

## What it may write

- Write negotiations only below `_ai_sdlc/adapters/<adapter-id>/`.
- Keep manifests in repository-owned visible paths or skill conformance fixtures.
- Never mutate a manifest during negotiation.

## Human checkpoints

- Ask when required semantics or host operation identity is ambiguous.
- Reject unknown fields, duplicate operations, invalid API ranges, undeclared
  capabilities, or non-equivalent native mappings.
- Never infer shell, filesystem, network, isolation, concurrency, or approval support.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes use identical compatibility and fallback rules.
- Full flow reviews the StepCard, mapping, derived capability, side-effect,
  evidence, idempotency, limit, fallback, and unsupported-requirement fields.

## Procedural step selectors

The router loads these skill-owned procedures just in time. Read only the selector matching the current phase, active role, and action; a selected step is normative and an unselected step stays out of context.

| Selector | Type | Phases | Roles | Dependencies | Operation | Side effect | Load rule | Step | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `preflight` | `analysis` | `prepare` | `product-manager`, `software-architect`, `software-engineer` | none | `inspect-and-route` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-host-adapter/steps/01-prepare.md) | establish inputs, authority, lifecycle state, and safe artifact routing |
| `context` | `context` | `clarify`, `route` | `product-manager`, `software-architect`, `software-engineer` | `preflight` | `compile-context` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-host-adapter/steps/02-context.md) | compile the minimum sufficient context before the owning action |
| `execute` | `action` | `execute` | `product-manager`, `software-architect`, `software-engineer` | `context` | `execute-procedure` | `workspace-write` | `on-demand` | [`steps/02-execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-host-adapter/steps/02-execute.md) | perform only the selected owning-skill procedure |
| `validate` | `validation` | `validate` | `product-manager`, `software-architect`, `software-engineer` | `execute` | `validate-evidence` | `none` | `before-completion` | [`steps/03-validate-and-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-host-adapter/steps/03-validate-and-handoff.md) | validate outputs, evidence, acceptance, and residual risk |
| `handoff` | `handoff` | `handoff`, `complete` | `product-manager`, `software-architect`, `software-engineer` | `validate` | `handoff-result` | `none` | `before-completion` | [`steps/04-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-host-adapter/steps/04-handoff.md) | return a journal-backed owner and next-action handoff |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` or `.claude/skills/<skill>/...` path reported by your profile. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`adapter.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-host-adapter/scripts/adapter.py) | Validate v2 host adapters and negotiate one canonical StepCard. | `python3 skills/ai-sdlc-host-adapter/scripts/adapter.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`effect_driver.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-host-adapter/scripts/effect_driver.py) | Execute allowlisted host effects with durable idempotent TOON receipts. | `python3 skills/ai-sdlc-host-adapter/scripts/effect_driver.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.toon --validate
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.toon --negotiate --request request.toon --write
python3 skills/ai-sdlc-host-adapter/scripts/effect_driver.py . --negotiation _ai_sdlc/adapters/host/negotiation.toon --request effect-request.toon
```

## Success criteria

The negotiation records StepCard identity, native mapping, unsupported
operation, derived and missing capabilities, side effect, gates, outputs,
idempotency scope, requested and effective limits, fallbacks, compatibility,
reasons, and deterministic fingerprints.

An execution receipt additionally records the registered driver, adapter,
native operation, side-effect class, request fingerprint, idempotency key,
outcome, bounded evidence, and receipt fingerprint without credentials.

Quality gate:

- Pass only when the StepCard operation has an equivalent mapping and every
  derived capability is declared by the adapter.
- Fail closed when host behavior would change workflow semantics.
- For execution, pass only when the receipt belongs to the exact request and an
  identical replay does not invoke the effect again.

## Blockers and recovery

- Ask when required semantics or host operation identity is ambiguous.
- Reject unknown fields, duplicate operations, invalid API ranges, undeclared
  capabilities, or non-equivalent native mappings.
- Never infer shell, filesystem, network, isolation, concurrency, or approval support.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Default to complete TOON with mappings, missing requirements, fallbacks,
  effective limits, compatibility, source fingerprint, and result fingerprint.
- Return summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v2` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read owning feature `_ai_sdlc/state.toon` before execution handoff.
    - Negotiation does not advance feature or runtime state.

??? info "Artifact metadata"

    - Related Markdown uses canonical `artifact_metadata` and `metatags`.
    - Machine records use versioned adapter, request, and negotiation schemas.

??? info "Specs index"

    - Read `_ai_sdlc/specs-index.toon` first and use feature-local `index.md` for human review.
    - Negotiation does not refresh either index.

## Example

```bash
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.toon --validate
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.toon --negotiate --request request.toon --write
python3 skills/ai-sdlc-host-adapter/scripts/effect_driver.py . --negotiation _ai_sdlc/adapters/host/negotiation.toon --request effect-request.toon
```

## Source contract

This page is generated from [`skills/ai-sdlc-host-adapter/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-host-adapter/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
