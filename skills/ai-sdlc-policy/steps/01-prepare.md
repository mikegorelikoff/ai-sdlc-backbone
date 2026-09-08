# Prepare — ai-sdlc-policy: Explainable Delivery Controls

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Action name and TOON context for evaluation.
- Base policy plus optional organization profile, project, and user layers.
- Explicit owner-approved waiver record when an allowed exception is requested.

### 0.2 Clarification Rules

- Resolve discoverable facts and reuse inherited decisions before asking.
- Missing optional context stays optional; label assumptions explicitly.
- Pause only work dependent on a missing material input or conflicting requirement.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.


### 0.3 Output Rules

- Report resolved policy fingerprint, layer provenance, action decision, matched
  rules, required gates, reason codes, and applied or rejected waivers.
- Return validation and handoff summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v2` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

### 0.4 Artifact Routing

- Keep approved policy layers in visible repository-owned paths.
- Write generated resolution and decision records only below `_ai_sdlc/`.
- Never overwrite a source policy or waiver during evaluation.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read canonical `_ai_sdlc/state.toon` before applying a decision to feature
  work. Policy evaluation does not create or advance feature `state.toon`.
- A deny or unsatisfied required gate blocks the owning workflow transition.

## 0.6 Artifact Metadata And Metatags

- Policy-related Markdown uses canonical `artifact_metadata` and `metatags`.
- Machine records use `ai-sdlc-policy-layer/v1`, `ai-sdlc-policy-waiver/v1`,
  `ai-sdlc-policy-resolution/v1`, and `ai-sdlc-policy-decision/v1`.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` first and use feature-local `index.md` for human
  discovery when evaluation context refers to feature artifacts.
- Policy evaluation does not refresh either specs index.

## Execution contract

Do not use policy evaluation to create requirements or product decisions. Use the owning refinement or `ai-sdlc-sdd` skill instead.

Read the [shared execution decisions](../../ai-sdlc-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
