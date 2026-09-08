---
title: Backlog Requirements Gap Review
description: Human-facing operating guide for ai-sdlc-backlog-requirements-gap-review, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-backlog-requirements-gap-review`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Pre-backlog planning review | BA | Product Owner, PM, Delivery, QA | `core` | Backlog-blocking gaps, assumptions, open questions, and readiness decision |

## Why it exists

Review the incoming initiative package and determine whether it is specific enough to support backlog decomposition and release planning.

## Use it when

Use when PRFAQ, BRD, PRD, product brief, workflow, or equivalent initiative artifacts exist and you need to review them for planning gaps, unclear scope, weak priorities, missing actors, and backlog-blocking ambiguity before decomposing work. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use it before goals, roles, capabilities, and epics exist. Use `ai-sdlc-goal-capability-and-epic-mapping` instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- PRFAQ, BRD, PRD, product brief, workflow, or equivalent artifact.
- Planning goal or target backlog scope.
- Known priority, MVP, or release constraints.

## Tell your agent

```text
Use ai-sdlc-backlog-requirements-gap-review for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report Backlog-blocking gaps, assumptions, open questions, and readiness decision, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- PRFAQ, BRD, PRD, product brief, workflow, or equivalent artifact.
- Planning goal or target backlog scope.
- Known priority, MVP, or release constraints.

## What it may write

- Maintain a feature decision log whenever this skill records, resolves, changes, or depends on a product, delivery, QA, security, validation, branching, implementation, or rollout decision.
- For PM, BA, QA, Delivery, discovery, planning, refinement, and readiness work, write decisions to `specs-refiniment/<feature-name>/decision-log.md`.
- For developer implementation SDD work, write decisions to `specs/<feature-name>/decision-log.md`.
- Each decision-log entry must include date, decision, context or evidence, options considered when relevant, owner, status, and links to affected artifacts, tasks, tests, or validation evidence.
- Use this exact decision-log structure:

  ```markdown
  # Decision Log

  | ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | DEC-001 | YYYY-MM-DD | proposed / accepted / superseded / rejected | role or name | concise decision | source facts, artifact links, or evidence | option A; option B; recommended default | affected docs, tasks, code, tests, or rollout notes | requirement IDs, test IDs, validation commands, PRs, commits, or tickets |
  ```

