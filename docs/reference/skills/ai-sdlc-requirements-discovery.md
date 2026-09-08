---
title: Requirements Discovery
description: Human-facing operating guide for ai-sdlc-requirements-discovery, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-requirements-discovery`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Requirements discovery before specification | BA | PM, PO, Dev, QA | `core` | Source-bound context, validated TOON discovery packet, business options, stakeholder questions, and conditional handoff |

## Why it exists

Turn raw feature or task inputs into a sourced problem analysis, business options, and an actionable stakeholder elicitation plan.

## Use it when

Analyze raw feature or task requirements, compare business solution options using relevant precedents, and prepare prioritized stakeholder questions with evidence-gathering methods. Use before detailed specification when the request or business approach is still unclear. Supports --quick-flow and --full-flow.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not repeat discovery when the business direction is accepted and only actors, rules or acceptance logic need detail. Use `ai-sdlc-ba` instead.
- Do not use a discovery packet as implementation approval or a readiness verdict. Use the appropriate requirements review and `ai-sdlc-sdd` instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Raw request, notes, feedback or a source locator. Ask for the actual request if
  none is available; do not invent it from the skill invocation alone.
- Identify product, actors, desired outcome and constraints from available
  context. Missing details are discovery questions, not automatic blockers.
- Establish the permitted sources and whether the user wants a saved packet.
  Choose a feature slug for deterministic artifact identity.
- Use `prepare --request <path>` for a UTF-8 input file, or
  `prepare --request-stdin` for verbatim pasted input. External evidence is an
  explicit local snapshot; helpers never fetch links or execute source content.

## Tell your agent

```text
Use ai-sdlc-requirements-discovery for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report Source-bound context, validated TOON discovery packet, business options, stakeholder questions, and conditional handoff, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Raw request, notes, feedback or a source locator. Ask for the actual request if
  none is available; do not invent it from the skill invocation alone.
- Identify product, actors, desired outcome and constraints from available
  context. Missing details are discovery questions, not automatic blockers.
- Establish the permitted sources and whether the user wants a saved packet.
  Choose a feature slug for deterministic artifact identity.
- Use `prepare --request <path>` for a UTF-8 input file, or
  `prepare --request-stdin` for verbatim pasted input. External evidence is an
  explicit local snapshot; helpers never fetch links or execute source content.

## What it may write

- The helper emits TOON to stdout by default. `--write` enables canonical
  feature output when durable work is in scope; `--replace` is required to
  change an existing differing output after reviewing it.
- `prepare` and `scaffold` write
  `specs-refiniment/<feature>/_ai_sdlc/requirements-discovery-context.toon`
  and `requirements-discovery-draft.toon`.
- `finalize` owns `_ai_sdlc/requirements-discovery.toon` and its human projection,
  `specs-refiniment/<feature>/requirements-discovery.md`. Never hand-edit the
  final files or place discovery in `specs/`.
- Keep owner decisions in the typed draft with source evidence. If an existing
  feature decision log is updated, link it without converting a proposal to acceptance.

## Human checkpoints

- Resolve discoverable facts and reuse inherited decisions before asking.
- Missing optional context stays optional; label assumptions explicitly.
- Pause only work dependent on a missing material input or conflicting requirement.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.

## Procedural step selectors

The router loads these skill-owned procedures just in time. Read only the selector matching the current phase, active role, and action; a selected step is normative and an unselected step stays out of context.

