# Prepare — ai-sdlc-research: Sourced Delivery Evidence

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Owning feature root.
- Research input using `ai-sdlc-research-input/v1`.
- Verifiable source locators and delivery trace targets.
- Internet access through the host web or browser tool for external or current questions.

### 0.2 Clarification Rules

- Ask when topic, decision to inform, source boundary, or freshness requirement is unclear.
- Separate sourced findings from inference and unresolved questions.
- Record contradictory sources and limitations; do not average them away.
- Do not claim current facts, legal conclusions, or user evidence without verification.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow permits one strong source when scope is explicitly narrow.
- Full flow requires at least two sources and two source types for each report.
- External and mixed scopes require an internet search and at least one direct
  `http://` or `https://` source locator; do not cite search-result pages.
- Both modes require every finding to cite registered sources and trace targets.

### 0.3 Output Rules

- Return question, source, finding, confidence, blocker, and output path counts
  directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or uncited research prose.
- Keep quotes within source rights and use concise paraphrase by default.

### 0.4 Artifact Routing

- Write `<feature-root>/research.md`.
- Write `<feature-root>/_ai_sdlc/research.toon`.
- Keep downloaded or licensed source files outside generated output unless allowed.
- Link research to requirements and decisions; do not overwrite them.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read `<feature-root>/_ai_sdlc/state.toon` before durable research writes.
- Research is optional and does not add a core lifecycle stage.
- `--state-check` is read-only; `--begin-state` and `--complete-state` are rejected.
- Accepted implications move through decisions, requirements, SDD, or change impact.

## 0.6 Artifact Metadata And Metatags

- Markdown starts with `artifact_metadata` using schema `ai-sdlc-research-metadata/v1`.
- Include `metatags` for `ai-sdlc`, `research`, `evidence`, and `traceable`.
- Record feature, workspace, flow mode, state file, trace IDs, and review status.

## 0.7 Specs Index

- Read the relevant `specs/_ai_sdlc/specs-index.toon` or
  `specs-refiniment/_ai_sdlc/specs-index.toon` before broad reads.
- Refresh the matching `specs/specs-index.md` or
  `specs-refiniment/specs-index.md` only after durable writes.
- Keep research inside the feature whose decisions it informs.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
