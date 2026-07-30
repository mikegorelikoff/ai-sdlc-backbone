---
title: Change Impact
description: Human-facing operating guide for ai-sdlc-change-impact, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-change-impact`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Cross-lifecycle change recovery | Delivery, Dev, BA, QA | PM, Architecture, Security | `core` | `change-impact.md` and `_ai_sdlc/change-impact.toon` |

## Why it exists

Trace changed sources to stale artifacts and safe reopen actions.

## Use it when

AI SDLC change-impact and lifecycle recovery workflow. Use when a requirement, acceptance criterion, decision, API contract, risk assumption, or other traced source changed after downstream artifacts were created and an AI assistant must identify stale artifacts, affected lifecycle stages, and evidence-backed reopen or revalidation actions without silently rewriting authoritative state. Supports `--quick-flow` for focused trace scanning and `--full-flow` for strict state and source-evidence gates.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use it for an unaccepted proposal that has no baseline change set. Use `ai-sdlc-change-set` instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Feature root in `specs/` or `specs-refiniment/`.
- A TOON change set with stable changed references and exact source evidence.
- Readable feature artifacts and, in full flow, canonical lifecycle state.

## Tell your agent

```text
Use ai-sdlc-change-impact for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `change-impact.md` and `_ai_sdlc/change-impact.toon`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Use repository-relative source evidence with a positive line number.
- Use stable trace IDs already present in source and downstream artifacts.
- Read state status and artifact ownership from canonical repository records.
- Exclude generated change-impact reports from their own analysis.

## What it may write

- Write human analysis to `<feature-root>/change-impact.md`.
- Write machine analysis to `<feature-root>/_ai_sdlc/change-impact.toon`.
- Never overwrite the changed source, downstream artifacts, or state.
- Route approved actions through the owning lifecycle skill.

## Human checkpoints

- Ask only when the feature, changed reference, or source evidence is ambiguous.
- Do not infer that an artifact is stale without an exact trace occurrence.
- Report missing state or unowned artifacts as blockers, not guessed stages.
- Preserve multiple changes independently even when they affect one artifact.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow scans feature Markdown and reports missing state as a blocker.
- Full flow requires canonical state plus valid changed-reference source lines.
- Neither mode changes state, artifacts, decisions, tasks, or indexes.

## Procedural step selectors

The router loads these skill-owned procedures just in time. Read only the selector matching the current phase, active role, and action; a selected step is normative and an unselected step stays out of context.

| Selector | Type | Phases | Roles | Dependencies | Operation | Side effect | Load rule | Step | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `preflight` | `analysis` | `prepare` | `business-analyst`, `product-manager`, `qa-engineer`, `software-engineer` | none | `inspect-and-route` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-impact/steps/01-prepare.md) | establish inputs, authority, lifecycle state, and safe artifact routing |
| `context` | `context` | `clarify`, `route` | `business-analyst`, `product-manager`, `qa-engineer`, `software-engineer` | `preflight` | `compile-context` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-impact/steps/02-context.md) | compile the minimum sufficient context before the owning action |
| `execute` | `action` | `execute` | `business-analyst`, `product-manager`, `qa-engineer`, `software-engineer` | `context` | `execute-procedure` | `workspace-write` | `on-demand` | [`steps/02-execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-impact/steps/02-execute.md) | perform only the selected owning-skill procedure |
| `validate` | `validation` | `validate` | `business-analyst`, `product-manager`, `qa-engineer`, `software-engineer` | `execute` | `validate-evidence` | `none` | `before-completion` | [`steps/03-validate-and-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-impact/steps/03-validate-and-handoff.md) | validate outputs, evidence, acceptance, and residual risk |
| `handoff` | `handoff` | `handoff`, `complete` | `business-analyst`, `product-manager`, `qa-engineer`, `software-engineer` | `validate` | `handoff-result` | `none` | `before-completion` | [`steps/04-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-impact/steps/04-handoff.md) | return a journal-backed owner and next-action handoff |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`change_impact.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-impact/scripts/change_impact.py) | Trace changed references to stale artifacts and safe recovery actions. | `python3 skills/ai-sdlc-change-impact/scripts/change_impact.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-change-impact/scripts/change_impact.py specs/payments --changes /tmp/changes.toon --emit --quick-flow
python3 skills/ai-sdlc-change-impact/scripts/change_impact.py specs/payments --changes /tmp/changes.toon --write --full-flow --format toon
python3 skills/ai-sdlc-change-impact/scripts/change_impact.py specs/payments --changes /tmp/changes.toon --state-check --format toon
```

The change set is read-only input. `--write` atomically creates both report
formats after all evidence gates pass.

## Success criteria

The TOON schema `ai-sdlc-change-impact/v1` contains changes, affected artifacts,
stage status, blockers, and actions with `stage`, `skill`, `action`, `reason`,
`evidence_path`, `evidence_line`, `changed_ref`, and `expected_artifact`.

Quality gate:

- Pass when every change has valid source evidence and every impact/action is
  backed by an exact downstream trace occurrence.
- Full flow fails when state is absent, source evidence is invalid, or an
  affected artifact cannot be mapped to a lifecycle owner.

## Blockers and recovery

- A valid change with no downstream occurrence reports no stale artifact and
  recommends targeted trace review rather than broad reopening.
- Multiple occurrences in one artifact are collapsed into one affected row per
  changed reference using the earliest exact line as evidence.
- Unknown artifact owners block full flow but remain visible in quick flow.
- Already active stages are revalidated, never reopened concurrently.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Return changed refs, stale artifacts, affected stages, blockers, and ordered
  reopen actions directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v2` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or ad hoc recovery files.
- Every affected artifact and reopen action must retain exact evidence.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read `<feature-root>/_ai_sdlc/state.toon` before proposing stage actions.
    - `--state-check` validates read-only state availability.
    - `--begin-state` and `--complete-state` are rejected because analysis cannot
      authorize reopening.
    - A `reopen` proposal applies only to a stage currently in a complete state;
      active and not-started stages receive revalidation or pre-start gates.
    - The owning workflow records accepted recovery in state and decision log.

??? info "Artifact metadata"

    - Markdown starts with `artifact_metadata` using schema
      `ai-sdlc-change-impact-metadata/v1`.
    - Include `metatags` for `ai-sdlc`, `change-impact`, `recovery`, and the affected
      stage identifiers.
    - Record feature, workspace, changed refs, state file, and flow mode.

??? info "Specs index"

    - Read `specs/_ai_sdlc/specs-index.toon` or
      `specs-refiniment/_ai_sdlc/specs-index.toon` before feature analysis.
    - Do not refresh `specs/<feature-name>/index.md` or
      `specs-refiniment/<feature-name>/index.md` during read-only analysis.
    - The owning workflow refreshes indexes only after an accepted state or
      authoritative artifact change.

## Example

Valid change:

```toon
changed_ref: AC-004
id: CHG-001
source:
  detail: Retry behavior changed from optional to required.
  line: 121
  path: requirements.md
```

Invalid counter-example: `The requirements changed recently.` It cannot prove
which durable source changed or which downstream artifacts are stale.

## Source contract

This page is generated from [`skills/ai-sdlc-change-impact/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-impact/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
