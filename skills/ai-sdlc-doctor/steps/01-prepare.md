# Prepare — ai-sdlc-doctor: Diagnostics And Safe Upgrade Plans

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Repository root for doctor checks.
- Current and target versioned inventories plus active harness API for upgrade planning.

### 0.2 Clarification Rules

- Resolve discoverable facts and reuse inherited decisions before asking.
- Missing optional context stays optional; label assumptions explicitly.
- Pause only work dependent on a missing material input or conflicting requirement.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.


### 0.3 Output Rules

- Default to complete TOON with checks, evidence, remediation, file changes,
  migrations, backups, rollback actions, blockers, and fingerprints.
- Return summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v2` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

### 0.4 Artifact Routing

- Write generated reports only below repository `_ai_sdlc/`.
- Keep authored upgrade inventories visible and version controlled.
- Never treat a generated plan as authority to apply changes.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read owning feature `_ai_sdlc/state.toon` when diagnostics affect feature work.
- Diagnostics and upgrade plans do not mutate feature state.

## 0.6 Artifact Metadata And Metatags

- Related Markdown uses canonical `artifact_metadata` and `metatags`.
- Machine records use versioned doctor, inventory, and upgrade-plan schemas.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` first and use feature-local `index.md` for human review.
- Operational reports do not refresh either index.

## Execution contract

Do not use it to diagnose application feature behavior. Use `ai-sdlc-validation` instead. Do not use it to apply installation or upgrade changes. Use the authorized install or update workflow instead.

Read the [shared execution decisions](../../ai-sdlc-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
