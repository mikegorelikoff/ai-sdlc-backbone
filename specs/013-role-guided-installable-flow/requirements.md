---
type: "ai-sdlc.requirements"
title: "Requirements"
description: "Implementation requirements, constraints, and acceptance criteria."
tags:
  - "ai-sdlc"
  - "sdd"
  - "requirements"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-27T12:13:45Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "013-role-guided-installable-flow"
  artifact: "requirements.md"
  path: "specs/013-role-guided-installable-flow/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/013-role-guided-installable-flow/_ai_sdlc/state.toon"
  decision_log: "specs/013-role-guided-installable-flow/decision-log.md"
  status: "review"
  owner: "Engineering"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "AC-009"
    - "AC-010"
    - "AC-011"
    - "AC-012"
    - "AC-013"
    - "AC-014"
    - "AC-015"
    - "AC-016"
    - "DEC-001"
    - "DEC-002"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
    - "NFR-008"
    - "REQ-001"
    - "REQ-002"
    - "REQ-003"
    - "REQ-004"
    - "REQ-005"
    - "REQ-006"
    - "REQ-007"
    - "REQ-008"
    - "REQ-009"
    - "REQ-010"
    - "REQ-011"
  related_artifacts:
    - "specs/013-role-guided-installable-flow/branch-plan.md"
    - "specs/013-role-guided-installable-flow/code-review.md"
    - "specs/013-role-guided-installable-flow/decision-log.md"
    - "specs/013-role-guided-installable-flow/design.md"
    - "specs/013-role-guided-installable-flow/plan.md"
    - "specs/013-role-guided-installable-flow/qa.md"
    - "specs/013-role-guided-installable-flow/tasks.md"
    - "specs/013-role-guided-installable-flow/test-cases.md"
    - "specs/013-role-guided-installable-flow/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "review"
    - "accepted"
---

# Requirements

## Goal
Deliver an installable and understandable AI SDLC flow in which one canonical runtime supports every skill, one active role guides each turn, and only the current role, skill step, and selected references enter context. Every installable skill must expose a concise SKILL.md router plus complete just-in-time procedural steps, and every durable runtime-generated Markdown artifact must be portable, typed, progressively discoverable OKF v0.2 knowledge.

## Problem Statement
The current repository has duplicated shared runtime code, an install path that can miss shared dependencies, unclear role and skill sequencing, and broad project-context loading. Users cannot easily predict which skill acts next, why it acts, or which context was selected, and reviewers can be led by opaque AI reasoning.

## Scope
Consolidate the runtime, introduce five role contracts and JIT selectors, cut the decision contract to `ai-sdlc-flow/v2`, add bounded configuration, migrate consumers/tests/docs/CI, verify project/selective/disposable-global installation, migrate all 44 installable skills from monolithic instructions to validated step manifests, and make durable Markdown generators emit conformant OKF v0.2 feature, change, and runtime bundles.

## Actors
- Product/Business Analyst: discovery and requirement framing.
- Product Manager: planning, priority, release, and delivery handoff.
- Software Architect: solution structure, contracts, risks, and migration.
- Software Engineer: implementation, branching, validation, review, and commit preparation.
- QA Engineer: testability, strategy, cases, traceability, and release evidence.
- Repository maintainer: installation, generated documentation, and contract governance.

## Inputs
User intent; explicit `--role` and `--action` overrides; feature state; skill manifests; role, step, and selector registries; bounded `values.flow` configuration; repository artifacts and changed paths.

## Outputs
A deterministic v2 DecisionCard; one active role; an optional explicit role handoff; one current flow step and one selected owning-skill step; selected and skipped context references with reasons; installable runtime assets; a validated step manifest for every installable skill; concise SKILL.md routers; OKF v0.2 knowledge bundles with progressive indexes and trust-aware provenance; updated generated documentation; deterministic validation evidence.