| Selector | Type | Phases | Roles | Dependencies | Operation | Side effect | Load rule | Step | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `preflight` | `analysis` | `prepare` | `business-analyst`, `product-manager`, `software-engineer`, `qa-engineer` | none | `bound-discovery` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-requirements-discovery/steps/01-prepare.md) | bound the feature or task and identify available raw inputs |
| `context` | `context` | `clarify`, `route` | `business-analyst`, `product-manager`, `software-engineer`, `qa-engineer` | `preflight` | `collect-requirements-evidence` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-requirements-discovery/steps/02-context.md) | select source evidence and test whether precedents transfer |
| `execute` | `action` | `execute` | `business-analyst`, `product-manager`, `software-engineer`, `qa-engineer` | `context` | `analyze-business-options` | `workspace-write` | `on-demand` | [`steps/02-execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-requirements-discovery/steps/02-execute.md) | compare business responses and prepare decision-linked stakeholder questions |
| `validate` | `validation` | `validate` | `business-analyst`, `product-manager`, `software-engineer`, `qa-engineer` | `execute` | `validate-discovery` | `none` | `before-completion` | [`steps/03-validate-and-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-requirements-discovery/steps/03-validate-and-handoff.md) | check traceability, option distinctions, and unresolved product choices |
| `handoff` | `handoff` | `handoff`, `complete` | `business-analyst`, `product-manager`, `software-engineer`, `qa-engineer` | `validate` | `handoff-result` | `none` | `before-completion` | [`steps/04-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-requirements-discovery/steps/04-handoff.md) | return the elicitation packet and next accountable owner |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` or `.claude/skills/<skill>/...` path reported by your profile. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`requirements_discovery.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-requirements-discovery/scripts/requirements_discovery.py) | Prepare, scaffold, validate, finalize and verify sourced discovery packets. | `python3 skills/ai-sdlc-requirements-discovery/scripts/requirements_discovery.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

Resolve `skills/` to the installed skills root when needed. For durable work,
run these commands in the project root; use the matching flow flag in prepare.

```bash
python3 skills/ai-sdlc-requirements-discovery/scripts/requirements_discovery.py prepare --feature <feature> --request <raw-input.md> --source <past-decision.md> --quick-flow --write
python3 skills/ai-sdlc-requirements-discovery/scripts/requirements_discovery.py scaffold --context specs-refiniment/<feature>/_ai_sdlc/requirements-discovery-context.toon --as-of <YYYY-MM-DD> --write
```

For pasted input use `--request-stdin` instead of `--request` and stream the
verbatim request on stdin. Omit `--source` when no historical evidence is available.
The helper marks stdin as a fixed snapshot; file sources receive freshness checks.

Fill only the generated draft using the schema and example in `references/`.
Keep its context fingerprint and explicit date. Supply all business judgments,
evidence limits and source-linked records as data. The empty scaffold is
intentionally invalid until analysis and question coverage are populated.

```bash
python3 skills/ai-sdlc-requirements-discovery/scripts/requirements_discovery.py validate --context specs-refiniment/<feature>/_ai_sdlc/requirements-discovery-context.toon --draft specs-refiniment/<feature>/_ai_sdlc/requirements-discovery-draft.toon
python3 skills/ai-sdlc-requirements-discovery/scripts/requirements_discovery.py finalize --context specs-refiniment/<feature>/_ai_sdlc/requirements-discovery-context.toon --draft specs-refiniment/<feature>/_ai_sdlc/requirements-discovery-draft.toon --write
python3 skills/ai-sdlc-requirements-discovery/scripts/requirements_discovery.py verify --report specs-refiniment/<feature>/_ai_sdlc/requirements-discovery.toon
```

All commands are offline. Omit `--write` to emit without persisting; `--replace`
is used only with `--write` after reviewing a differing existing output.
Never bypass a failed check by editing a final report or its fingerprint.
For updated sources, rebuild context and review/rebase the analysis onto it.

## Success criteria

Return a problem brief, classified requirements with source IDs, precedent
evidence and transfer limits, a business-option comparison, and prioritized
questions with stakeholder roles, evidence methods and decision consequences.
State the conditional recommendation, unresolved choices and next owner.
The full field contract and illustrative case are in
`references/output-contract.md`.

## Blockers and recovery

- Resolve discoverable facts and reuse inherited decisions before asking.
- Missing optional context stays optional; label assumptions explicitly.
- Pause only work dependent on a missing material input or conflicting requirement.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Return completion and next steps directly in the active agent response.
- Do not create `summary.txt` or another standalone summary file unless requested.
- Follow `references/output-contract.md`; identify what is confirmed, inferred,
  disputed, missing and proposed. Mark readiness separately from packet completion.
- Return useful findings even when history, stakeholder names or replies are
  unavailable. Use roles as proposed contacts when names are unknown.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read existing `_ai_sdlc/state.toon` when present. This optional advisory skill
      adds no lifecycle stage; do not invoke begin/complete for it or change another
      skill's state. A completed packet is not refinement or implementation readiness.

??? info "Artifact metadata"

    - The helper generates Markdown starting with `artifact_metadata` using
      `ai-sdlc-artifact-metadata/v1`: feature, artifact, path, workspace
      (`refinement`), skill, flow_mode, state_file, decision_log, status, owner,
      created_at, updated_at, trace_ids, related_artifacts, validation and metatags.
    - The draft's explicit `as_of` date determines metadata dates; no wall clock
      participates in context, report or Markdown generation.
    - The generated projection uses this skill's name and tags `ai-sdlc`, `refinement`,
      `requirements-discovery`, plus the actual status. Do not imply stakeholder
      acceptance through a `validated` or `approved` packet status.

??? info "Specs index"

    - Before broad feature searches, use an existing
      `specs-refiniment/_ai_sdlc/specs-index.toon` or
      `specs/_ai_sdlc/specs-index.toon` to select related evidence.
    - After a durable refinement write, run the installed shared runtime's
      `ai_sdlc_specs_index.py --workspace refinement --quick-flow`
      (or `--full-flow` for that mode) and verify the feature's `index.md`.

## Example

```text
Use ai-sdlc-requirements-discovery --quick-flow.
Analyze these raw feature requirements: <request or source path>.
Compare business options using available historical decisions: <source paths>.
Prepare stakeholder questions with priorities and evidence-gathering methods.
```

## Source contract

This page is generated from [`skills/ai-sdlc-requirements-discovery/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-requirements-discovery/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
