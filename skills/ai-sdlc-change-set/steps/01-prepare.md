# Prepare — ai-sdlc-change-set: Isolated Change Workspace

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Repository root and a lowercase hyphenated change ID.
- Change title, summary, owner, and one or more repository-relative canonical
  target paths.
- Quick or full flow selection when organization policy requires it.

### 0.2 Clarification Rules

- Ask when the owner, target authority, or intended outcome is ambiguous.
- Reject absolute paths, parent traversal, targets inside `changes/`, and
  duplicate targets instead of normalizing them silently.
- Treat generated workspace content as a proposal until a later controlled
  apply workflow proves approval and conflict freedom.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow may create a draft from confirmed repository context and visible
  assumptions.
- Full flow requires explicit owner, summary, and canonical targets.
- Neither flow reads, writes, renames, or deletes canonical targets.

### 0.3 Output Rules

- Report the change ID, workspace path, status, owner, targets, fingerprint,
  validation result, and next required action.
- Before the final response, emit an `ai-sdlc-handoff/v1` result that routes a
  structurally valid workspace to delta authoring and validation. Include
  `next_required` and `next_optional` actions with reasons, commands, and
  expected artifacts.
- Return progress, validation, and handoff summaries directly in the active agent response.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.
- Do not create ad hoc summaries outside the canonical workspace files.

### 0.4 Artifact Routing

- Route every change to `<repository>/changes/<change-id>/`.
- Keep human intent in `proposal.md`, `design.md`, `tasks.md`,
  `deltas/index.md`, and `evidence/index.md`.
- Keep complete agent-facing TOON beside interoperable JSON for the change set,
  delta set, apply preview, approval, and recovery records.
- Never store a change workspace inside `specs/`, `specs-refiniment/`, or a
  canonical target directory.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Change status begins as `draft` in the change-set record.
- T002 creates only the intake state; later delta, preview, apply, and archive
  tasks own their state transitions.
- Read the owning feature `_ai_sdlc/state.toon` when targets belong to an
  existing feature, but do not modify feature `state.toon` during intake.

## 0.6 Artifact Metadata And Metatags

- Generated Markdown starts with `artifact_metadata` frontmatter using
  `ai-sdlc-change-set-metadata/v1`.
- Include change ID, artifact, status, owner, created and updated dates,
  canonical targets, and `metatags` for `ai-sdlc`, `change-set`, `proposal`,
  and `draft`.
- The JSON record uses schema `ai-sdlc-change-set/v1` and a deterministic
  contract fingerprint.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for human
  feature discovery when canonical targets belong to existing specs.
- A draft change workspace is not a feature spec and does not refresh either
  specs index.
- The later apply workflow refreshes indexes only after an approved canonical
  artifact change.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