## Functional Requirements
- REQ-001: `skills/ai-sdlc-shared-runtime` is the only shared runtime source; tracked `skills/_shared` and runtime synchronization fallbacks are removed.
- REQ-002: five neutral role contracts define mission, ownership, entry signals, boundaries, workflow, handoffs, selectors, and examples; exactly one role is active per decision.
- REQ-003: a trusted registry selects the current step and bounded references just in time, records selected/skipped items and reasons, and prevents untrusted paths or symlink escapes.
- REQ-004: the flow contract uses `ai-sdlc-flow/v2`; v1 input is rejected with migration guidance; CLI supports `--role`, `--action`, `--team`, and `--user`.
- REQ-005: repository configuration supports only role aliases, menu mode, and bounded context selectors with schema validation and deterministic precedence.
- REQ-006: reference generation and active-skill docs consume the canonical runtime and selector registry.
- REQ-007: full, selective, and disposable-global installation include the shared runtime and leave no dependency on a source checkout.
- REQ-008: every installable skill owns a schema-valid `steps/manifest.json` whose selectors declare phase, role, action, loading rule, token cap, path, and reason.
- REQ-009: every applicable skill moves detailed prepare, execution, validation, and handoff instructions from `SKILL.md` into complete skill-owned step files; `SKILL.md` remains a concise router that names exactly when each step must be read.
- REQ-010: the canonical runtime validates and selects skill steps just in time, and flow decisions include the selected owning-skill step without permitting cross-package path escape.
- REQ-011: generated documentation, installation packaging, compatibility checks, and tests inventory step manifests and detect missing, unlinked, unsafe, oversized, or drifted step files.
- REQ-012: every durable Markdown artifact written by AI SDLC runtime scripts is rendered through one standard-library OKF v0.2 contract with a non-empty top-level `type`, explicit title/description/tags/status/generated provenance, and the existing `artifact_metadata` extension when lifecycle routing applies.
- REQ-013: every feature directory, change workspace, and `_ai_sdlc` runtime knowledge tree is a self-contained OKF bundle with deterministic reserved `index.md` files; workspace `_ai_sdlc/specs-index.toon` remains the compact cross-feature router and human `specs-index.md` projections are removed.
- REQ-014: all write-capable generators accept or inherit `generated.by`, preserve provenance on metadata-only refresh, clear stale verification after meaningful content/source changes, and never infer OKF verification from AI SDLC lifecycle status.
- REQ-015: project context is written only to `_ai_sdlc/context/project-context.md`; legacy root context and human specs-index paths have no runtime read or write fallback, while explicit migration detects divergence before removal or relocation.

## Non-Functional Requirements
- NFR-001 Determinism: identical inputs and configuration produce byte-stable routing fields and fingerprints.
- NFR-002 Safety: selectors are allowlisted, path-contained, file-bounded, and fail closed.
- NFR-003 Transparency: every decision exposes requested and active role, handoff reason, action, flow step, owning-skill step, selected/skipped references, and fingerprints.
- NFR-004 Context economics: the benchmark retains 100% required-reference recall while reducing selected reference tokens by at least 15% from the broad-load baseline.
- NFR-005 Portability: tests never mutate a real home directory and installed skills run without repository-only paths.
- NFR-006 Compatibility discipline: configuration, registry, and manifest errors are actionable; the v1 contract is not silently accepted.
- NFR-007 Progressive disclosure: every SKILL.md is below 120 lines and the aggregate SKILL.md word count is reduced by at least 60% without deleting normative instructions.
- NFR-008 Human readability: each selected step is self-contained, imperative, ordered, and names its entry condition, evidence, actions, validation, and handoff boundary.
- NFR-009 Portability: generated bundles conform to OKF v0.2 without a third-party runtime dependency and preserve unknown producer extensions during refresh.
- NFR-010 Trust integrity: `generated.at` changes only for meaningful content/provenance changes and `verified` never survives a change that invalidates its evidence.
- NFR-011 Index economy: workspace TOON remains compact for routing while bundle-local `index.md` supplies human-readable titles and descriptions without opening every concept.

## Constraints
Python standard library only for runtime changes; existing artifact/state contracts remain supported; public artifacts must be source-neutral; skill inventory remains exactly 44 installable entrypoints; generated files must be drift-checked.

