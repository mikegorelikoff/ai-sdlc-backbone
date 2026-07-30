---
type: "ai-sdlc.delivery-spec"
title: "Delivery Specification"
description: "Structured implementation and cross-functional delivery contract."
tags:
  - "ai-sdlc"
  - "requirements"
  - "delivery"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-27T12:13:45Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "013-role-guided-installable-flow"
  artifact: "delivery-spec.md"
  path: "specs-refiniment/013-role-guided-installable-flow/delivery-spec.md"
  workspace: "refinement"
  skill: "ai-sdlc-delivery-spec-synthesis"
  flow_mode: "full"
  state_file: "specs-refiniment/013-role-guided-installable-flow/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/013-role-guided-installable-flow/decision-log.md"
  status: "review"
  owner: "Business Analyst"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "BR-001"
    - "BR-002"
    - "BR-003"
    - "BR-004"
    - "BR-005"
    - "DEC-001"
    - "REQ-001"
    - "REQ-002"
    - "REQ-003"
    - "REQ-004"
    - "RISK-001"
    - "RISK-002"
    - "RISK-003"
  related_artifacts:
    - "specs-refiniment/013-role-guided-installable-flow/backlog-gap-review.md"
    - "specs-refiniment/013-role-guided-installable-flow/backlog.md"
    - "specs-refiniment/013-role-guided-installable-flow/business-context.md"
    - "specs-refiniment/013-role-guided-installable-flow/decision-log.md"
    - "specs-refiniment/013-role-guided-installable-flow/delivery-gap-review.md"
    - "specs-refiniment/013-role-guided-installable-flow/discovery.md"
    - "specs-refiniment/013-role-guided-installable-flow/goal-capability-map.md"
    - "specs-refiniment/013-role-guided-installable-flow/prfaq.md"
    - "specs-refiniment/013-role-guided-installable-flow/release-slicing.md"
    - "specs-refiniment/013-role-guided-installable-flow/requirements-readiness.md"
    - "specs-refiniment/013-role-guided-installable-flow/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-delivery-spec-synthesis"
    - "delivery-spec"
    - "review"
---

# delivery-spec.md

## Feature Summary
- REQ-001: Replace the dual `_shared`/runtime authority with one installable canonical runtime.
- REQ-002: Route through exactly one active canonical role and preserve cross-role work as explicit handoffs.
- REQ-003: Load only the selected role reference and current workflow step while explaining context economics.
- REQ-004: Publish a breaking `ai-sdlc-flow/v3` card during the release-candidate line.

## Actors and Stakeholders
- Product Manager: owns customer problem, outcomes, and product trade-offs.
- Product Owner: owns delegated backlog ordering and acceptance clarity.
- Business Analyst: owns actor, workflow, rule, and exception analysis.
- QA Engineer: owns independent testability and quality-evidence recommendations.
- Software Engineer: owns technical design, implementation, validation, and engineering-risk escalation.
- Harness Maintainer: owns package compatibility, schemas, generated docs, and release validation.

## Scope and Boundaries
- In scope: canonical runtime consolidation; five neutral role contracts; selector registry; JIT steps; bounded config; V2 card; install and documentation validation.
- Out of scope: new installable role skills, a replacement navigator, fictional personas, arbitrary team-defined actions, permission expansion, deployment, or telemetry upload.

## Workflows and Failure Paths
- Clear intent -> requested action -> state/prerequisite resolution -> exactly one active role -> selected step -> V2 DecisionCard -> fingerprinted Apply.
- Ambiguous intent -> role/action menu; no mutation until resolved.
- Missing runtime -> fail with the exact companion install instruction.
- Selector/config/reference/state drift -> reject Apply and require a fresh Explore.
- Cross-role prerequisite -> preserve requested role/action and show the prerequisite owner as the next active role.

## Requirements and Business Rules
- BR-001: The installed skill inventory remains 44; role contracts are references, not entrypoint skills.
- BR-002: Exactly one `active_role` is emitted; other roles appear only in handoffs.
- BR-003: Package-owned role/action/skill and step mappings cannot be overridden by project configuration.
- BR-004: V1 cards are rejected with a rerun-Explore diagnostic.
- BR-005: Direct reading wins unless packed context retains every critical anchor and saves at least 15% net tokens.

## Data, Integrations, and Non-Functional Requirements
- Machine contracts use versioned TOON schemas; agent-facing status remains Markdown/TOON.
- Selector and referenced-step paths must stay within the installed flow skill and reject symlink escape.
- Context selector globs are repository-relative, bounded to 16..4000 tokens, and treated as untrusted evidence.
- Deterministic output and fingerprints must be stable for identical repository, selector, config, and intent inputs.

## Dependencies, Risks, and Constraints
- Depends on Skills CLI discovery by `SKILL.md`, the existing context engine, state machine, artifact/index helpers, and documentation generator.
- Risk RISK-001: removing `_shared` touches every deterministic helper import and CI path.
- Risk RISK-002: selector drift could route the right intent to the wrong owner or skill.
- Risk RISK-003: overly broad context selectors could recreate the unreadable context problem.
- Mitigation: schema coverage, import smoke tests, exact mapping tests, bounded JIT context, and full installation validation.

