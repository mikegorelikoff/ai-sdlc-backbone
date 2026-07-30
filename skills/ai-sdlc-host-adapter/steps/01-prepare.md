# Prepare — ai-sdlc-host-adapter: Portable Host Negotiation

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Versioned adapter manifest and capability request.
- One complete context-ready StepCard, desired concurrency, and isolation need.

### 0.2 Clarification Rules

- Ask when required semantics or host operation identity is ambiguous.
- Reject unknown fields, duplicate operations, invalid API ranges, undeclared
  capabilities, or non-equivalent native mappings.
- Never infer shell, filesystem, network, isolation, concurrency, or approval support.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes use identical compatibility and fallback rules.
- Full flow reviews the StepCard, mapping, derived capability, side-effect,
  evidence, idempotency, limit, fallback, and unsupported-requirement fields.

### 0.3 Output Rules

- Default to complete TOON with mappings, missing requirements, fallbacks,
  effective limits, compatibility, source fingerprint, and result fingerprint.
- Return summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v2` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

### 0.4 Artifact Routing

- Write negotiations only below `_ai_sdlc/adapters/<adapter-id>/`.
- Keep manifests in repository-owned visible paths or skill conformance fixtures.
- Never mutate a manifest during negotiation.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read owning feature `_ai_sdlc/state.toon` before execution handoff.
- Negotiation does not advance feature or runtime state.

## 0.6 Artifact Metadata And Metatags

- Related Markdown uses canonical `artifact_metadata` and `metatags`.
- Machine records use versioned adapter, request, and negotiation schemas.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` first and use feature-local `index.md` for human review.
- Negotiation does not refresh either index.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
