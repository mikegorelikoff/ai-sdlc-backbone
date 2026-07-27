# Prepare — ai-sdlc-workflow: Declarative Workflow Planning

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Versioned workflow JSON, declared capabilities, typed steps, dependencies,
  bounded conditions, approval gates, and deterministic hook declarations.
- Optional JSON context and explicit host concurrency/isolation capabilities.

### 0.2 Clarification Rules

- Ask when an action, approval owner, or required capability is missing.
- Reject unknown fields, undeclared capabilities, cycles, unsafe identifiers,
  invalid conditions, and hooks without exact targets.
- Never infer approval, shell authority, network authority, or safe isolation.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes use identical validation, cycle, capability, and fallback rules.
- Full flow requires review of every skipped/deferred condition, gate, hook, and fallback.

### 0.3 Output Rules

- Default to complete TOON with workflow fingerprint, step decisions, waves,
  gates, hooks, fallbacks, host capabilities, and plan fingerprint.
- Return validation and handoff summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
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

- Machine records use `ai-sdlc-workflow/v1` and `ai-sdlc-workflow-plan/v1`.
- Workflow-related Markdown uses canonical `artifact_metadata` and `metatags`
  when authored.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` before resolving feature-local actions and
  use `specs-index.md` for human review.
- Planning does not refresh either specs index.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
