---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "012-deduplicate-skill-entrypoints"
  artifact: "test-cases.md"
  path: "specs/012-deduplicate-skill-entrypoints/test-cases.md"
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
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
  related_artifacts:
    - "specs/012-deduplicate-skill-entrypoints/branch-plan.md"
    - "specs/012-deduplicate-skill-entrypoints/decision-log.md"
    - "specs/012-deduplicate-skill-entrypoints/design.md"
    - "specs/012-deduplicate-skill-entrypoints/plan.md"
    - "specs/012-deduplicate-skill-entrypoints/qa.md"
    - "specs/012-deduplicate-skill-entrypoints/requirements.md"
    - "specs/012-deduplicate-skill-entrypoints/tasks.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "review"
    - "deduplication"
---

# Test Cases

## Scope
Validate FR-001–FR-006 and AC-001–AC-006 across routing, removal, packaging, compatibility, and generated documentation.

## Scenario Matrix
| ID | Requirement | Scenario | Expected |
| --- | --- | --- | --- |
| TC-001 | AC-001 | Former navigator discovery, QA, story, review, and implementation intents | Flow selects the same owning skill |
| TC-002 | AC-002 | Scan active packages, inventories, current docs, generated catalogs, and tests after deletion | No navigator package or active reference; historical specs, audits, and migration provenance are allow-listed |
| TC-003 | AC-003 | Generate module, compatibility, catalog, and install outputs | Exactly 44 skills and no navigator |
| TC-004 | AC-004 | Explore and Apply regression | Explore writes nothing; drift blocks; one action maximum |
| TC-005 | AC-005 | Exact duplicate audit | Mirrors and generic fixtures are classified intentional |
| TC-006 | AC-006 | Full focused gate | All selected commands pass |

## Layer Mapping
TC-001 and TC-004 are flow unit/integration tests. TC-002 is a repository reference scan. TC-003 covers module/compatibility/docs/install integration. TC-005 is documented audit evidence. TC-006 is validation orchestration.

## Automation Plan
Extend `skills/ai-sdlc-flow/tests/test_flow.py`; update existing shared/docs tests and generated counts; run repository scripts without network.

## Open Gaps
No blocking gaps. Historical migration wording must be explicitly allow-listed in the stale-reference scan.
