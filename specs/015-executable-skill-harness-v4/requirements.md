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
  at: "2026-07-30T08:41:38Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "015-executable-skill-harness-v4"
  artifact: "requirements.md"
  path: "specs/015-executable-skill-harness-v4/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/015-executable-skill-harness-v4/_ai_sdlc/state.toon"
  decision_log: "specs/015-executable-skill-harness-v4/decision-log.md"
  status: "review"
  owner: "Repository Maintainers"
  created_at: "2026-07-30"
  updated_at: "2026-07-30"
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
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
    - "NFR-008"
  related_artifacts:
    - "specs/015-executable-skill-harness-v4/branch-plan.md"
    - "specs/015-executable-skill-harness-v4/decision-log.md"
    - "specs/015-executable-skill-harness-v4/design.md"
    - "specs/015-executable-skill-harness-v4/index.md"
    - "specs/015-executable-skill-harness-v4/plan.md"
    - "specs/015-executable-skill-harness-v4/qa.md"
    - "specs/015-executable-skill-harness-v4/research.md"
    - "specs/015-executable-skill-harness-v4/tasks.md"
    - "specs/015-executable-skill-harness-v4/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "review"
    - "harness-v4"
---

# Requirements

## Goal
Turn all 44 AI SDLC skills into a deterministic executable v4 harness whose semantic steps, context, gates, side effects, evidence, and handoffs can be selected, resumed, and evaluated.

## Problem Statement
The current skill manifests expose mostly prepare, execute, and validate documents while many real procedures remain numbered prose inside one execute file. Workflow graphs are plan-only, runtime tasks are not compiled from skill manifests, context selection is not step-owned, and cross-contract drift can pass until a human notices it.

## Scope
- Replace the v1 skill-step extension with a validated v2 DAG and StepCard contract.
- Compile per-step deterministic context and durable run plans.
- Integrate flow, workflow, runtime, host adapter, and handoff contracts.
- Convert and validate all 44 installed skills without retaining an in-runtime legacy reader.
- Add deterministic all-skill evals and a provider-neutral live eval protocol.
- Make canonical TOON the only structured machine-data representation across source, fixtures, contracts, generated artifacts, CLI output, and documentation builds.
- Publish hard-cut v4 compatibility, maintainer, and user documentation.

## Actors
- Agent host: discovers a skill and executes selected StepCards.
- Harness operator: explores intent, approves Apply, resumes or inspects a run.
- Skill author: owns semantic steps, contracts, fixtures, and gates.
- Harness maintainer: owns schemas, generators, compatibility, and release gates.
- Reviewer and QA engineer: inspect traceability, context sufficiency, replay, and eval evidence.

## Inputs
- Skill manifest, semantic step documents, entrypoint, phase, action, and role.
- Repository files and artifact trace IDs eligible for bounded context selection.
- Host capability inventory and explicit Apply authorization.
- Existing run journal, task results, fingerprints, and retry state when resuming.

## Outputs
- A ready StepCard with dependency, operation, context, gate, output, recovery, and side-effect contracts.
- A deterministic context pack or an explicit direct-read decision.
- A durable run v2 journal and replayable result for every Apply-owned step.
- Generated concise routers, drift receipts, deterministic eval receipts, and live-eval protocol results.

## Functional Requirements
- FR-001: Every one of the 44 skills must have an `ai-sdlc-skill-steps/v2` manifest containing a valid acyclic semantic graph, explicit entrypoints, stable step IDs, and at least five executable nodes.
- FR-002: Manifest and step documents must be canonical; SKILL routers and reference projections must be generated and fail validation when stale.
- FR-003: Every ready step must compile a context contract with mandatory anchors, topology and trace selectors, budget, sufficiency rules, critical-anchor recall, and a direct-read fallback.
- FR-004: The selector must compile a stable run v2 task graph with dependencies, max attempts, commit boundaries, outputs, and failure policy.
- FR-005: Runtime must journal every owning-skill step after Apply, including read-only steps, and enforce stable idempotency keys around side effects and resume.
- FR-006: Explore must perform zero durable writes; Apply must validate the decision fingerprint before creating the run and must reject stale exploration.
- FR-007: Flow, workflow, runtime, host adapter, and handoff contracts must exchange the same StepCard, capability, evidence, and status semantics.
- FR-008: A deterministic suite must exercise all 44 skills and a provider-neutral live suite must cover representative lifecycle paths before release.
- FR-009: v4 must be a hard contract cut: older TOON schemas are rejected by expected-versus-received schema checks, with no silent fallback or compatibility reader.
- FR-010: Registries, catalogs, compatibility baselines, decisions, and public documentation must describe the generated-source and release model.
- FR-011: Canonical TOON must be the only structured machine-data representation. Source, fixtures, contracts, CLI modes, generated artifacts, documentation builds, and compatibility checks must contain no alternate serializer, parser, mode, extension, or textual format identifier.

