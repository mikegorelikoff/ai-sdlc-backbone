# Prepare — ai-sdlc-qa: QA Planning And Evidence

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Requirements, stories, delivery spec, `specs-refiniment/<feature-name>/<file.md>` QA context, or changed implementation context.
- Acceptance criteria, changed files, or release-sensitive behavior.
- Validation output if already run.

### 0.2 Clarification Rules

- Resolve discoverable facts and reuse inherited decisions before asking.
- Missing optional context stays optional; label assumptions explicitly.
- Pause only work dependent on a missing material input or conflicting requirement.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.


### 0.3 Output Rules

- Keep output structured with headings and bullets.
- Make findings, gaps, risks, and blockers explicit.
- Tie recommendations to evidence from the provided artifact, `specs-refiniment/<feature-name>/<file.md>` workspace, or user context.
- Include role ownership when the output creates follow-up work for BA, QA, Dev, PM, or Delivery.
- Return progress, completion, validation, and handoff summaries directly in the active agent response.
- Before the final response, emit the `ai-sdlc-handoff/v2` contract with `result`, `blockers`, `next_required`, and `next_optional`; every action includes `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file unless the user explicitly requests one.
- Keep durable writes limited to the canonical lifecycle artifacts, decision log, human-readable index, and `_ai_sdlc` machine files.
- Let shared helpers migrate legacy paths on the next write; never overwrite or manually merge divergent legacy and canonical files.

### 0.4 Artifact Routing

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

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

Registered stage: `qa_plan`; workspace: `refinement`.
Canonical output: `qa.md`. Required predecessors: `ai-sdlc-requirements-readiness-review`.
Possible downstream consumers: `ai-sdlc-qa-requirements-gap-review`; these are not automatic invocations.

Follow the shared registered-stage protocol for `check`, `begin` and evidence-
backed `complete`. Keep feature state at `_ai_sdlc/state.toon`; an index or
conversation does not establish stage completion. Preserve the owning skill's
quick/full gates and record any permitted predecessor exception explicitly.

## 0.6 Artifact Metadata And Metatags

For canonical lifecycle Markdown, use the shared Harness metadata contract.
The owning writer maintains `artifact_metadata`, `metatags`, current sources,
validation and status. Do not mark planned or missing evidence as validated.

## 0.7 Specs Index

- Before searching across feature folders, inspect the compact LLM index first: `specs-refiniment/_ai_sdlc/specs-index.toon` for refinement work or `specs/_ai_sdlc/specs-index.toon` for implementation work.
- Use the human-readable index at `specs-refiniment/<feature-name>/index.md` or `specs/<feature-name>/index.md` when reporting feature coverage, artifact inventory, or handoff status to people.
- After this skill creates or materially updates an artifact, refresh the matching workspace index with `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_specs_index.py --workspace <refinement|implementation> --quick-flow|--full-flow`.
- In `--quick-flow`, rely on `specs-index.toon` to choose the smallest relevant artifact set before opening files.
- In `--full-flow`, verify the updated artifact appears in both `specs-index.toon` and feature-local `index.md` before final handoff.
- The specs index summarizes artifact metadata and state; it does not replace reading the selected source artifacts when details, approvals, or validation evidence matter.

## 0.8 Complete Refinement Cascade

- Trigger the complete cascade only when the user explicitly asks for a full, complete, or end-to-end spec refinement or asks for every refinement artifact. A normal `--full-flow` call for one skill remains single-stage.
- Before the first durable write, run `python3 skills/ai-sdlc-shared-runtime/scripts/refinement_status.py --feature <feature-name> --gate full --format toon` and start with the earliest reported `next_skill`, including stages earlier than this skill.
- Execute the existing refinement skills in lifecycle order with `--full-flow`: discovery, PRFAQ, delivery-package gap review, requirements readiness, goal/capability mapping, backlog gap review, backlog decomposition, story decomposition, release slicing, BA context, delivery spec, QA plan, QA gap review, test strategy, test cases, test suite, QA readiness, and delivery handoff.
- Produce all 18 canonical Markdown artifacts. `release-slicing.md` is mandatory for a complete cascade; when release slicing is not applicable, write an explicit evidence-backed N/A artifact and complete the stage instead of skipping it.
- After every stage, finalize its artifact, record required decisions, mark the stage `done`, and refresh the refinement indexes before selecting the next skill.
- Do not declare the cascade complete until `python3 skills/ai-sdlc-shared-runtime/scripts/refinement_status.py --feature <feature-name> --gate full --format markdown` exits successfully with `18/18`. If it fails, continue with the reported next skill or return the concrete blocker and remaining inventory in the active agent response.
- Surface checkpoint and final summaries in Codex only; never persist a cascade summary as a text file.

## Execution contract

Do not use it while expected behavior or acceptance criteria are undefined. Use the requirements readiness or business-analysis workflow instead.

Read the [shared execution decisions](../../ai-sdlc-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
