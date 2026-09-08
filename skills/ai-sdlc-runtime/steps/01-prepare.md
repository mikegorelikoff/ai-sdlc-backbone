# Prepare — ai-sdlc-runtime: Resumable Delivery Runs

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Versioned run plan, safe run ID, dependency graph, task input fingerprints,
  retry limits, budgets, and commit-boundary flags.
- Exact result fingerprint, token use, commit evidence, and reason when recording.

### 0.2 Clarification Rules

- Resolve discoverable facts and reuse inherited decisions before asking.
- Missing optional context stays optional; label assumptions explicitly.
- Pause only work dependent on a missing material input or conflicting requirement.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.


### 0.3 Output Rules

- Report run status, sequence, current task, ready tasks, budgets, stop reason,
  recovery status, and next command.
- Return validation and handoff summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v2` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

### 0.4 Artifact Routing

- Route each run only to `_ai_sdlc/runs/<run-id>/`.
- Keep journal append-only, TOON recovery state atomically replaceable, and
  TOON state as the complete agent-facing projection.
- Never store runtime records inside a feature spec folder.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read the owning feature `_ai_sdlc/state.toon` before starting feature work.
- Runtime task state does not replace feature `state.toon`; the owning workflow
  performs feature transitions only after runtime and validation evidence agree.

## 0.6 Artifact Metadata And Metatags

- Runtime-related Markdown uses canonical `artifact_metadata` and `metatags`.
- Machine records use `ai-sdlc-run-plan/v2`, `ai-sdlc-run-event/v2`, and
  `ai-sdlc-run-state/v2` with deterministic fingerprints.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` first and use feature-local `index.md` for human
  feature discovery before constructing a plan.
- Runtime state does not refresh either specs index.

## Execution contract

Do not use it without an accepted immutable execution plan. Use `ai-sdlc-workflow` or `ai-sdlc-sdd` instead. Do not use it for a bounded one-off task that needs no declared DAG. Use the normal owning implementation workflow instead.

Read the [shared execution decisions](../../ai-sdlc-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
