---
title: Commit Prep
description: Human-facing operating guide for ai-sdlc-commit-prep, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-commit-prep`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Commit readiness / traceability | Dev | QA, BA, PM | `core` | Safe staged set, validated commit readiness, conventional commit message, and post-commit traceability |

## Why it exists

Prepare and create a safe AI SDLC commit by reviewing the branch and working tree, staging only related files, validating SDD evidence, using a valid Conventional Commit message, and reporting post-commit traceability.

## Use it when

AI SDLC commit preparation workflow. Use when an AI assistant is asked to commit repository changes, prepare an auditable commit message, stage files safely, include SDD traceability, verify branch/spec alignment, or verify the working tree before committing. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use it while the task or validation evidence is incomplete. Use `ai-sdlc-validation` and finish the owning task instead.
- Do not use it only to word a commit subject. Use `ai-sdlc-conventional-commit` instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Explicit commit request or completed workflow state.
- Current branch, dirty tree, staged files, and diff.
- Validation results plus spec traceability when applicable.

## Tell your agent

```text
Use ai-sdlc-commit-prep for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report Safe staged set, validated commit readiness, conventional commit message, and post-commit traceability, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Collect the user’s explicit commit request or workflow state showing commit prep is justified.
- Collect the active spec folder for medium or large work.
- Collect validation commands and outcomes that are current for the active diff.
- Collect the current branch and dirty tree from `git status --short --branch`.

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

- Use `specs/` only for developer implementation SDD packages and repo-governance artifacts.
- Do not place PM, BA, QA, Delivery, discovery, planning, refinement, or readiness outputs in `specs/`; those belong at `specs-refiniment/<feature-name>/<file.md>`.
- When consuming `specs-refiniment/<feature-name>/<file.md>`, treat it as upstream refinement context and create or update `specs/` only when implementation work is explicitly in scope.

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
| `preflight` | `analysis` | `prepare` | `software-engineer` | none | `inspect-and-route` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-commit-prep/steps/01-prepare.md) | establish inputs, authority, lifecycle state, and safe artifact routing |
| `context` | `context` | `clarify`, `route` | `software-engineer` | `preflight` | `compile-context` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-commit-prep/steps/02-context.md) | compile the minimum sufficient context before the owning action |
| `execute` | `action` | `execute` | `software-engineer` | `context` | `execute-procedure` | `workspace-write` | `on-demand` | [`steps/02-execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-commit-prep/steps/02-execute.md) | perform only the selected owning-skill procedure |
| `validate` | `validation` | `validate` | `software-engineer` | `execute` | `validate-evidence` | `none` | `before-completion` | [`steps/03-validate-and-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-commit-prep/steps/03-validate-and-handoff.md) | validate outputs, evidence, acceptance, and residual risk |
| `handoff` | `handoff` | `handoff`, `complete` | `software-engineer` | `validate` | `handoff-result` | `none` | `before-completion` | [`steps/04-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-commit-prep/steps/04-handoff.md) | return a journal-backed owner and next-action handoff |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` or `.claude/skills/<skill>/...` path reported by your profile. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`check_commit_ready.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py) | Check AI SDLC commit readiness signals. | `python3 skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py --help` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

- Run commit readiness before staging final commit content or writing the final commit summary.
- Quick flow: `python3 skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py --quick-flow --spec specs/<feature-name> --allow-unstaged --no-require-staged`
- Full flow: `python3 skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py --full-flow --spec specs/<feature-name>`
- For an explicitly task-scoped commit in a larger active SDD plan, add
  `--task TNNN`. The selected task must be present and complete; later pending
  tasks remain allowed. Without `--task`, every spec task must be complete.
- Every medium or large traced SDD commit message must include the completed
  task identity as `Task: TNNN` (or a comma-separated list). `--task` narrows
  the readiness check; it does not replace the commit-message trailer.
- Use `--allow-unstaged` only when intentionally checking readiness before final staging.
- Use `--no-require-staged` only for preflight checks; omit it immediately before commit creation.

## Success criteria

Return this final report:

```text
Commit:
- Hash: full_hash
- Subject: conventional subject
- Branch: branch-name
- Spec: specs/NNN-feature-name | none
- Task: TNNN[, TNNN] | none

Staging:
- Included: path groups and why they belong.
- Excluded: unrelated dirty paths or none.

Validation:
- command -> outcome

Post-commit:
- Working tree: clean | dirty with listed paths.
- Residual risk: none | concrete issue.
```

Quality gate:

- Pass when the branch/spec relationship is explicit, the commit contains only related files, validation is current, message validation passes, and post-commit status is reported.
- Fail when branch/spec mismatch is hidden, unrelated files are staged, validation is stale, the message validator fails, or the final report hides a dirty tree.

## Blockers and recovery

- Stop and ask before staging when unrelated changes are mixed inside a file required for the current change.
- Stop and resolve branch state with `$ai-sdlc-branching` when medium or large work is still on `dev`, `main`, `master`, or a branch that does not include the active spec slug.
- Use `--allow-unstaged` on the readiness checker only when unrelated unstaged files are intentionally left out and reported.
- Do not amend an existing commit unless the user explicitly requests amend.
- Do not run destructive cleanup commands unless the user requested or approved them.
- Report failed commit hooks with the hook output and do not claim a commit exists.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Keep output structured with headings and bullets.
- Make findings, gaps, risks, and blockers explicit.
- Tie recommendations to evidence from the provided artifact, repository, `specs-refiniment/<feature-name>/<file.md>` workspace, or user context.
- Include role ownership when the output creates follow-up work for BA, QA, Dev, PM, or Delivery.
- Return progress, completion, validation, and handoff summaries directly in the active agent response.
- Before the final response, emit the `ai-sdlc-handoff/v2` contract with `result`, `blockers`, `next_required`, and `next_optional`; every action includes `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file unless the user explicitly requests one.
- Keep durable writes limited to the canonical lifecycle artifacts, decision log, human-readable index, and `_ai_sdlc` machine files.
- Let shared helpers migrate legacy paths on the next write; never overwrite or manually merge divergent legacy and canonical files.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    Registered stage: `commit_prep`; workspace: `implementation`.
    Canonical output: `commit-readiness.md`. Required predecessors: `ai-sdlc-code-review`.
    Possible downstream consumers: `ai-sdlc-conventional-commit`; these are not automatic invocations.

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

Valid staging rationale:

```text
Staging:
- Included: `skills/*/SKILL.md` because every file is part of the skill instruction upgrade.
- Included: `specs/177-skill-instruction-upgrade/*` because the SDD package documents this change.
- Excluded: `apps/web/.env.local` because it is unrelated and sensitive.
```

Invalid counter-example:

```text
Ran git add -A and committed everything.
```

Reject this when the working tree contains files not inspected for scope.

## Source contract

This page is generated from [`skills/ai-sdlc-commit-prep/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-commit-prep/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
