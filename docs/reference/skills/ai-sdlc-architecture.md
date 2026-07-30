---
title: Architecture
description: Human-facing operating guide for ai-sdlc-architecture, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-architecture`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Design and implementation planning | Architecture, Dev | QA, Security, Delivery, BA | `architecture` | `architecture.md` and `_ai_sdlc/architecture.toon` |

## Why it exists

Preserve traceable architecture boundaries, decisions, and risks.

## Use it when

Optional AI SDLC architecture workflow. Use when an AI assistant needs to define system boundaries, components, interfaces, architectural constraints, alternatives, decisions, tradeoffs, risks, or validation for a feature and produce routed human and machine artifacts linked to requirements and durable decisions. Supports `--quick-flow` for focused design and `--full-flow` for strict decision, risk, and validation coverage.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use it while business behavior or customer value is still unclear. Use `ai-sdlc-ba` or the appropriate refinement workflow instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Implementation feature root.
- Architecture input using `ai-sdlc-architecture-input/v1`.
- Requirement, acceptance, risk, or decision trace targets.

## Tell your agent

```text
Use ai-sdlc-architecture for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `architecture.md` and `_ai_sdlc/architecture.toon`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Capture design context and constraints before components.
- Trace interfaces and decisions to durable requirement or decision IDs.
- Give risks an owner and mitigation.
- Provide executable or inspectable validation evidence.

## What it may write

- Write `<feature-root>/architecture.md`.
- Write `<feature-root>/_ai_sdlc/architecture.toon`.
- Keep ADRs or decision-log entries separate when organizational authority
  requires them; link their IDs from architecture decisions.
- Do not write into refinement unless architecture work is explicitly upstream.

## Human checkpoints

- Ask when system boundary, quality attribute, authority, or irreversible choice is ambiguous.
- Separate constraints from decisions and decisions from implementation tasks.
- Record alternatives and consequences for every material decision.
- Do not invent infrastructure, data classification, or production topology.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow permits a bounded architecture slice with explicit gaps.
- Full flow requires at least one decision, risk, and validation check.
- Both modes require trace targets for constraints, interfaces, decisions, and risks.

## Procedural step selectors

The router loads these skill-owned procedures just in time. Read only the selector matching the current phase, active role, and action; a selected step is normative and an unselected step stays out of context.

| Selector | Type | Phases | Roles | Dependencies | Operation | Side effect | Load rule | Step | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `preflight` | `analysis` | `prepare` | `software-architect`, `software-engineer` | none | `inspect-and-route` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-architecture/steps/01-prepare.md) | establish inputs, authority, lifecycle state, and safe artifact routing |
| `context` | `context` | `clarify`, `route` | `software-architect`, `software-engineer` | `preflight` | `compile-context` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-architecture/steps/02-context.md) | compile the minimum sufficient context before the owning action |
| `execute` | `action` | `execute` | `software-architect`, `software-engineer` | `context` | `execute-procedure` | `workspace-write` | `on-demand` | [`steps/02-execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-architecture/steps/02-execute.md) | perform only the selected owning-skill procedure |
| `validate` | `validation` | `validate` | `software-architect`, `software-engineer` | `execute` | `validate-evidence` | `none` | `before-completion` | [`steps/03-validate-and-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-architecture/steps/03-validate-and-handoff.md) | validate outputs, evidence, acceptance, and residual risk |
| `handoff` | `handoff` | `handoff`, `complete` | `software-architect`, `software-engineer` | `validate` | `handoff-result` | `none` | `before-completion` | [`steps/04-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-architecture/steps/04-handoff.md) | return a journal-backed owner and next-action handoff |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`architecture.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-architecture/scripts/architecture.py) | Validate and route traceable architecture artifacts. | `python3 skills/ai-sdlc-architecture/scripts/architecture.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-architecture/scripts/architecture.py specs/payments --input /tmp/architecture.toon --emit --quick-flow
python3 skills/ai-sdlc-architecture/scripts/architecture.py specs/payments --input /tmp/architecture.toon --write --full-flow --format toon
```

## Success criteria

`ai-sdlc-architecture/v1` contains context, constraints, components, interfaces,
decisions, risks, and validation checks with trace targets and owners.

Quality gate:

- Pass when boundaries are explicit and every material claim has traceability.
- Full flow fails without decisions, risks, validation, alternatives, consequences,
  risk ownership, or mitigation.

## Blockers and recovery

- A local reversible patch may use quick flow and record no new decision.
- External systems remain components with explicit unverified interface assumptions.
- Existing ADRs are referenced, not duplicated.
- Diagram generation is optional; structured contracts remain authoritative.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Return design scope, decision/risk counts, blockers, validation status, and
  output paths directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v2` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or untraced diagrams.
- Keep Markdown authoritative for detail and TOON bounded for routing.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read `<feature-root>/_ai_sdlc/state.toon` before architecture work.
    - Architecture is an optional design utility and does not add a core lifecycle stage.
    - `--state-check` is read-only; `--begin-state` and `--complete-state` are rejected.
    - Route accepted design changes back through SDD and change-impact recovery.

??? info "Artifact metadata"

    - Markdown starts with `artifact_metadata` using schema
      `ai-sdlc-architecture-metadata/v1`.
    - Include `metatags` for `ai-sdlc`, `architecture`, `design`, and `traceable`.
    - Record feature, workspace, flow mode, state file, trace IDs, and status.

??? info "Specs index"

    - Read `specs/_ai_sdlc/specs-index.toon` and feature state before broad reads.
    - Refresh `specs/<feature-name>/index.md` only after a durable architecture write.
    - Do not alter `specs-refiniment/_ai_sdlc/specs-index.toon` or
      `specs-refiniment/<feature-name>/index.md` for implementation-owned architecture.

## Example

A valid decision records `DEC-021`, its requirement traces, selected option,
rationale, alternatives, and operational consequences. “Use microservices
because they scale” is invalid without evidence, boundary, alternatives, or tradeoff.

## Source contract

This page is generated from [`skills/ai-sdlc-architecture/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-architecture/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
