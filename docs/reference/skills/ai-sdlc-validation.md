---
title: Validation
description: Human-facing operating guide for ai-sdlc-validation, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-validation`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Implementation validation | Dev | QA, BA | `core` | Focused validation commands, outcomes, coverage notes, and residual risk |

## Why it exists

Select, run, and report focused deterministic validation checks for AI SDLC code, SQL, API, provider, SDD, documentation, and tool-governance changes.

## Use it when

AI SDLC backend validation workflow. Use when an AI assistant needs to validate Go, SQL, API, provider integration, SDD, or documentation changes in this repository and choose focused deterministic checks without running unrelated expensive tests by default. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use it when expected behavior is undefined. Use `ai-sdlc-sdd` or the QA requirements workflow instead.
- Do not use it to produce review findings. Use `ai-sdlc-code-review` or `ai-sdlc-security-testing` instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Changed files, diff, or explicit validation target.
- Active spec and QA context when user-visible or release-sensitive.
- Sandbox constraints and previous validation output if relevant.

## Tell your agent

```text
Use ai-sdlc-validation for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report Focused validation commands, outcomes, coverage notes, and residual risk, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Collect changed files from `git status --short`, `git diff --name-only`, or explicit user-provided paths.
- Read the active spec and `qa.md` when the work is medium, large, release-sensitive, or user-visible.
- Collect previous validation output only when it is current for the same diff signature.
- Collect sandbox constraints that affect Go cache, network access, local listeners, or external services.
- Run the validation planner when changed files are not trivial:

  ```bash
  python3 skills/ai-sdlc-validation/scripts/validation_plan.py
  ```

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
| `preflight` | `analysis` | `prepare` | `qa-engineer`, `software-engineer` | none | `inspect-and-route` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-validation/steps/01-prepare.md) | establish inputs, authority, lifecycle state, and safe artifact routing |
| `context` | `context` | `clarify`, `route` | `qa-engineer`, `software-engineer` | `preflight` | `compile-context` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-validation/steps/02-context.md) | compile the minimum sufficient context before the owning action |
| `execute` | `action` | `execute` | `qa-engineer`, `software-engineer` | `context` | `execute-procedure` | `workspace-write` | `on-demand` | [`steps/02-execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-validation/steps/02-execute.md) | perform only the selected owning-skill procedure |
| `validate` | `validation` | `validate` | `qa-engineer`, `software-engineer` | `execute` | `validate-evidence` | `none` | `before-completion` | [`steps/03-validate-and-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-validation/steps/03-validate-and-handoff.md) | validate outputs, evidence, acceptance, and residual risk |
| `handoff` | `handoff` | `handoff`, `complete` | `qa-engineer`, `software-engineer` | `validate` | `handoff-result` | `none` | `before-completion` | [`steps/04-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-validation/steps/04-handoff.md) | return a journal-backed owner and next-action handoff |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` or `.claude/skills/<skill>/...` path reported by your profile. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`run_validation.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-validation/scripts/run_validation.py) | Execute a reviewed argv-only validation plan and write current evidence. | `python3 skills/ai-sdlc-validation/scripts/run_validation.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`validation_plan.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-validation/scripts/validation_plan.py) | Suggest focused AI SDLC validation commands from changed files. | `python3 skills/ai-sdlc-validation/scripts/validation_plan.py --help` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

- Run validation planning after identifying changed files and before choosing commands manually.
- Quick flow: `python3 skills/ai-sdlc-validation/scripts/validation_plan.py --quick-flow <changed-file>...`
- Full flow: `python3 skills/ai-sdlc-validation/scripts/validation_plan.py --full-flow <changed-file>...`
- If no files are supplied, the script inspects the current git worktree.
- Execute the suggested commands that match the requested risk level; document skipped broader commands as residual risk.

## Success criteria

Use this format:

```text
Validation:
- command: exact command
  outcome: passed | failed | skipped | blocked
  reason: why this command was selected or skipped

Coverage:
- Changed surface: files or package group.
- Behavior covered: requirement, scenario, or risk covered by the command.

Residual risk:
- none | explicit unvalidated behavior and why it remains.
```

Quality gate:

- Pass when validation commands match the changed surfaces, required checks are current for the active diff, and skipped checks include residual risk.
- Fail when validation is broad but irrelevant, narrow but misses a changed contract, or reports success while a command failed.

## Blockers and recovery

- Mark a check `blocked` when sandbox, missing dependency, missing credential, or unavailable service prevents execution.
- Request escalation only after a required command fails for a likely sandbox reason; do not escalate to bypass project policy.
- Run broader suites after focused checks when the changed surface spans handlers, services, providers, config, or generated contracts.
- Do not run production integrations unless the user explicitly requests them and required credentials are already available through approved mechanisms.
- Treat stale validation as absent when files changed after the command ran.

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

    Registered stage: `validation`; workspace: `implementation`.
    Canonical output: `validation.md`. Required predecessors: `ai-sdlc-sdd`.
    Possible downstream consumers: `ai-sdlc-code-review`; these are not automatic invocations.

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

Focused Go package change:

```text
Validation:
- command: GOCACHE=/tmp/ai-sdlc-go-cache go test ./internal/service -run 'TestLoanTransfer|TestReturnPreflight' -count=1
  outcome: passed
  reason: covers changed service behavior and preflight failure paths.
- command: git diff --check
  outcome: passed
  reason: required whitespace validation for all changes.

Residual risk:
- none
```

Tool setup change:

```text
Validation:
- command: PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-harness-pycache python3 -m py_compile skills/ai-sdlc-validation/scripts/validation_plan.py
  outcome: passed
  reason: validates changed skill metadata.
- command: python3 skills/ai-sdlc-sdd/scripts/sdd_status.py --spec specs/185-spec-kit-sdd-quality-gates
  outcome: passed
  reason: confirms the active governance spec is structurally valid and ready for implementation.
- command: find skills -name SKILL.md -maxdepth 2
  outcome: passed
  reason: validates SDD governance shape.
```

Invalid counter-example:

```text
Validation passed.
```

Reject this because it omits exact commands, changed surface coverage, and residual risk.

## Source contract

This page is generated from [`skills/ai-sdlc-validation/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-validation/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
