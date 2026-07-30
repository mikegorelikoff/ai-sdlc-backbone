---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "code-review.md"
  path: "specs/011-guided-explore-apply-flow/code-review.md"
  workspace: "implementation"
  skill: "ai-sdlc-code-review"
  flow_mode: "full"
  state_file: "specs/011-guided-explore-apply-flow/_ai_sdlc/state.toon"
  decision_log: "specs/011-guided-explore-apply-flow/decision-log.md"
  status: "approved"
  owner: "Repository Maintainers"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-002"
    - "AC-003"
    - "AC-005"
    - "AC-008"
    - "AC-009"
    - "AC-010"
    - "DEC-006"
    - "DEC-012"
    - "FR-002"
    - "FR-003"
    - "FR-005"
    - "FR-009"
    - "TC-004"
    - "TC-006"
    - "TC-010"
    - "TC-017"
    - "TC-018"
  related_artifacts:
    - "specs/011-guided-explore-apply-flow/requirements.md"
    - "specs/011-guided-explore-apply-flow/test-cases.md"
    - "specs/011-guided-explore-apply-flow/validation.md"
    - "specs/011-guided-explore-apply-flow/_ai_sdlc/validation-receipt.toon"
  validation:
    - "code-review readiness completed without errors"
    - "focused regression checks passed after fixes"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-code-review"
    - "code-review"
    - "approved"
---

# Code Review

## Findings

- No unresolved findings in the final reviewed diff.

## Independent Findings and Resolution

The first pass read requirements, acceptance criteria, tests, and the diff before implementation rationale or prior verdicts.

| Severity | Evidence | Independent finding | Resolution |
| --- | --- | --- | --- |
| High | `skills/_shared/ai_sdlc_flow.py` renderers; FR-002 | Markdown and TOON omitted selected source hashes, so the human-readable cards were incomplete even though TOON carried the evidence. | Both renderers now expose the source hash list; parity regression assertions cover it. |
| High | `discover_sources`; FR-003 / AC-003 | Supplying `--source` replaced mandatory state/config/index evidence, allowing those inputs to drift without invalidating Apply. | Explicit sources now extend mandatory controls; Apply rediscovers the mandatory set and rejects additions, deletion, or hash drift. |
| Medium | `skills/ai-sdlc-flow/SKILL.md`; AC-002 | The pipe example connected Explore directly to executing Apply, contradicting the explicit human checkpoint. | The documentation now shows a separate Apply command for an already accepted card. |
| Medium | `choose_context`; AC-007 | Negative counts or retained anchors greater than total were not rejected deterministically. | Invalid measurements now return `FLOW_INVALID_CONTEXT`; boundary tests cover both cases. |
| Medium | `validate_workspace`; AC-005 | A symlinked canonical `specs` or `specs-refiniment` root was followed even though feature-root symlinks were rejected. | Canonical workspace-root symlinks are now blocked and tested. |
| Medium | `skills/_shared/test_modules.py`; AC-009 / AC-010 | The shipped module registry used `2.0.0-rc.1`, while discovery and its repository test still rejected prerelease SemVer and expected `1.11.0`. | Module identities now accept SemVer prerelease/build labels, API range parsing remains strict three-part numeric, and the repository test covers `2.0.0-rc.1` plus flow ownership. |
| Low | DecisionCard/readability; FR-002 | Classification confidence and default project-context freshness were not explicit. | DecisionCard now carries confidence, and `auto` resolves to a hash-backed present/not-found status. |

## Comparison Phase

After the independent findings were recorded, they were compared with the implementation intent and validation evidence. The initial implementation rationale did not call out the contract gaps above; all were therefore retained as review findings and fixed. The clean post-fix pass found no additional P0/P1 behavior issue or material readability violation.

## Validation Gaps

- None for the checked-in deterministic scope after the final validation receipt is refreshed.
- Token measurements are caller-supplied; the implementation validates and evaluates them but does not independently estimate token usage.

## Residual Risk

- Fingerprints provide local drift detection, not authentication or authorization.
- Global public CLI installation remains explicitly out of scope.

## Summary

Reviewed the flow, navigator, shared runtime, packaging, docs, tests, and lifecycle artifacts against FR-001–FR-010 and TC-001–TC-020. Seven independent findings were corrected; the post-fix diff has no unresolved review finding.
