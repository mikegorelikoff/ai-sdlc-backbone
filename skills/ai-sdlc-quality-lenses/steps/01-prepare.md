# Prepare — ai-sdlc-quality-lenses: Traceable Cross-Artifact Review

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- One readable source artifact.
- One or more lens identifiers from `references/quality-lenses.json`.
- A feature or initiative identifier.
- An owner for every finding.

### 0.2 Clarification Rules

- Ask only when the artifact, review objective, or accountable owner is ambiguous.
- Record uncertainty as a finding; do not invent evidence or trace targets.
- Treat a lens with no supported finding as a valid clean result.
- Do not silently convert a finding into a requirement, decision, or task.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow uses the explicitly selected lenses, or the registry defaults.
- Full flow applies every lens whose `applies_to` includes the artifact kind.
- Both modes use the same finding schema and finalization gates.

### 0.3 Output Rules

- Return selected lenses, finding counts by severity and status, blockers, and
  output paths directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or unregistered review files.
- Never finalize a finding without evidence, severity, trace targets, owner,
  resolution status, and next action.

### 0.4 Artifact Routing

- Default human output: `<artifact-parent>/quality-lens-report.md`.
- Default machine output: `<artifact-parent>/_ai_sdlc/quality-lens-report.toon`.
- Use `--output-root` to route the pair to an owning feature directory.
- Keep the source artifact unchanged; reports are review evidence.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Quality review does not advance lifecycle state by itself.
- Read `_ai_sdlc/state.toon` to understand the current stage and valid owner.
- `--state-check` is read-only; `--begin-state` and `--complete-state` are
  rejected by the report finalizer.
- Route accepted findings to the owning workflow for lifecycle changes.

## 0.6 Artifact Metadata And Metatags

- Markdown starts with `artifact_metadata` using schema
  `ai-sdlc-quality-report-metadata/v1`.
- Include `metatags` for `ai-sdlc`, `quality-lens`, selected lenses, and
  `evidence-backed`.
- Record the source artifact, registry version, feature, flow mode, and trace
  identifiers in metadata.

## 0.7 Specs Index

- Review the relevant `specs/_ai_sdlc/specs-index.toon` or
  `specs-refiniment/_ai_sdlc/specs-index.toon` before broad reads.
- Refresh `specs/specs-index.md` or `specs-refiniment/specs-index.md` only when
  the report is routed into that workspace and the owning workflow requires it.
- Do not use a quality report as a replacement for source requirements,
  decisions, tests, tasks, or state.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
