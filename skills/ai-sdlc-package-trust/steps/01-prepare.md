# Prepare — ai-sdlc-package-trust: Trusted Packages And Private Metrics

> Selector: prepare, clarify, or route

## Entry

Confirm the requested scope, flow mode, canonical workspace, required evidence, active lifecycle state, and safe runtime layout before acting.

## Procedure

### 0.1 Required Inputs

- Package root, versioned manifest, allowed origins/capabilities, active harness API, and provenance policy.
- Repository-local runtime and evidence records for metrics.

### 0.2 Clarification Rules

- Resolve discoverable facts and reuse inherited decisions before asking.
- Missing optional context stays optional; label assumptions explicitly.
- Pause only work dependent on a missing material input or conflicting requirement.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.


### 0.3 Output Rules

- Default to complete TOON trust decisions or content-free aggregate metrics.
- Return summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v2` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

### 0.4 Artifact Routing

- Write generated decisions and metrics only below `_ai_sdlc/`.
- Never rewrite package files, manifests, runtime records, or evidence ledgers.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read owning feature `_ai_sdlc/state.toon` before using a trust decision.
- Trust and metrics do not advance feature state.

## 0.6 Artifact Metadata And Metatags

- Related Markdown uses canonical `artifact_metadata` and `metatags`.
- Machine records use versioned package, trust-decision, and local-metrics schemas.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` first and use feature-local `index.md` for human review.
- Trust and metrics outputs do not refresh either index.

## Execution contract

Do not use package verification to install, execute, publish, sign, approve, or delete a package. Use the separately authorized package lifecycle workflow instead. Do not use local metrics for content analytics or telemetry upload. Use an approved observability and privacy workflow instead.

Read the [shared execution decisions](../../ai-sdlc-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

Proceed only when inputs, authority, state prerequisites, artifact routes, and context boundaries are explicit; otherwise return the blocker or clarification.