- When writing or updating files, place PM, BA, QA, Delivery, discovery, planning, refinement, and readiness artifacts at `specs-refiniment/<feature-name>/<file.md>`.
- Use the path pattern `specs-refiniment/<feature-name>/<file.md>`; choose a stable feature slug when known, otherwise use `tbd-<short-topic>` for `<feature-name>`.
- Do not write this skill's output into `specs/`; that folder is reserved for developer implementation SDD artifacts.
- If the user explicitly asks to convert a refined artifact into developer implementation work, hand off to `$ai-sdlc-sdd`.

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
| `preflight` | `analysis` | `prepare` | `business-analyst` | none | `inspect-and-route` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-backlog-requirements-gap-review/steps/01-prepare.md) | establish inputs, authority, lifecycle state, and safe artifact routing |
| `context` | `context` | `clarify`, `route` | `business-analyst` | `preflight` | `compile-context` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-backlog-requirements-gap-review/steps/02-context.md) | compile the minimum sufficient context before the owning action |
| `execute` | `action` | `execute` | `business-analyst` | `context` | `execute-procedure` | `workspace-write` | `on-demand` | [`steps/02-execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-backlog-requirements-gap-review/steps/02-execute.md) | perform only the selected owning-skill procedure |
| `validate` | `validation` | `validate` | `business-analyst` | `execute` | `validate-evidence` | `none` | `before-completion` | [`steps/03-validate-and-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-backlog-requirements-gap-review/steps/03-validate-and-handoff.md) | validate outputs, evidence, acceptance, and residual risk |
| `handoff` | `handoff` | `handoff`, `complete` | `business-analyst` | `validate` | `handoff-result` | `none` | `before-completion` | [`steps/04-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-backlog-requirements-gap-review/steps/04-handoff.md) | return a journal-backed owner and next-action handoff |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` or `.claude/skills/<skill>/...` path reported by your profile. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`backlog_gap_scan.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-backlog-requirements-gap-review/scripts/backlog_gap_scan.py) | Compress initiative artifacts into backlog-planning gap signals. | `Imported helper; use the owning skill rather than invoking it directly.` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/backlog_gap_scan.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-backlog-requirements-gap-review/scripts/backlog_gap_scan.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-backlog-requirements-gap-review/scripts/backlog_gap_scan.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Success criteria

A successful result produces Backlog-blocking gaps, assumptions, open questions, and readiness decision and satisfies every output rule and blocker check below.

## Blockers and recovery

- Resolve discoverable facts and reuse inherited decisions before asking.
- Missing optional context stays optional; label assumptions explicitly.
- Pause only work dependent on a missing material input or conflicting requirement.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Keep output structured with headings and bullets.
- Make findings, gaps, risks, and blockers explicit.
- Tie recommendations to evidence from the provided artifact, `specs-refiniment/<feature-name>/<file.md>` workspace, or user context.
- Include role ownership when the output creates follow-up work for BA, QA, Dev, PM, or Delivery.
- Return progress, completion, validation, and handoff summaries directly in the active agent response.
- Before the final response, emit the `ai-sdlc-handoff/v2` contract with `result`, `blockers`, `next_required`, and `next_optional`; every action includes `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file unless the user explicitly requests one.
- Keep durable writes limited to the canonical lifecycle artifacts, decision log, human-readable index, and `_ai_sdlc` machine files.
- Let shared helpers migrate legacy paths on the next write; never overwrite or manually merge divergent legacy and canonical files.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    Registered stage: `backlog_gap_review`; workspace: `refinement`.
    Canonical output: `backlog-gap-review.md`. Required predecessors: `ai-sdlc-goal-capability-and-epic-mapping`.
    Possible downstream consumers: `ai-sdlc-backlog-decomposition-and-task-planning`; these are not automatic invocations.

    Follow the shared registered-stage protocol for `check`, `begin` and evidence-
    backed `complete`. Keep feature state at `_ai_sdlc/state.toon`; an index or
    conversation does not establish stage completion. Preserve the owning skill's
    quick/full gates and record any permitted predecessor exception explicitly.

??? info "Artifact metadata"

    For canonical lifecycle Markdown, use the shared Harness metadata contract.
    The owning writer maintains `artifact_metadata`, `metatags`, current sources,
    validation and status. Do not mark planned or missing evidence as validated.

??? info "Specs index"

    - Before searching across feature folders, inspect the compact LLM index first: `specs-refiniment/_ai_sdlc/specs-index.toon` for refinement work or `specs/_ai_sdlc/specs-index.toon` for implementation work.
    - Use the human-readable index at `specs-refiniment/<feature-name>/index.md` or `specs/<feature-name>/index.md` when reporting feature coverage, artifact inventory, or handoff status to people.
    - After this skill creates or materially updates an artifact, refresh the matching workspace index with `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_specs_index.py --workspace <refinement|implementation> --quick-flow|--full-flow`.
    - In `--quick-flow`, rely on `specs-index.toon` to choose the smallest relevant artifact set before opening files.
    - In `--full-flow`, verify the updated artifact appears in both `specs-index.toon` and feature-local `index.md` before final handoff.
    - The specs index summarizes artifact metadata and state; it does not replace reading the selected source artifacts when details, approvals, or validation evidence matter.

## Example

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/backlog_gap_scan.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-backlog-requirements-gap-review/scripts/backlog_gap_scan.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-backlog-requirements-gap-review/scripts/backlog_gap_scan.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Source contract

This page is generated from [`skills/ai-sdlc-backlog-requirements-gap-review/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-backlog-requirements-gap-review/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
