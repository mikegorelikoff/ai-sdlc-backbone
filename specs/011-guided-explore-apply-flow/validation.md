---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "validation.md"
  path: "specs/011-guided-explore-apply-flow/validation.md"
  workspace: "implementation"
  skill: "ai-sdlc-validation"
  flow_mode: "full"
  state_file: "specs/011-guided-explore-apply-flow/_ai_sdlc/state.toon"
  decision_log: "specs/011-guided-explore-apply-flow/decision-log.md"
  status: "validated"
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
    - "AC-007"
    - "AC-008"
    - "AC-009"
    - "AC-010"
    - "DEC-011"
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
    - "specs/011-guided-explore-apply-flow/_ai_sdlc/validation-plan.toon"
    - "specs/011-guided-explore-apply-flow/_ai_sdlc/validation-receipt.toon"
    - "specs/011-guided-explore-apply-flow/requirements.md"
    - "specs/011-guided-explore-apply-flow/test-cases.md"
  validation:
    - "12/12 reviewed validation-plan commands passed"
    - "validation receipt verified current"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-validation"
    - "validation"
    - "validated"
---

# Validation

## Result

Passed. The reviewed argv-only plan executed 12 focused and repository-level checks with zero failed commands.

## Evidence

- Flow contracts: 12 tests passed, including read-only Explore, source drift rejection, one-action Apply, context economics, and spec-first review ordering.
- Navigator regression: 8 tests passed, including intent-first routing for new feedback.
- Shared skill script contracts: 29 tests passed.
- Every skill-owned test file passed.
- Module discovery and prerelease SemVer compatibility tests passed.
- Compatibility baseline passed with 45 protected skills.
- Documentation and generated catalog validation passed with 185 public pages, 45 skills, 5 modules, and 120 scripts.
- Emulated project-scoped installation smoke passed.
- Full SDD status remained `ready_for_impl`.
- Full 18-stage refinement gate passed with zero blockers and warnings.
- `git diff --check` passed.

Machine-verifiable command hashes, byte counts, exit codes, environment, revision, plan hash, and workspace fingerprint are recorded in `_ai_sdlc/validation-receipt.toon`.

## Manual Checks

- The Markdown DecisionCard presents intent, route, rigor, roles, context economics, blockers, writes, checkpoint, and fingerprint in readable labels.
- The independent-review packet excludes AI rationale and prior verdict fields until an explicit finding or `No findings.` result is recorded.
- The seeded review fixture exposes both a P1 behavior marker and a readability marker during the independent phase; the clean fixture records an explicit no-findings result.

## Residual Risk

- Context token and anchor counts are supplied measurements; the flow enforces the acceptance rule but does not estimate tokens itself.
- The fingerprint is a local integrity comparison, not authentication.
- Global public CLI installation remains out of scope; project-scoped packaging is validated.