## Decisions, Assumptions, and Open Questions
- DEC-001 accepted: five role references, one active role, automatic selection with explicit override, menu only when unclear, bounded configuration, canonical runtime, and V2 hard cut.
- DEC-003 accepted: all durable runtime-generated Markdown is native OKF v0.2; feature, change, and runtime directories are independent bundles with progressive reserved indexes.
- No blocking product questions remain; implementation evidence may refine technical details without changing these accepted boundaries.

## Success Measures
- AC-001: full and selective installations execute flow and SDD helpers without `_shared`.
- AC-002: clear requests select one role/action; ambiguous requests expose a deterministic menu.
- AC-003: JIT output names one current step and selected role reference and explains every skipped reference.
- AC-004: packed context is accepted only at 100% critical-anchor recall and >=15% net savings.
- AC-005: 44-skill inventory, docs generation, all skill tests, and installed workflow smoke pass.

## Source Coverage
- Sources consumed:
  - Active user feedback and accepted implementation plan dated 2026-07-27.
  - `skills/ai-sdlc-flow/SKILL.md` and `skills/ai-sdlc-flow/scripts/flow.py`.
  - `skills/_shared/` and `skills/ai-sdlc-shared-runtime/` packaging evidence.
  - `docs/roles/`, `docs/reference/skills-by-role.md`, and `docs/scripts/build_catalog.py`.
  - `specs-refiniment/013-role-guided-installable-flow/decision-log.md`.
  - `specs-refiniment/013-role-guided-installable-flow/discovery.md`.
  - `specs-refiniment/013-role-guided-installable-flow/prfaq.md`.
  - `specs-refiniment/013-role-guided-installable-flow/delivery-gap-review.md`.
  - `specs-refiniment/013-role-guided-installable-flow/requirements-readiness.md`.
  - `specs-refiniment/013-role-guided-installable-flow/goal-capability-map.md`.
  - `specs-refiniment/013-role-guided-installable-flow/backlog-gap-review.md`.
  - `specs-refiniment/013-role-guided-installable-flow/backlog.md`.
  - `specs-refiniment/013-role-guided-installable-flow/user-stories.md`.
  - `specs-refiniment/013-role-guided-installable-flow/release-slicing.md`.
  - `specs-refiniment/013-role-guided-installable-flow/business-context.md`.

## Requirement Detail
| Requirement ID | Actor/System | Requirement | Source | Priority | Acceptance Ref |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | Feature 013 actor/system | REQ-001 | DEC-001 and accepted plan | must | AC-001 |

- The matrix is bounded to the accepted Feature 013 scope and traces to DEC-001.

## Workflow Detail
| Workflow ID | Trigger | Actor | Steps | End State | Exceptions | Requirement Ref |
| --- | --- | --- | --- | --- | --- | --- |
| Feature 013 workflow id | Feature 013 trigger | Feature 013 actor | Feature 013 steps | Feature 013 end state | Feature 013 exceptions | Feature 013 requirement ref |

- The matrix is bounded to the accepted Feature 013 scope and traces to DEC-001.

## Business Rule Detail
| Rule ID | Rule | Applies To | Source | Failure Behavior | Decision Ref |
| --- | --- | --- | --- | --- | --- |
| Feature 013 rule id | Feature 013 rule | Feature 013 applies to | DEC-001 and accepted plan | Feature 013 failure behavior | DEC-001 |

- The matrix is bounded to the accepted Feature 013 scope and traces to DEC-001.

## User Story Traceability
- User Story Traceability is defined by REQ-001..REQ-004, AC-001..AC-005, and DEC-001 with no blocking gap.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Acceptance Traceability
- Acceptance Traceability is defined by REQ-001..REQ-015, AC-001..AC-022, DEC-001, and DEC-003 with no blocking gap.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## QA and Operational Notes
- Validate selector determinism, negative cases, context economics, source/selective/global installations, and generated documentation.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Handoff Risks
- Primary handoff risks are incomplete import migration and undocumented selector/config incompatibility.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## OKF Delivery Contract

- REQ-012: one standard-library renderer owns OKF v0.2 frontmatter, concept profiles, provenance refresh, verification invalidation, and preservation of unknown extensions.
- REQ-013: each `specs/<feature>/`, `specs-refiniment/<feature>/`, `changes/<change>/`, and `_ai_sdlc/` tree is an independently valid bundle. Reserved `index.md` files provide human navigation; compact workspace routing remains TOON-only.
- REQ-014: write-capable commands accept `--generated-by`; absent overrides preserve an existing valid actor or default to `process:ai-sdlc`. Lifecycle state never implies `verified`.
- REQ-015: project context exists only at `_ai_sdlc/context/project-context.md`, module knowledge only at `_ai_sdlc/modules.md`, and runtime code has no legacy path fallback.
- The first durable write to a legacy feature preflights and migrates the complete feature bundle. Any conflict aborts before mutation.

## OKF Acceptance Detail

| Acceptance | Required outcome |
| --- | --- |
| AC-017 | Both Feature 013 trees validate as OKF v0.2 bundles and expose deterministic root indexes. |
| AC-018 | Every durable writer family uses an explicit shared concept profile. |
| AC-019 | Actor, timestamp, status, source, extension, and verification semantics pass deterministic unit tests. |
| AC-020 | Human workspace indexes and root project context are absent; only the new routes are supported. |
| AC-021 | Change and runtime trees expose progressive reserved indexes, including valid nested delta/evidence indexes. |
| AC-022 | Legacy first-write migration is complete and atomic, or leaves the original tree byte-identical. |