## Non-Functional Requirements
- NFR-001: Identical inputs and repository bytes must produce byte-stable selection, graph fingerprints, context packs, plans, and deterministic eval results.
- NFR-002: Durable state must be TOON serializable, append-only where journaled, path-contained, replayable, and safe under interrupted retries.
- NFR-003: The deterministic core must use local standard-library logic only; it may not require embeddings, network access, or a model call.
- NFR-004: A packed context is sufficient only with 100 percent critical-anchor recall and at least 15 percent net token savings; otherwise the StepCard requires direct reading.
- NFR-005: Validation must cover schema, semantics, drift, replay, security boundaries, all-skill conversion, and representative live behavior with auditable receipts.
- NFR-006: Explore must be verifiably zero-write and Apply must make every durable mutation attributable to a run and step.
- NFR-007: Contracts must work in source checkout and installed `.agents/skills` layouts without host-specific Python packages.
- NFR-008: Every tracked or generated TOON artifact must decode and canonicalize deterministically, and repository plus documentation-build scans must prove the absence of alternate machine-format artifacts and identifiers.

## Constraints
- Preserve the public inventory of 44 skills and their current lifecycle ownership.
- Keep concise Agent Skills compatible `SKILL.md` frontmatter and progressive disclosure.
- Use canonical repository writers for generated indexes and script-owned SDD artifacts.
- Use one shared canonical TOON codec for machine-readable contracts, fixtures, state, journals, receipts, and CLI output.
- Do not add a distributed scheduler, external vector store, hidden telemetry, implicit permission expansion, or alternate serialization compatibility layer.
- Treat all manifest, context, output, and host paths as untrusted until containment checks pass.

## Acceptance Criteria
- AC-001: Given the repository inventory, when v4 validation runs, then exactly 44 manifests pass v2 schema, DAG, path, entrypoint, and minimum semantic-step checks.
- AC-002: Given a skill manifest change, when generated router checks run, then stale or hand-edited router projections are reported and regeneration restores exact output.
- AC-003: Given identical step and repository inputs, when context compiles twice, then output and fingerprint are byte-identical and every mandatory critical anchor is present or execution is blocked.
- AC-004: Given a packed context with less than 15 percent savings or incomplete critical anchors, when sufficiency is evaluated, then the StepCard selects direct reading and records the reason.
- AC-005: Given an approved Apply, when a graph compiles and runs, then every selected step receives one stable task identity and start, terminal, evidence, and result journal records.
- AC-006: Given an interrupted or repeated side-effecting step, when the run resumes, then completed results are reused and the idempotency key prevents duplicate effects.
- AC-007: Given Explore-only commands, when filesystem snapshots are compared, then no run, journal, cache, lock, state, or derived context file was created or modified.
- AC-008: Given repository or decision drift between Explore and Apply, when Apply validates the fingerprint, then it rejects execution before run creation.
- AC-009: Given flow, workflow, runtime, adapter, and handoff fixtures, when contract integration runs, then StepCard fields, capabilities, status, evidence, and failure semantics agree.
- AC-010: Given an older TOON schema at a v4 entrypoint, when it is loaded, then canonical TOON decoding is followed by an explicit expected-versus-received schema rejection, no compatibility reader is invoked, and no output is written.
- AC-011: Given the deterministic eval suite, when it runs offline, then all 44 skills cover happy, blocked, invalid, resume, and context-sufficiency scenarios with TOON receipts.
- AC-012: Given a release candidate, when the provider-neutral live protocol runs on the representative skill set, then routing, step compliance, evidence, recovery, and context quality are scored and recorded without changing deterministic core output.
- AC-013: Given the complete repository and a strict documentation build, when the TOON-only gate runs, then no alternate-format extension or identifier exists, every `.toon` file decodes, and canonical decode-encode output is byte-stable for repository-owned generated artifacts.

## Out of Scope
- A general distributed workflow engine or remote persistence service.
- Embedding or model-based retrieval inside deterministic selection.
- Certification of every model, provider, or agent host in repository tests.
- Automatic sub-agent delegation, background network actions, or broader permissions.
- Backward-compatible execution or in-runtime conversion of pre-v4 machine contracts after the hard cut.

## Assumptions
- The approved plan is the decision-complete product input, so upstream discovery interviews may be skipped with DEC-001 trace.
- Existing skill procedures remain authoritative domain content while their execution boundaries are decomposed.
- Five semantic nodes is the minimum useful portable graph; complex skills may define more.
- Provider-neutral live eval definitions belong in the repository while provider credentials and certification receipts remain release-owner inputs.

## Open Questions
- OQ-001: Release maintainers own the provider and model certification matrix; resolution is required for a release receipt but does not block deterministic v4 implementation.

## Decision Status
All blocking implementation decisions are resolved. DEC-001 accepts quick-flow from the approved plan; DEC-002 accepts manifest and step docs as canonical; DEC-003 accepts durable per-step journaling; DEC-004 accepts deterministic lexical JIT context with strict fallback; DEC-005 accepts two-tier evals; DEC-006 preserves Explore zero-write and Apply-only run creation; DEC-007 accepts canonical TOON as the sole structured machine-data representation with a repository-wide absence and canonicalization gate; DEC-009 preserves immutable v4.0.0 and publishes the native TOON-only installer as corrective v4.0.1 history.
