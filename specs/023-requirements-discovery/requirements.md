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
  at: "2026-09-07T18:25:31Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "023-requirements-discovery"
  artifact: "requirements.md"
  path: "specs/023-requirements-discovery/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/023-requirements-discovery/_ai_sdlc/state.toon"
  decision_log: "specs/023-requirements-discovery/decision-log.md"
  status: "review"
  owner: "implementation agent"
  created_at: "2026-09-07"
  updated_at: "2026-09-07"
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
    - "DEC-002"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
  related_artifacts:
    - "specs/023-requirements-discovery/decision-log.md"
    - "specs/023-requirements-discovery/design.md"
    - "specs/023-requirements-discovery/index.md"
    - "specs/023-requirements-discovery/plan.md"
    - "specs/023-requirements-discovery/qa.md"
    - "specs/023-requirements-discovery/tasks.md"
    - "specs/023-requirements-discovery/test-cases.md"
    - "specs/023-requirements-discovery/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "review"
---

# Requirements

## Goal
Add a requirements discovery assistant to each product skill group: AI SDLC Harness and AI SDLC Loop.

## Problem Statement
Raw feature and task requests need analysis before detailed BA or readiness review: distinguish missing facts, compare business responses using relevant precedents, and prepare questions for the stakeholders who can resolve uncertainty.

## Scope
Two product-local skills with deterministic offline helpers for bounded source preparation, draft scaffolding, typed validation, canonical report generation and freshness verification; executable graphs, installers and documentation.

## Actors
BA leads requirement elicitation; PM/PO owns business choices; stakeholders provide evidence; QA and engineering clarify acceptance and feasibility.

## Inputs
User request in this conversation (no external ticket; documented no-ticket exception), repository skill contracts, product installer sources, and existing BA, discovery and requirements-review workflows.

## Outputs
ai-sdlc-requirements-discovery and ai-sdlc-loop-requirements-discovery; raw-input inventory, sourced precedents, option comparison, prioritized stakeholder questions and a conditional handoff.

## Functional Requirements
- FR-001: Accept raw notes, tickets or feature/task requests without an existing PRD.
- FR-002: Separate facts, assumptions, contradictions, unknowns and proposals with stable source references.
- FR-003: Compare distinct business options using sourced precedents or labeled hypotheses.
- FR-004: Link material gaps and candidate options to stakeholder questions, priorities, evidence locations and methods.
- FR-005: Keep recommendations conditional and choices unaccepted without a recorded owner response.
- FR-006: Install both namespaced products without a mandatory new lifecycle stage.
- FR-007: Prepare byte-stable source contexts and draft skeletons through product-local scripts; bind source paths and exact content digests.
- FR-008: Reject invalid schemas/types, duplicate IDs, dangling references, incomplete elicitation coverage, unsupported precedent outcomes and unsupported acceptance records.
- FR-009: Finalize canonical TOON from validated analysis and generate Harness Markdown through the script; verify current source freshness and report fingerprints.
- FR-010: Keep commands read-only by default; explicit writes are contained, atomic, idempotent for identical output and require explicit replacement for different existing output.

## Non-Functional Requirements
- NFR-001: Preserve existing stage, install profile, approval, navigation and public paths.
- NFR-002: No fabricated source access, outcomes, stakeholder replies or authority.
- NFR-003: Keep routers below 120 lines and use five-node v2 manifests.
- NFR-004: Identical source bytes, paths, analysis and explicit date produce identical canonical bytes regardless of input list order or absolute project location; no clock, randomness, network or model call in deterministic helpers.
- NFR-005: Validate UTF-8, bounded input size, symlink/traversal and protected output paths; malformed input must fail without partial output.

## Constraints
Loop is a separate Git submodule. Its machine artifacts remain TOON. Harness refinement artifacts stay under specs-refiniment. Work remains on branches based on the current product tips containing the unreleased quality gate.

## Acceptance Criteria
- AC-001: Given either installed skill, when the v2 selector runs, then dependency-ready steps return without errors.
- AC-002: Given raw input, when analyzed, then source-linked observations, business options and targeted stakeholder questions are present.
- AC-003: Given missing history or owner replies, when finalized, then the output retains explicit unknowns and grants no implementation approval.
- AC-004: Given a supported installation profile, when installed, then the product includes its helper and sibling runtime and preserves unrelated skills.
- AC-005: Given source changes, when catalogs and docs checks run, then both capabilities remain discoverable with valid paths.
- AC-006: Given equivalent source/draft inputs in different argument or collection order, when preparation and finalization repeat, then canonical bytes and fingerprints are equal.
- AC-007: Given malformed types, IDs, references, missing option/gap question coverage or unsupported acceptance, when validated or finalized, then exit is nonzero and no report is written.
- AC-008: Given a finalized report, when a bound source changes or the report is tampered with, then verify fails read-only.
- AC-009: Given unsafe paths, symlinks, collisions or a write failure, when output is requested, then unrelated files remain untouched and partial reports are rolled back.

## Out of Scope
Committing, publishing or resuming the stopped release; running a real customer discovery; stakeholder communication; making business reasoning itself deterministic; replacing the lifecycle runtimes.

## Assumptions
- A-001: Each product means Harness and Loop in this checkout.
- A-002: One coherent assistant covers input analysis, options and stakeholder elicitation.
- A-003: Model judgment is explicit draft data; scripts validate and serialize it without inventing business content.
- A-004: External evidence enters as explicitly provided local UTF-8 snapshots; helpers make no network calls.

## Open Questions
No blocking questions for this bounded addition. Product decisions elicited by future use remain with that feature's owner.

## Decision Status
Resolved blockers: the missing deterministic contract is addressed by DEC-002. Accepted assumptions: A-001 through A-004. Commit and release stay paused after the user's stop.
