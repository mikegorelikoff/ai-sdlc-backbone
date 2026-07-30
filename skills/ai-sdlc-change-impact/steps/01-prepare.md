# Prepare — ai-sdlc-change-impact: Evidence-Backed Lifecycle Recovery

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Feature root in `specs/` or `specs-refiniment/`.
- A TOON change set with stable changed references and exact source evidence.
- Readable feature artifacts and, in full flow, canonical lifecycle state.

### 0.2 Clarification Rules

- Ask only when the feature, changed reference, or source evidence is ambiguous.
- Do not infer that an artifact is stale without an exact trace occurrence.
- Report missing state or unowned artifacts as blockers, not guessed stages.
- Preserve multiple changes independently even when they affect one artifact.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow scans feature Markdown and reports missing state as a blocker.
- Full flow requires canonical state plus valid changed-reference source lines.
- Neither mode changes state, artifacts, decisions, tasks, or indexes.

### 0.3 Output Rules

- Return changed refs, stale artifacts, affected stages, blockers, and ordered
  reopen actions directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v2` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or ad hoc recovery files.
- Every affected artifact and reopen action must retain exact evidence.

### 0.4 Artifact Routing

- Write human analysis to `<feature-root>/change-impact.md`.
- Write machine analysis to `<feature-root>/_ai_sdlc/change-impact.toon`.
- Never overwrite the changed source, downstream artifacts, or state.
- Route approved actions through the owning lifecycle skill.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read `<feature-root>/_ai_sdlc/state.toon` before proposing stage actions.
- `--state-check` validates read-only state availability.
- `--begin-state` and `--complete-state` are rejected because analysis cannot
  authorize reopening.
- A `reopen` proposal applies only to a stage currently in a complete state;
  active and not-started stages receive revalidation or pre-start gates.
- The owning workflow records accepted recovery in state and decision log.

## 0.6 Artifact Metadata And Metatags

- Markdown starts with `artifact_metadata` using schema
  `ai-sdlc-change-impact-metadata/v1`.
- Include `metatags` for `ai-sdlc`, `change-impact`, `recovery`, and the affected
  stage identifiers.
- Record feature, workspace, changed refs, state file, and flow mode.

## 0.7 Specs Index

- Read `specs/_ai_sdlc/specs-index.toon` or
  `specs-refiniment/_ai_sdlc/specs-index.toon` before feature analysis.
- Do not refresh `specs/<feature-name>/index.md` or
  `specs-refiniment/<feature-name>/index.md` during read-only analysis.
- The owning workflow refreshes indexes only after an accepted state or
  authoritative artifact change.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
