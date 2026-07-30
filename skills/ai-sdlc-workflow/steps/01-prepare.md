# Prepare — ai-sdlc-workflow: Declarative Workflow Planning

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Versioned workflow TOON whose nodes name installed skills, canonical
  entrypoints, dependencies, bounded conditions, and approval owners.
- Optional TOON condition context, requested concurrency, and explicit approved
  node IDs.

### 0.2 Clarification Rules

- Ask when a target skill, entrypoint, action, role, or approval owner is
  materially ambiguous.
- Reject unknown fields, cycles, unsafe identifiers, invalid conditions, and
  missing canonical skill graphs.
- Never infer approval, shell authority, network authority, or host execution.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes use identical validation, cycle, condition, approval, and
  compilation rules.
- Full flow requires review of every skipped, deferred, or blocked node.

### 0.3 Output Rules

- Default to complete TOON with workflow fingerprint, node decisions, waves,
  approvals, derived capabilities and side effects, plus the run-plan
  fingerprint.
- Return validation and handoff summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v2` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

### 0.4 Artifact Routing

- Write generated plans only below `_ai_sdlc/workflows/<workflow-id>/`.
- Keep authored workflow definitions in visible repository-owned paths.
- Never execute or rewrite the authored workflow during planning.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read the owning feature `_ai_sdlc/state.toon` before planning feature work.
- Workflow plans do not advance feature state or runtime task state.

## 0.6 Artifact Metadata And Metatags

- Machine records use `ai-sdlc-workflow/v2` and `ai-sdlc-workflow-plan/v2`.
- Workflow-related Markdown uses canonical `artifact_metadata` and `metatags`
  when authored.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` before resolving feature-local actions and
  use feature-local `index.md` for human review.
- Planning does not refresh either specs index.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
