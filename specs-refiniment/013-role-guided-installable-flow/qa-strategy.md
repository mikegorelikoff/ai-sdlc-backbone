---
type: "ai-sdlc.qa-strategy"
title: "QA Scope and Strategy"
description: "Risk-based QA scope, layers, data, environments, and suite intent."
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
  artifact: "qa-strategy.md"
  path: "specs-refiniment/013-role-guided-installable-flow/qa-strategy.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-scope-and-strategy-design"
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
    - "specs-refiniment/013-role-guided-installable-flow/qa.md"
    - "specs-refiniment/013-role-guided-installable-flow/release-slicing.md"
    - "specs-refiniment/013-role-guided-installable-flow/requirements-readiness.md"
    - "specs-refiniment/013-role-guided-installable-flow/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-test-scope-and-strategy-design"
    - "qa-strategy"
    - "review"
---

# qa-strategy.md

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

## Test Scope
- Unit, schema, routing, state/fingerprint, import, installation, documentation, and manual readability coverage.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Risk and Coverage Priorities
| Risk | Likelihood | Impact | Coverage Layer | Priority | Owner |
| --- | --- | --- | --- | --- | --- |
| Feature 013 risk | Feature 013 likelihood | Feature 013 impact | Feature 013 coverage layer | must | QA Engineer |

- The matrix is bounded to the accepted Feature 013 scope and traces to DEC-001.

## Layer and Suite Strategy
- Unit for pure selectors/config; integration for flow/context/state; smoke for source/selective/global installs; regression for all skills/docs.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Test Data Strategy
- Deterministic intents for all five roles, ambiguous phrases, unsafe configs, stale fingerprints, and disposable repositories.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Environment Dependencies
- Python 3.10+, Git, pinned Skills CLI for installation smoke, and the documented docs environment.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Automation Strategy
- Keep unit/integration tests offline; isolate CLI installation smokes and report network blockers explicitly.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Strategy Risks
- Installation smoke cost and platform variance are controlled by focused local fixtures plus CI coverage.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.
