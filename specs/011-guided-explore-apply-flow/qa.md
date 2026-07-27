---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "qa.md"
  path: "specs/011-guided-explore-apply-flow/qa.md"
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
    - "AC-010"
    - "TC-001"
    - "TC-020"
  related_artifacts:
    - "specs/011-guided-explore-apply-flow/branch-plan.md"
    - "specs/011-guided-explore-apply-flow/decision-log.md"
    - "specs/011-guided-explore-apply-flow/design.md"
    - "specs/011-guided-explore-apply-flow/requirements.md"
    - "specs/011-guided-explore-apply-flow/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "approved"
---

# QA

## Change Summary
Introduce the `ai-sdlc-flow` meta-skill, correct navigator classification precedence, add shared fingerprint/path/role/rigor/context contracts, enforce spec-first review ordering, and update catalogs/docs while preserving direct-skill compatibility. QA validates safety and transparency before convenience.

## Acceptance Scenarios
Execute TC-001–TC-020. P0 signoff requires AC-001–AC-010: correct intent routing, zero-write Explore, single-step drift-safe Apply, root safety, evidence-driven roles, explained rigor, measured context fallback, blind defect/readability detection, compatibility, and all repository gates.

## Regression Targets
`ai-sdlc-navigator`; `ai-sdlc-shared-runtime` and canonical `_shared`; path/state/index helpers; context benchmark; `ai-sdlc-code-review`; every direct skill help/smoke surface; module and managed-skill inventories; catalog generator; docs validator; project-scoped install smoke; SDD/refinement state and indexes.

## Risk Notes
P0: Apply mutates on drift or unsafe root. P1: intent selects wrong feature, Explore writes, anchor loss is accepted, blind review ordering leaks rationale, or direct skills break. P2: explanations or docs are incomplete. Stop on unexpected tracked-file mutation, non-deterministic fingerprint, missing fixture evidence, or catalog/runtime divergence.

## Validation Commands
1. `python3 -m unittest skills.ai-sdlc-flow.tests.test_flow` or the repository-compatible file invocation chosen in T005.
2. `python3 skills/ai-sdlc-navigator/tests/test_navigate.py` and affected focused suites.
3. `python3 -m unittest discover -s skills/_shared -p 'test_*.py'` plus shared-runtime mirror tests.
4. `python3 docs/scripts/build_catalog.py --check` and `python3 docs/scripts/validate_docs.py`.
5. Project-scoped install smoke and compatibility checks documented by current scripts.
6. Full SDD gates in prescribed order and `refinement_status.py --feature 011-guided-explore-apply-flow --gate full`.
Exact executable command forms are confirmed during T001 and recorded without broadening scope.

## Manual Checks
As a newcomer, read an Explore card and identify why the feature, workspace, roles, rigor, context strategy, and next checkpoint were chosen; verify planned writes before Apply. Change one evidence input and confirm the drift diagnostic is actionable. Review the seeded diff without rationale, record the bug and readability issue, then reveal comparison context and verify independent findings were preserved.

## Signoff
Engineering and QA sign off only when TC-001–TC-020 pass, filesystem snapshots prove Explore no-write and rejected Apply no-write, accepted Apply dispatches one action, critical recall is 100%, accepted pack savings is at least 15%, seeded P0/P1 and readability findings are detected blind, no unexpected P0/P1 remains, direct skills pass compatibility, and all docs/catalog/SDD/refinement gates are green.
