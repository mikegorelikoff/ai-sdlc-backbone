---
title: Workflow
description: Human-facing operating guide for ai-sdlc-workflow, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-workflow`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Controlled execution planning | Delivery, Dev | QA, Security, Architecture | `core` | `workflow-plan.toon`, `run-plan.toon`, and `plan.md` below `_ai_sdlc/workflows/<workflow-id>/` |

## Why it exists

Compile portable workflow intent into deterministic, gated skill waves and one immutable runtime plan.

## Use it when

AI SDLC declarative workflow planning. Use when an AI assistant needs to validate a versioned workflow of canonical skill entrypoints, evaluate bounded conditions, enforce explicit approval owners, detect dependency cycles, compile deterministic waves, or produce one runtime-compatible run plan without executing it. Supports `--quick-flow` and `--full-flow`.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use it for a one-off task with no reusable or declared DAG. Use the normal owning skill instead.
- Do not use it to execute an accepted plan. Use `ai-sdlc-runtime` instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Versioned workflow TOON whose nodes name installed skills, canonical
  entrypoints, dependencies, bounded conditions, and approval owners.
- Optional TOON condition context, requested concurrency, and explicit approved
  node IDs.

## Tell your agent

```text
Use ai-sdlc-workflow for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `workflow-plan.toon`, `run-plan.toon`, and `plan.md` below `_ai_sdlc/workflows/<workflow-id>/`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Exact workflow identity and version.
- Canonical skill, entrypoint, role, and action for each node.
- Optional bounded condition context.
- Requested planning concurrency and explicit approved node IDs.

## What it may write

- Write generated plans only below `_ai_sdlc/workflows/<workflow-id>/`.
- Keep authored workflow definitions in visible repository-owned paths.
- Never execute or rewrite the authored workflow during planning.

## Human checkpoints

- Ask when a target skill, entrypoint, action, role, or approval owner is
  materially ambiguous.
- Reject unknown fields, cycles, unsafe identifiers, invalid conditions, and
  missing canonical skill graphs.
- Never infer approval, shell authority, network authority, or host execution.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes use identical validation, cycle, condition, approval, and
  compilation rules.
- Full flow requires review of every skipped, deferred, or blocked node.

## Procedural step selectors

The router loads these skill-owned procedures just in time. Read only the selector matching the current phase, active role, and action; a selected step is normative and an unselected step stays out of context.

| Selector | Type | Phases | Roles | Dependencies | Operation | Side effect | Load rule | Step | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `preflight` | `analysis` | `prepare` | `product-manager`, `software-engineer` | none | `inspect-and-route` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-workflow/steps/01-prepare.md) | establish inputs, authority, lifecycle state, and safe artifact routing |
| `context` | `context` | `clarify`, `route` | `product-manager`, `software-engineer` | `preflight` | `compile-context` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-workflow/steps/02-context.md) | compile the minimum sufficient context before the owning action |
| `execute` | `action` | `execute` | `product-manager`, `software-engineer` | `context` | `execute-procedure` | `workspace-write` | `on-demand` | [`steps/02-execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-workflow/steps/02-execute.md) | perform only the selected owning-skill procedure |
| `validate` | `validation` | `validate` | `product-manager`, `software-engineer` | `execute` | `validate-evidence` | `none` | `before-completion` | [`steps/03-validate-and-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-workflow/steps/03-validate-and-handoff.md) | validate outputs, evidence, acceptance, and residual risk |
| `handoff` | `handoff` | `handoff`, `complete` | `product-manager`, `software-engineer` | `validate` | `handoff-result` | `none` | `before-completion` | [`steps/04-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-workflow/steps/04-handoff.md) | return a journal-backed owner and next-action handoff |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` or `.claude/skills/<skill>/...` path reported by your profile. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`workflow.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-workflow/scripts/workflow.py) | Validate and compile v2 workflows from canonical skill-step graphs. | `python3 skills/ai-sdlc-workflow/scripts/workflow.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.toon --validate --format toon
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.toon --plan --context context.toon --concurrency 4 --approved-node release --write
```

## Success criteria

The plan records every node as eligible, skipped, deferred, or blocked;
selected waves; explicit approvals; derived capabilities and side effects;
source fingerprints; and the embedded runtime plan.

Quality gate:

- Pass when the workflow is acyclic, every referenced skill graph validates,
  conditions are bounded, approval gates are satisfied, and the compiled run
  plan passes runtime validation.
- Fail closed on invalid workflow structure or ambiguous authority.

## Blockers and recovery

- Ask when a target skill, entrypoint, action, role, or approval owner is
  materially ambiguous.
- Reject unknown fields, cycles, unsafe identifiers, invalid conditions, and
  missing canonical skill graphs.
- Never infer approval, shell authority, network authority, or host execution.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Default to complete TOON with workflow fingerprint, node decisions, waves,
  approvals, derived capabilities and side effects, plus the run-plan
  fingerprint.
- Return validation and handoff summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v2` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read the owning feature `_ai_sdlc/state.toon` before planning feature work.
    - Workflow plans do not advance feature state or runtime task state.

??? info "Artifact metadata"

    - Machine records use `ai-sdlc-workflow/v2` and `ai-sdlc-workflow-plan/v2`.
    - Workflow-related Markdown uses canonical `artifact_metadata` and `metatags`
      when authored.

??? info "Specs index"

    - Read `_ai_sdlc/specs-index.toon` before resolving feature-local actions and
      use feature-local `index.md` for human review.
    - Planning does not refresh either specs index.

## Example

```bash
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.toon --validate --format toon
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.toon --plan --context context.toon --concurrency 4 --approved-node release --write
```

## Source contract

This page is generated from [`skills/ai-sdlc-workflow/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-workflow/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