## Acceptance Criteria
- AC-001: no tracked `skills/_shared` path remains and all consumers import the canonical runtime.
- AC-002: full, selective, and disposable-global install smoke tests pass without source-tree fallback.
- AC-003: each of the five roles has a validated contract and exactly one role is active in every v2 decision.
- AC-004: clear intent selects a role/action directly; ambiguous intent produces a deterministic menu; explicit overrides win when valid.
- AC-005: cross-role work emits a documented handoff reason and re-routes through state prerequisites.
- AC-006: the DecisionCard validates as `ai-sdlc-flow/v2`; v1 is rejected with migration guidance.
- AC-007: only the selected current step and allowlisted references are loaded, with selected/skipped reasons and stable fingerprints.
- AC-008: malicious, escaping, oversized, or unknown selectors fail closed with actionable errors.
- AC-009: bounded `values.flow` configuration validates role aliases, menu mode, selector priority, token caps, and unknown keys.
- AC-010: selector benchmark demonstrates 100% required-reference recall and at least 15% token reduction.
- AC-011: generated role/step/selector documentation has no drift and installation docs describe the canonical layout.
- AC-012: focused tests, repository tests, SDD validation, docs validation, and code review pass.
- AC-013: all 44 installable skills contain a schema-valid step manifest; every declared Markdown step is regular, contained, linked from SKILL.md, and selected deterministically.
- AC-014: all SKILL.md routers are below 120 lines and aggregate SKILL.md words fall by at least 60%, while a contract-preservation test proves required lifecycle, safety, script, output, and scope instructions remain present across the router plus selected step resources.
- AC-015: the canonical step selector returns the correct phase/role/action match, selected and skipped reasons, stable fingerprints, and actionable failures for malformed manifests, traversal, symlinks, unknown skills, unknown phases, and token overflow.
- AC-016: flow Explore includes the owning skill step in JIT context; generated skill guides expose selector tables; full/selective/global install smoke and compatibility checks include every step manifest and file.
- AC-017: every non-reserved Markdown file generated inside Feature 013 implementation and refinement bundles has parseable frontmatter with a non-empty top-level `type`; both bundle roots declare `okf_version: "0.2"` in `index.md`.
- AC-018: shared feature writers, specialized feature writers, change-set writers, external snapshots, context/runtime reports, workflow, trust, doctor, adapter, metrics, delivery-graph, and module outputs all use the shared OKF renderer and fail validation when no explicit concept profile exists.
- AC-019: generated actor override/default behavior, meaningful-change timestamps, lifecycle-to-OKF status mapping, source preservation, unknown extension preservation, and verification invalidation pass deterministic unit tests.
- AC-020: `specs/specs-index.md`, `specs-refiniment/specs-index.md`, and root `project-context.md` are absent; the compact v2 TOON indexes and `_ai_sdlc/context/project-context.md` are the only supported generated routes.
- AC-021: `changes/<id>/`, `_ai_sdlc/`, and nested runtime directories generate valid progressive indexes; `deltas/index.md` and `evidence/index.md` use reserved-index structure rather than concept metadata.
- AC-022: an untouched legacy feature remains readable without mutation, while the first durable write migrates the entire feature atomically or fails without a partial bundle when metadata/frontmatter conflicts.

## Out of Scope
Creating role-specific skill duplicates, a separate navigator skill, support for arbitrary user-provided file paths, converting authored repository documentation or skill instruction sources into OKF runtime bundles, changing the 44-skill inventory, preserving flow v1 compatibility, or changing the substantive authority and lifecycle behavior of existing skills.

## Assumptions
Existing skill metadata and state transitions remain authoritative. Role selection guides orchestration but never bypasses lifecycle prerequisites. Repository-relative reference assets are trusted only after registry and containment validation.

## Open Questions
None. Full-flow refinement resolved runtime layout, role set, configuration boundary, contract version, selector policy, context target, and installation matrix.

## Decision Status
DEC-001, DEC-002, and DEC-003 are accepted. Resolved blockers: canonical runtime location, role set, v2 hard cut, selector trust boundary, configuration surface, installation matrix, context-economics threshold, all-skill step applicability, manifest contract, SKILL.md size target, OKF bundle boundaries, provenance behavior, index replacement, and the context path hard cut. Existing lifecycle authority remains unchanged; the new split and OKF layer may relocate but must not weaken normative instructions.
