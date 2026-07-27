---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "013-role-guided-installable-flow"
  artifact: "code-review.md"
  path: "specs/013-role-guided-installable-flow/code-review.md"
  workspace: "implementation"
  skill: "ai-sdlc-code-review"
  flow_mode: "full"
  state_file: "specs/013-role-guided-installable-flow/_ai_sdlc/state.toon"
  decision_log: "specs/013-role-guided-installable-flow/decision-log.md"
  status: "approved"
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
    - "AC-011"
    - "AC-012"
    - "AC-013"
    - "AC-014"
    - "AC-015"
    - "AC-016"
    - "DEC-001"
    - "DEC-002"
  related_artifacts:
    - "specs/013-role-guided-installable-flow/requirements.md"
    - "specs/013-role-guided-installable-flow/design.md"
    - "specs/013-role-guided-installable-flow/test-cases.md"
    - "specs/013-role-guided-installable-flow/validation.md"
    - "specs/013-role-guided-installable-flow/_ai_sdlc/validation-receipt.json"
  validation:
    - "code-review readiness completed without errors"
    - "ai-sdlc-validation-receipt/v1: 10 commands; 0 failures"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-code-review"
    - "code-review"
    - "approved"
---

# Code Review

## Findings

No unresolved findings remain in the final reviewed diff.

## Independent Findings and Resolution

The first pass read requirements, acceptance criteria, test cases, and the
changed runtime/configuration/install surfaces before comparing implementation
rationale or prior validation results.

| Severity | Evidence | Independent finding | Resolution |
| --- | --- | --- | --- |
| Medium | `ai_sdlc_flow.build_card`, selector registry, AC-008/AC-009 | Direct API callers could pass malformed selector records that reached indexed fields and failed with an opaque `KeyError` or `TypeError`; registry values were shape-checked but not fully bounded. | Runtime validation now checks exact fields, unique IDs, canonical roles/actions, contained package paths, integer bounds, and reason length before routing. CLI and direct API failures are actionable and fail closed. Regression tests cover unknown fields, roles, and escaping paths. |
| Low | `DecisionCard` construction; user readability feedback | The 36-field positional dataclass construction was difficult for a human reviewer to audit and made field-order mistakes unnecessarily likely. | Construction now uses explicit keyword arguments and readable checkpoint formatting without changing the serialized contract. |
| Low | Explore CLI error boundary | Registry or direct routing validation errors raised after configuration loading could escape the CLI as a traceback. | Explore now converts routing validation failures into a deterministic `FLOW_INVALID_ROUTE` error and performs no mutation. |

## Comparison Phase

After the independent findings were recorded, they were compared with the
requirements, design, tests, and current validation receipt. All three findings
were retained and corrected. The post-fix pass found no additional correctness,
security, traceability, installation, or material readability defect.

## Progressive-Disclosure Review Addendum

The step-manifest extension was reviewed as a new boundary against REQ-008
through REQ-011 and AC-013 through AC-016. No unresolved finding remains.

| Severity | Evidence | Independent finding | Resolution |
| --- | --- | --- | --- |
| Medium | `ai_sdlc_steps.resolve_skill_root`; installed-layout fallback | An incomplete target skill, including a broken directory symlink, could be skipped in favor of the packaged source copy and hide a broken installation. | Target layout now has strict precedence and fails closed for incomplete, non-directory, or symlinked skill roots. Dedicated regressions cover missing manifests and broken symlinks. |
| Medium | `ai_sdlc_steps.load_manifest`; singular owning-skill step contract | Two selectors with overlapping phase, role, and action domains could both match even though the router and DecisionCard expose one owning procedure. | Manifest validation now rejects overlapping selector domains before selection. |
| Medium | `ai_sdlc_steps.select_steps`; direct CLI usage | Optional role and action filters were initially treated as required membership, preventing phase-only direct selection. | Omitted filters are now wildcards; explicit mismatches still return `STEP_NO_MATCH`. |
| Medium | Flow registry owners versus migrated manifests | Several action owners did not match the role declared by their owning skill, which blocked otherwise valid Explore decisions. | Role declarations were aligned with the accepted owner model and every registry action now resolves an owning-skill step in an integration test. |
| Low | Flow router entry wording | The generic router instruction named a `prepare` selector even though guided flow begins with `clarify` and `route`. | Router wording now distinguishes the flow entry selectors without weakening the prepare-first rule for other skills. |
| Low | Compatibility and lifecycle tests | Tests that read only monolithic `SKILL.md` files would either fail spuriously or encourage copying normative prose back into routers. | Contract checks now aggregate each concise router with only its manifest-declared procedures. |

The post-fix pass also verified 44 manifests, 135 declared procedures, router
size budgets, generated selector documentation, three installed layouts, and
the ten-command validation matrix.

## Validation Gaps

No gap remains for the checked-in deterministic scope. Real networked Skills
CLI installation was not repeated locally; pinned CI retains the public and
immutable-remote installation checks.

## Residual Risk

- Intent classification remains deliberately keyword-based and blocks mixed
  intent instead of guessing.
- The selector allowlist can only load regular, non-symlink files shipped
  inside the flow package; broader project context remains intentionally out of
  scope.

## Summary

The final implementation satisfies AC-001 through AC-016: it removes the
repository-only runtime duplicate, installs one canonical runtime, exposes five
neutral role contracts with one active owner, loads bounded step/reference
context just in time, validates configuration and selectors fail closed, and
passes the ten-command validation matrix. Every installable skill now exposes a
concise router backed by validated, skill-owned procedural steps.
