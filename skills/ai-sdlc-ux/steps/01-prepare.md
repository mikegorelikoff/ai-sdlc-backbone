# Prepare — ai-sdlc-ux: Traceable Experience Specification

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Owning feature root.
- UX input using `ai-sdlc-ux-input/v1`.
- Actors and requirement or acceptance trace targets.

### 0.2 Clarification Rules

- Resolve discoverable facts and reuse inherited decisions before asking.
- Missing optional context stays optional; label assumptions explicitly.
- Pause only work dependent on a missing material input or conflicting requirement.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.


### 0.3 Output Rules

- Return actors, journey/state coverage, accessibility status, blockers, and
  output paths directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v2` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or untraced mockup prose.
- Keep behavior testable and avoid presenting assumptions as research.

### 0.4 Artifact Routing

- Write `<feature-root>/ux-spec.md`.
- Write `<feature-root>/_ai_sdlc/ux-spec.toon`.
- Use the owning workspace selected by the feature; implementation UX supports SDD.
- Keep generated image/design files separate and link them as evidence when present.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read `<feature-root>/_ai_sdlc/state.toon` before durable work.
- UX is an optional capability and does not add a core lifecycle stage.
- `--state-check` is read-only; `--begin-state` and `--complete-state` are rejected.
- Route accepted behavior changes through owning requirements and change-impact workflows.

## 0.6 Artifact Metadata And Metatags

- Markdown starts with `artifact_metadata` using schema `ai-sdlc-ux-metadata/v1`.
- Include `metatags` for `ai-sdlc`, `ux`, `experience`, and `traceable`.
- Record feature, workspace, flow mode, state file, trace IDs, and review status.

## 0.7 Specs Index

- Read the relevant `specs/_ai_sdlc/specs-index.toon` or
  `specs-refiniment/_ai_sdlc/specs-index.toon` before broad reads.
- Refresh the matching `specs/<feature-name>/index.md` or
  `specs-refiniment/<feature-name>/index.md` only after durable writes.
- Keep one UX artifact in the owning feature boundary.

## Execution contract

Do not use it while actors, workflows, or business rules are unclear. Use `ai-sdlc-ba` instead. Do not use it to implement interface code. Use `ai-sdlc-sdd` instead.

Read the [shared execution decisions](../../ai-sdlc-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
