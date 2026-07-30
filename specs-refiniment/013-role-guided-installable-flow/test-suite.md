---
type: "ai-sdlc.test-suite"
title: "Test Suite"
description: "Executable smoke, regression, and acceptance suite definitions."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-27T12:13:45Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "013-role-guided-installable-flow"
  artifact: "test-suite.md"
  path: "specs-refiniment/013-role-guided-installable-flow/test-suite.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-case-and-suite-synthesis"
  flow_mode: "full"
  state_file: "specs-refiniment/013-role-guided-installable-flow/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/013-role-guided-installable-flow/decision-log.md"
  status: "review"
  owner: "QA Engineer"
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
    - "TC-001"
  related_artifacts:
    - "specs-refiniment/013-role-guided-installable-flow/backlog-gap-review.md"
    - "specs-refiniment/013-role-guided-installable-flow/backlog.md"
    - "specs-refiniment/013-role-guided-installable-flow/business-context.md"
    - "specs-refiniment/013-role-guided-installable-flow/decision-log.md"
    - "specs-refiniment/013-role-guided-installable-flow/delivery-gap-review.md"
    - "specs-refiniment/013-role-guided-installable-flow/delivery-spec.md"
    - "specs-refiniment/013-role-guided-installable-flow/discovery.md"
    - "specs-refiniment/013-role-guided-installable-flow/goal-capability-map.md"
    - "specs-refiniment/013-role-guided-installable-flow/prfaq.md"
    - "specs-refiniment/013-role-guided-installable-flow/qa-gap-review.md"
    - "specs-refiniment/013-role-guided-installable-flow/qa-strategy.md"
    - "specs-refiniment/013-role-guided-installable-flow/qa.md"
    - "specs-refiniment/013-role-guided-installable-flow/release-slicing.md"
    - "specs-refiniment/013-role-guided-installable-flow/requirements-readiness.md"
    - "specs-refiniment/013-role-guided-installable-flow/test-cases.md"
    - "specs-refiniment/013-role-guided-installable-flow/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-test-case-and-suite-synthesis"
    - "test-suite"
    - "review"
---

# test-suite.md

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
  - `specs-refiniment/013-role-guided-installable-flow/delivery-spec.md`.
  - `specs-refiniment/013-role-guided-installable-flow/qa.md`.
  - `specs-refiniment/013-role-guided-installable-flow/qa-gap-review.md`.
  - `specs-refiniment/013-role-guided-installable-flow/qa-strategy.md`.
  - `specs-refiniment/013-role-guided-installable-flow/test-cases.md`.

## Suite Coverage Matrix
| Suite | Purpose | Test IDs | Trigger | Environment | Owner |
| --- | --- | --- | --- | --- | --- |
| Feature 013 suite | Feature 013 purpose | TC-001 | Feature 013 trigger | Feature 013 environment | QA Engineer |

- The matrix is bounded to the accepted Feature 013 scope and traces to DEC-001.

## Smoke Suite
- Flow `--help`, clear Explore, ambiguous Explore, SDD helper import, and runtime state helper status.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Regression Suite
- All shared/runtime tests, every skill tests, flow V2, context, docs, and install/update checks.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## UAT Suite
- A contributor selects each role path, reviews context evidence, accepts a handoff, and executes one revalidated checkpoint.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Entry Criteria
- Feature code and SDD artifacts complete; temporary environments available; no unrelated dirty changes.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Exit Criteria
- All suites pass on the exact revision and residual risks are explicit.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Execution Dependencies
- Runtime consolidation and generated docs must be current before installation suites run.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.
