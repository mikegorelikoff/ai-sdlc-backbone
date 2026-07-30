# Prepare — ai-sdlc-architecture: Traceable System Design

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Implementation feature root.
- Architecture input using `ai-sdlc-architecture-input/v1`.
- Requirement, acceptance, risk, or decision trace targets.

### 0.2 Clarification Rules

- Ask when system boundary, quality attribute, authority, or irreversible choice is ambiguous.
- Separate constraints from decisions and decisions from implementation tasks.
- Record alternatives and consequences for every material decision.
- Do not invent infrastructure, data classification, or production topology.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow permits a bounded architecture slice with explicit gaps.
- Full flow requires at least one decision, risk, and validation check.
- Both modes require trace targets for constraints, interfaces, decisions, and risks.

### 0.3 Output Rules

- Return design scope, decision/risk counts, blockers, validation status, and
  output paths directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v2` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or untraced diagrams.
- Keep Markdown authoritative for detail and TOON bounded for routing.

### 0.4 Artifact Routing

- Write `<feature-root>/architecture.md`.
- Write `<feature-root>/_ai_sdlc/architecture.toon`.
- Keep ADRs or decision-log entries separate when organizational authority
  requires them; link their IDs from architecture decisions.
- Do not write into refinement unless architecture work is explicitly upstream.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read `<feature-root>/_ai_sdlc/state.toon` before architecture work.
- Architecture is an optional design utility and does not add a core lifecycle stage.
- `--state-check` is read-only; `--begin-state` and `--complete-state` are rejected.
- Route accepted design changes back through SDD and change-impact recovery.

## 0.6 Artifact Metadata And Metatags

- Markdown starts with `artifact_metadata` using schema
  `ai-sdlc-architecture-metadata/v1`.
- Include `metatags` for `ai-sdlc`, `architecture`, `design`, and `traceable`.
- Record feature, workspace, flow mode, state file, trace IDs, and status.

## 0.7 Specs Index

- Read `specs/_ai_sdlc/specs-index.toon` and feature state before broad reads.
- Refresh `specs/<feature-name>/index.md` only after a durable architecture write.
- Do not alter `specs-refiniment/_ai_sdlc/specs-index.toon` or
  `specs-refiniment/<feature-name>/index.md` for implementation-owned architecture.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
