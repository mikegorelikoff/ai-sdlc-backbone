---
type: "ai-sdlc.test-cases"
title: "Test Cases"
description: "Test scenarios, expected outcomes, and coverage mapping."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-09-01T09:52:49Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "test-cases.md"
  path: "specs/022-ai-sdlc-loop/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-09-01"
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
    - "AC-017"
    - "AC-018"
    - "AC-019"
    - "TC-001"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-009"
    - "TC-010"
    - "TC-012"
    - "TC-013"
    - "TC-015"
    - "TC-016"
    - "TC-017"
    - "TC-018"
    - "TC-024"
    - "TC-025"
    - "TC-026"
    - "TC-027"
    - "TC-028"
    - "TC-029"
    - "TC-030"
    - "TC-031"
    - "TC-032"
    - "TC-033"
    - "TC-034"
    - "TC-035"
    - "TC-036"
    - "TC-037"
    - "TC-038"
    - "TC-039"
  related_artifacts:
    - "specs/022-ai-sdlc-loop/branch-plan.md"
    - "specs/022-ai-sdlc-loop/code-review.md"
    - "specs/022-ai-sdlc-loop/commit-message.md"
    - "specs/022-ai-sdlc-loop/commit-readiness.md"
    - "specs/022-ai-sdlc-loop/decision-log.md"
    - "specs/022-ai-sdlc-loop/design.md"
    - "specs/022-ai-sdlc-loop/index.md"
    - "specs/022-ai-sdlc-loop/plan.md"
    - "specs/022-ai-sdlc-loop/qa.md"
    - "specs/022-ai-sdlc-loop/requirements.md"
    - "specs/022-ai-sdlc-loop/security-review.md"
    - "specs/022-ai-sdlc-loop/tasks.md"
    - "specs/022-ai-sdlc-loop/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "approved"
    - "engineering-quality-gate"
    - "ai-sdlc-loop"
---

# Test Cases

## Scope
Implementation coverage extends the existing TC-001 through TC-031 suite with TC-032 through TC-039 for the dual Harness/Loop engineering quality gate: package discovery, deterministic bounded context and representative examples, typed findings and safe remediation, verification truthfulness, report invariants and drift, mandatory Loop ordering, exact installed inventory, examples, documentation, and generated catalog agreement.

## Scenario Matrix
- TC-001..TC-003 / AC-001: all install profiles, unsafe inputs, idempotency, managed drift, and exact inventory.
- TC-004..TC-005 / AC-002: canonical Specify and fingerprint sensitivity.
- TC-006..TC-009 / AC-003: approval states, eligibility, scoped paths, and escape defenses.
- TC-010..TC-012 / AC-004: passing/failing verification and secret redaction.
- TC-013..TC-015 / AC-005: commit denials, success, and replay/drift protection.
- TC-016..TC-017 / AC-006: compatible promotion and atomic rejection.
- TC-018..TC-024 / AC-007: documentation, trust files, OS CI, public/tag identity, submodule, parent regression, and manual UAT.
- TC-025 / AC-008: durable Loop artifacts remain TOON-only.
- TC-026 / AC-009: delivery-control helpers load and canonical v2 prepare steps resolve.
- TC-027 / AC-010: compact QA output is deterministic, typed, atomic, and path-safe.
- TC-028 / AC-011: requirements review emits typed TOON and rejects severe or incomplete readiness.
- TC-029 / AC-012: release readiness binds gates to an exact Git identity and rejects incomplete readiness.
- TC-030 / AC-013: distributed directories, frontmatter, manifests, paths, and examples use `ai-sdlc-loop-{slug}`.
- TC-031 / AC-014: strict MkDocs build, navigation, source inventory, and primary install command remain aligned.
- TC-032 / AC-015, AC-019: both quality-gate packages have valid frontmatter, v2 manifests, bounded steps, schemas, examples, loadable helpers, selector entrypoints, and skill-script contracts.
- TC-033 / AC-016: unchanged and absolute-path-varied Git fixtures produce byte-identical bounded context; changed paths, candidates, examples, and verification sources use stable ordering; diff drift changes the context fingerprint.
- TC-034 / AC-017: every finding validates severity/category/path/evidence/impact/recommended fix; repository-fit and anti-AI/scope checks are present; invalid or duplicate finding IDs fail without output.
- TC-035 / AC-017: High and safe localized Medium remediation is allowed only inside approved paths; Low and clarification-blocked findings remain explicit; unrelated tracked, staged, unstaged, and untracked bytes stay unchanged.
- TC-036 / AC-018: focused checks precede broader checks, post-fix checks are distinguishable, every status is pass/fail/not_run/unavailable, and failed or unexecuted required available checks make PASS impossible.
- TC-037 / AC-016, AC-018: unchanged normalized draft plus context yields byte-identical canonical report/fingerprint; stale context, unresolved High/blocking Medium, or inconsistent decision/status is rejected atomically.
- TC-038 / AC-015: Loop orchestrator resolves Implement → Engineering Quality Gate → Verify; Verify denies missing, non-ready, invalid, or stale gate evidence and accepts current ready evidence; direct skill invocation remains selectable.
- TC-039 / AC-019: Loop installs exactly twenty namespaced packages and documents all source skills/examples; Harness core/module/default inventory exposes the canonical skill; generated catalogs and all count baselines match source.

## Layer Mapping
Skill-local unit tests cover context discovery, deterministic ranking, canonical TOON, fingerprints, report schema, status/readiness invariants, output containment, and atomic writes. Loop integration tests cover installation, selection, orchestrator order, Verify enforcement, promotion/status inclusion, and stale evidence. Harness shared-runtime tests cover core module/default inventories, loader graphs, script contracts, compatibility counts, and flow routing. Documentation tests cover generated catalog coverage and Loop source-backed inventory. Existing security and preservation fixtures cover symlink, traversal, unauthorized path, and unrelated-work invariants.

## Automation Plan
Add `skills/ai-sdlc-engineering-quality-gate/tests/test_engineering_quality_gate.py`, its standard `test_scripts.py`, and `products/ai-sdlc-loop/tests/test_engineering_quality_gate.py`; extend Loop install/docs/workflow tests and Harness module/flow/install/count tests. Run each new skill test and helper contract first; then Loop unittest/compile/shell/docs checks; then Harness module, skill, catalog, docs, MkDocs/render, and diff checks. Use reproducible temporary Git fixtures with fixed commits and no network.

## Open Gaps
AI semantic judgment cannot be proven solely by deterministic helper tests, so forward-test the completed skill on at least one realistic changed repository fixture and independently inspect whether it selects useful comparisons, records evidence, and obeys fix scope. Hosted OS and release identity work already represented by T006 remains a separate pre-existing release gate; it is not waived by TC-032 through TC-039.
