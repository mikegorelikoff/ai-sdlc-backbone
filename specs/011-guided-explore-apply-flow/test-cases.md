---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "test-cases.md"
  path: "specs/011-guided-explore-apply-flow/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/011-guided-explore-apply-flow/_ai_sdlc/state.toon"
  decision_log: "specs/011-guided-explore-apply-flow/decision-log.md"
  status: "approved"
  owner: "Repository Maintainers"
  created_at: "2026-07-26"
  updated_at: "2026-07-26"
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
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-009"
    - "TC-010"
    - "TC-011"
    - "TC-012"
    - "TC-013"
    - "TC-014"
    - "TC-015"
    - "TC-016"
    - "TC-017"
    - "TC-018"
    - "TC-019"
    - "TC-020"
  related_artifacts:
    - "specs/011-guided-explore-apply-flow/branch-plan.md"
    - "specs/011-guided-explore-apply-flow/decision-log.md"
    - "specs/011-guided-explore-apply-flow/design.md"
    - "specs/011-guided-explore-apply-flow/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "approved"
---

# Test Cases

## Scope
Test FR-001–FR-010 and AC-001–AC-010 across pure units, temporary-repository integration, installed-runtime compatibility, generated documentation, and manual readability/blind-review evidence. Use only checked-in synthetic data; global installation, remote publication, telemetry, and multi-stage execution are excluded.

## Scenario Matrix
| Test ID | Acceptance Ref | Scenario | Preconditions | Steps | Expected Result | Priority | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-001 | AC-001 | New-feedback intent beats latest completed state | latest feature 010 plus original feedback | Explore | feature 011 and refinement/SDD checkpoint | P0 | automated |
| TC-002 | AC-001 | Ambiguous intent blocks selection | mixed refinement and implementation signals | Explore | blocker and no selected action | P0 | automated |
| TC-003 | AC-002 | Explore filesystem snapshot | fixture repository and intent | Explore Markdown | zero path/content changes | P0 | automated |
| TC-004 | AC-002 | Markdown/TOON semantic parity | same fixture | render both formats | same card fields and fingerprint | P0 | automated |
| TC-005 | AC-003 | Accepted Apply dispatch | unchanged card/state | Apply | exactly one allow-listed action | P0 | automated |
| TC-006 | AC-003 | Fingerprint drift matrix | mutate each fingerprint input | Apply each card | drift blocker and zero mutation | P0 | automated |
| TC-007 | AC-004 | Canonical root routing | refinement and implementation fixtures | Explore | correct distinct root | P0 | automated |
| TC-008 | AC-004 | Caller override and traversal | root override and .. path | Explore/Apply | FLOW_UNSAFE_ROOT | P0 | automated |
| TC-009 | AC-004 | Symlink feature root | symlinked specs feature | Explore/Apply | FLOW_UNSAFE_ROOT | P0 | automated |
| TC-010 | AC-004 | Divergent roots | canonical plus conflicting legacy fixture | Explore/Apply | fail closed with divergence diagnostic | P0 | automated |
| TC-011 | AC-005 | Minimal code roles | code-only intent | Explore | Contributor/Engineering only | P0 | automated |
| TC-012 | AC-005 | Evidence-driven role expansion | auth, migration, release, product-policy fixtures | Explore | only matching role with cited trigger | P0 | automated |
| TC-013 | AC-006 | Adaptive rigor table | low-risk and cross-cutting fixtures | Explore | quick then full with reasons | P0 | automated |
| TC-014 | AC-006 | Rigor overrides and policy | safe and unsafe overrides | Explore | honor safe; upgrade/block unsafe | P0 | automated |
| TC-015 | AC-007 | Pack threshold success | 100% anchors and 15% savings | Explore | packed selected and economics shown | P0 | automated |
| TC-016 | AC-007 | Pack rejection boundaries | anchor loss, 14.99%, negative reread saving | Explore | direct selected with all metrics | P0 | automated |
| TC-017 | AC-008 | Blind seeded review | bug plus readability fixture | Review through flow | both findings before rationale | P0 | automated |
| TC-018 | AC-008 | Clean blind review | clean fixture | Review through flow | no unexpected P0/P1 | P0 | automated |
| TC-019 | AC-009 | Direct-skill compatibility | current command fixtures | run focused compatibility/install smoke | all existing paths remain valid | P0 | automated |
| TC-020 | AC-010 | Catalog/docs/full gates | generated inventories and complete package | run validation order | all gates pass and flow appears once where required | P0 | automated |

## Layer Mapping
TC-001–TC-002: navigator/flow classification unit and integration. TC-003–TC-006: DecisionCard/fingerprint/action adapter integration. TC-007–TC-010: temporary-filesystem path safety. TC-011–TC-016: pure role/rigor/context tables plus flow integration. TC-017–TC-018: review workflow contract and seeded fixtures. TC-019: compatibility and install smoke. TC-020: docs, catalog, SDD, and refinement end-to-end gates.

## Automation Plan
Add `skills/ai-sdlc-flow/tests/test_flow.py`; expand navigator, shared runtime, path, context benchmark, code-review, compatibility, module, install-smoke, and docs tests. Use `tempfile.TemporaryDirectory`, deterministic Git fixtures, subprocess argv arrays, and before/after recursive hashes. Snapshot schema fields rather than incidental prose. Manual evidence is limited to newcomer readability and confirmation that blind findings precede rationale.

## Open Gaps
All acceptance outcomes have test IDs and deterministic fixture designs. Owner: QA and Repository Maintainers. Impact: implementation can proceed test-first. Resolution: T005–T007 bind these cases to concrete test modules and commands before any task is marked complete.
