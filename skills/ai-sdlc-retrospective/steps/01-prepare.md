# Prepare — ai-sdlc-retrospective: Reviewable Delivery Learning

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Completed or paused feature root.
- Retrospective JSON containing observations and proposals.
- Exact artifact or validation evidence for every observation.

### 0.2 Clarification Rules

- Ask only when evidence, proposal owner, or intended policy target is unclear.
- Keep observed facts separate from interpretation and proposed change.
- Do not mark a proposal accepted without a durable decision reference.
- Do not infer approval from implementation, silence, or prior chat.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow permits draft proposals but still requires observation evidence.
- Full flow additionally requires every proposal to have an owner and every
  accepted proposal to have a decision reference.
- Neither mode applies proposals or edits target files.

### 0.3 Output Rules

- Return observation and proposal counts, accepted-decision coverage,
  blockers, and output paths directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or policy patches.
- Preserve rejected and deferred proposals for learning history.

### 0.4 Artifact Routing

- Write human output to `<feature-root>/retrospective.md`.
- Write machine output to `<feature-root>/_ai_sdlc/retrospective.toon`.
- Keep proposal target paths as references only.
- Apply accepted improvements later through the target-owning workflow.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Retrospective is a utility workflow and does not advance feature lifecycle.
- Read `_ai_sdlc/state.toon` to confirm feature identity and delivery status.
- `--state-check` is read-only; `--begin-state` and `--complete-state` are
  rejected by the finalizer.
- A proposal decision changes proposal governance status, not lifecycle state.

## 0.6 Artifact Metadata And Metatags

- Markdown starts with `artifact_metadata` using schema
  `ai-sdlc-retrospective-metadata/v1`.
- Include `metatags` for `ai-sdlc`, `retrospective`, `learning`, and proposal
  statuses.
- Record feature, workspace, flow mode, evidence paths, and decision refs.

## 0.7 Specs Index

- Read `specs/_ai_sdlc/specs-index.toon` or
  `specs-refiniment/_ai_sdlc/specs-index.toon` before targeted evidence reads.
- Do not refresh `specs/specs-index.md` or
  `specs-refiniment/specs-index.md` for a read-only draft.
- Refresh indexes only through the owning workflow after durable report writes.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
