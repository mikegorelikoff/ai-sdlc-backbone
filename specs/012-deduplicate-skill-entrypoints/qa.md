---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "012-deduplicate-skill-entrypoints"
  artifact: "qa.md"
  path: "specs/012-deduplicate-skill-entrypoints/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/012-deduplicate-skill-entrypoints/_ai_sdlc/state.toon"
  decision_log: "specs/012-deduplicate-skill-entrypoints/decision-log.md"
  status: "approved"
  owner: "Repository Maintainers"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "TC-001"
    - "TC-006"
  related_artifacts:
    - "specs/012-deduplicate-skill-entrypoints/branch-plan.md"
    - "specs/012-deduplicate-skill-entrypoints/decision-log.md"
    - "specs/012-deduplicate-skill-entrypoints/design.md"
    - "specs/012-deduplicate-skill-entrypoints/requirements.md"
    - "specs/012-deduplicate-skill-entrypoints/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "approved"
    - "deduplication"
---

# QA

## Change Summary
One canonical guided entrypoint replaces the duplicate navigator/flow pair.

## Acceptance Scenarios
Exercise TC-001–TC-006, including former navigator-only intents, ambiguous intent, zero-write Explore, source drift, and installed package inventory.

## Regression Targets
Direct skill invocation, state/index schemas, shared-runtime mirrors, protected flags, module discovery, install smoke, compatibility, catalogs, and docs navigation.

## Risk Notes
Highest risk is silent loss of a navigator-only route or accidental expansion of executable Apply actions.

## Validation Commands
`python3 skills/ai-sdlc-flow/tests/test_flow.py`; shared contract/per-skill/module tests; compatibility; docs validation/tests; emulated install smoke; SDD gates; `git diff --check`.

## Manual Checks
Read the generated flow reference and migration note; confirm the 44-skill catalog has one obvious entrypoint.

## Signoff
QA-ready when TC-001–TC-006 pass and no unexplained navigator reference remains.
