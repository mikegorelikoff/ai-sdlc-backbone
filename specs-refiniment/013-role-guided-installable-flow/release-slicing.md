---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "013-role-guided-installable-flow"
  artifact: "release-slicing.md"
  path: "specs-refiniment/013-role-guided-installable-flow/release-slicing.md"
  workspace: "refinement"
  skill: "ai-sdlc-release-slicing-and-backlog-readiness-review"
  flow_mode: "full"
  state_file: "specs-refiniment/013-role-guided-installable-flow/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/013-role-guided-installable-flow/decision-log.md"
  status: "review"
  owner: "Product Owner"
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
    - "specs-refiniment/013-role-guided-installable-flow/decision-log.md"
    - "specs-refiniment/013-role-guided-installable-flow/delivery-gap-review.md"
    - "specs-refiniment/013-role-guided-installable-flow/discovery.md"
    - "specs-refiniment/013-role-guided-installable-flow/goal-capability-map.md"
    - "specs-refiniment/013-role-guided-installable-flow/prfaq.md"
    - "specs-refiniment/013-role-guided-installable-flow/requirements-readiness.md"
    - "specs-refiniment/013-role-guided-installable-flow/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-release-slicing-and-backlog-readiness-review"
    - "release-slicing"
    - "review"
---

# release-slicing.md

## Feature Summary
- REQ-001: Replace the dual `_shared`/runtime authority with one installable canonical runtime.
- REQ-002: Route through exactly one active canonical role and preserve cross-role work as explicit handoffs.
- REQ-003: Load only the selected role reference and current workflow step while explaining context economics.
- REQ-004: Publish a breaking `ai-sdlc-flow/v2` card during the release-candidate line.

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
- Machine contracts use versioned JSON schemas; agent-facing status remains Markdown/TOON.
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

## MVP Slice
- One release-candidate slice delivers canonical runtime, role-guided flow V2, bounded context configuration, documentation, and validation together.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Release Slice Matrix
| Slice | Value | Stories | Dependencies | Exit Criteria | Risks |
| --- | --- | --- | --- | --- | --- |
| Feature 013 slice | Feature 013 value | Feature 013 stories | Feature 013 dependencies | Feature 013 exit criteria | Feature 013 risks |

- The matrix is bounded to the accepted Feature 013 scope and traces to DEC-001.

## Sequencing and Dependencies
- Runtime -> selectors/role cards -> flow V2 -> generated docs -> install and regression validation.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Milestones and Readiness
- M1 runtime imports; M2 selector/role behavior; M3 docs/config; M4 full validation.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Release Risks
- Do not release if any `_shared` operational dependency, V1 acceptance path, inventory drift, or install smoke failure remains.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.

## Release Verdict
- Candidate is releasable only after all feature and repository gates pass.
- Evidence is the accepted plan, inspected repository contracts, and completed upstream Feature 013 artifacts.
