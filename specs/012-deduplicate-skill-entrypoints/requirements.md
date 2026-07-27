---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "012-deduplicate-skill-entrypoints"
  artifact: "requirements.md"
  path: "specs/012-deduplicate-skill-entrypoints/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/012-deduplicate-skill-entrypoints/_ai_sdlc/state.toon"
  decision_log: "specs/012-deduplicate-skill-entrypoints/decision-log.md"
  status: "review"
  owner: "Repository Maintainers"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "DEC-001"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
  related_artifacts:
    - "specs/012-deduplicate-skill-entrypoints/branch-plan.md"
    - "specs/012-deduplicate-skill-entrypoints/decision-log.md"
    - "specs/012-deduplicate-skill-entrypoints/design.md"
    - "specs/012-deduplicate-skill-entrypoints/plan.md"
    - "specs/012-deduplicate-skill-entrypoints/qa.md"
    - "specs/012-deduplicate-skill-entrypoints/tasks.md"
    - "specs/012-deduplicate-skill-entrypoints/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "review"
    - "deduplication"
---

# Requirements

## Goal
Reduce public skill-selection ambiguity by exposing one canonical guided entrypoint.

## Problem Statement
`ai-sdlc-flow` and `ai-sdlc-navigator` both classify intent and recommend the next owning skill, creating two competing entrypoints after feature 011.

## Scope
Migrate navigator-only intent routes and repository context signals into flow; remove the navigator package and every inventory, compatibility, install, catalog, documentation, and test reference.

## Actors
Contributors use flow; repository maintainers own routing and compatibility; downstream owning skills remain unchanged.

## Inputs
All 45 repo-local SKILL.md files, module manifests, managed-skill lists, compatibility baseline, installer smoke checks, generated catalogs, docs, and navigator/flow tests.

## Outputs
One `ai-sdlc-flow` entrypoint with complete routing coverage; 44 unique skills; migration guidance from navigator to flow; regenerated inventories.

## Functional Requirements
- FR-001: `ai-sdlc-flow` must cover every unique navigator intent route before removal.
- FR-002: Remove `skills/ai-sdlc-navigator/` and all registry, baseline, install, catalog, documentation, and test references.
- FR-003: Preserve direct owning-skill invocation and protected CLI flags.
- FR-004: Preserve read-only Explore and one-action Apply semantics.
- FR-005: Keep shared-runtime mirrors because project-scoped installation requires them.
- FR-006: Add migration guidance naming `ai-sdlc-flow` as the replacement.

## Non-Functional Requirements
- NFR-001: No duplicate declared skill IDs or semantic routing entrypoints remain.
- NFR-002: Compatibility, module, docs, install-smoke, and per-skill tests pass.
- NFR-003: Generated catalogs report 44 skills.
- NFR-004: Routing output remains deterministic and readable.

## Constraints
The physical `specs-refiniment` path and installed shared-runtime mirrors remain unchanged. The removal occurs during the 2.0.0 release-candidate line.

## Acceptance Criteria
- AC-001: Given each former navigator intent fixture, when flow explores it, then the same owning skill is selected.
- AC-002: Given active packages, manifests, current documentation, generated catalogs, and tests after deletion, when references are scanned, then `ai-sdlc-navigator` is absent; historical specs, audit records, and the explicit migration note may retain it as provenance.
- AC-003: Given generated inventories, when module, compatibility, catalog, and install checks run, then each reports exactly 44 skills.
- AC-004: Given unchanged and drifted cards, when Explore and Apply run, then Explore writes nothing, unchanged Apply dispatches at most one action, and drift performs zero mutations.
- AC-005: Given the exact-file audit, when duplicates are classified, then shared-runtime mirrors and generic fixtures are retained with documented reasons.
- AC-006: Given the final diff, when focused validation runs, then every command passes and generated artifacts are current.

## Out of Scope
Merging sequential delivery, QA, review, runtime, commit, or shared-runtime skills; changing lifecycle artifact schemas; publishing or globally installing a release.

## Assumptions
The user authorizes removal of confirmed semantic duplicates. Because flow 011 is not merged to main, this work uses a stacked branch from its commit.

## Open Questions
None blocking. Additional consolidation requires separate evidence because the remaining similar skills own distinct stages and outputs.

## Decision Status
Resolved blockers: none. Accepted assumptions: remove only the flow/navigator semantic duplicate, retain stage-specific skills and runtime mirrors, and use the stacked branch. DEC-001 is accepted.
