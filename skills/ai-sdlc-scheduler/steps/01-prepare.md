# Prepare — AI SDLC Scheduler

## Entry

A validated run plan and explicit scheduler state path are available.

## Procedure

Confirm authority, run identity, repository containment, worker and retry
budgets, injected clock, and immutable plan fingerprint. Reject ambiguous state
ownership or an existing state path during create.

Support `--quick-flow` for bounded assumption-driven work and `--full-flow` for
verified handoff.

### 0.1 Required Inputs

- Validated immutable run plan, scheduler state path, run ID, worker identity,
  expected revision, injected integer clock, lease duration, and authority.

### 0.2 Clarification Rules

- Resolve discoverable facts and reuse inherited decisions before asking.
- Missing optional context stays optional; label assumptions explicitly.
- Pause only work dependent on a missing material input or conflicting requirement.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.


### 0.3 Output Rules

- Return scheduler progress and blockers directly in the active agent response.
  Keep machine state, events, dispatches, and receipts in `_ai_sdlc/` as TOON.

### 0.4 Artifact Routing

- Route scheduler runs under `_ai_sdlc/scheduler/<run-id>/`, isolated runtime
  runs under `_ai_sdlc/runs/`, and feature decisions to its decision log.

## 0.4.1 Runtime Path Resolution

In a source checkout, resolve logical `skills/` commands under `skills/`. In a
consumer repository, resolve them under `.agents/skills/` and require the
sibling `ai-sdlc-shared-runtime`. Never infer a global installation.

## 0.5 Feature State Machine

Keep lifecycle state at `specs/<feature>/_ai_sdlc/state.toon`; never expose it
as a top-level file. Record decisions in the feature decision log and honor
predecessor stages before claiming implementation work.

## 0.6 Artifact Metadata And Metatags

Generated Markdown must carry `artifact_metadata` and useful `metatags`; these
indexes never replace the body or decision log.

## 0.7 Specs Index

Inspect `_ai_sdlc/specs-index.toon` before broad reads and refresh both it and
the feature-local `index.md` after durable artifact changes. Do not create `summary.txt`
or another detached summary. Report progress directly in the
active agent response and report completion directly in the active agent response.

## Execution contract

Do not use it without a validated immutable run plan or when one sequential runtime is sufficient. Use `ai-sdlc-runtime` instead. Do not use a scheduler lease as external-effect authority. Use `ai-sdlc-host-adapter` negotiation and its registered effect driver instead.

Read the [shared execution decisions](../../ai-sdlc-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Inputs and authority are explicit, or a precise blocker is returned.
