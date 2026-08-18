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
  at: "2026-08-17T11:13:22Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "test-cases.md"
  path: "specs/022-ai-sdlc-loop/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-08-17"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
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
    - "TC-020"
    - "TC-021"
    - "TC-022"
    - "TC-024"
  related_artifacts:
    - "specs/022-ai-sdlc-loop/branch-plan.md"
    - "specs/022-ai-sdlc-loop/decision-log.md"
    - "specs/022-ai-sdlc-loop/design.md"
    - "specs/022-ai-sdlc-loop/index.md"
    - "specs/022-ai-sdlc-loop/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "approved"
    - "ai-sdlc-loop"
---

# Test Cases

## Scope
Implementation coverage extends the approved refinement suite through TC-031: all install profiles, deterministic Specify, approval denial/eligibility, scoped change evidence, verification failures/redaction, commit authority, TOON promotion compatibility, stage and delivery-control manifests, helper loading and selection, TOON-native requirements, QA, release reviews, exact Loop skill namespace, strict MkDocs documentation, public release identity, parent submodule, and Harness regression.

## Scenario Matrix
- TC-001..TC-003 / AC-001: all profiles, unsafe inputs, idempotency, and managed drift.
- TC-004..TC-005 / AC-002: canonical Specify and fingerprint sensitivity.
- TC-006..TC-009 / AC-003: approval states, eligibility, scoped paths, and escape defenses.
- TC-010..TC-012 / AC-004: passing/failing verification and secret redaction.
- TC-013..TC-015 / AC-005: commit denials, success, and replay/drift protection.
- TC-016..TC-017 / AC-006: compatible promotion and atomic rejection.
- TC-018..TC-024 / AC-007: documentation, trust files, OS CI, public/tag identity, submodule, parent regression, and manual UAT.
- TC-025 / AC-008: manifests, runtime paths, install records, state, evidence, and promotion remain TOON-only.
- TC-026 / AC-009: all eight delivery-control helpers load and their canonical v2 prepare steps resolve through the copied shared selector.
- TC-027 / AC-010: the compact QA helper emits deterministic canonical TOON, validates typed acceptance scenarios, resolves its five-node graph, writes atomically, and rejects traversal or non-TOON output.
- TC-028 / AC-011: requirements review emits deterministic typed TOON and rejects `ready` with critical/high findings or missing coverage.
- TC-029 / AC-012: release readiness binds TOON gates to an exact Git identity and rejects `ready` with incomplete gates or blockers.
- TC-030 / AC-013: installer inventory, directory names, `SKILL.md` frontmatter, manifest IDs, runtime paths, and public examples use exactly `ai-sdlc-loop-{slug}`, with `ai-sdlc-loop-orchestrate` as the root router and no superseded packaged IDs.
- TC-031 / AC-014: MkDocs strict build passes; navigation contains the six public sections in order; every source skill appears in Reference; and the versioned install command appears once and identically in README, Home, and Start here.

## Layer Mapping
Unit tests cover normalization, canonical TOON round trips, fingerprints, paths, receipts, redaction, v1/v2 skill manifests, helper imports, step selection, requirements/QA/release artifact generation, and schema validation. Integration tests cover the exact seventeen-member installer inventory and isolated Git workflow fixtures. Security tests cover escape, replay, secret, and preservation invariants. Promotion tests cover TOON supported-field equality and version rejection. Hosted checks cover operating systems and public identity. Parent checks cover gitlink and canonical documentation validation. TC-024 remains manual because approval must remain human.

## Automation Plan
Create `tests/test_install.py`, `tests/test_workflow.py`, `tests/test_security.py`, `tests/test_promotion.py`, `tests/test_docs.py`, and `tests/test_release.py`, with test names carrying TC identifiers. Run `python3 -m unittest discover -s tests -v`, `python3 -m compileall`, installer smoke fixtures, shell syntax, and `git diff --check` locally. GitHub Actions runs the network-free suite on Linux, macOS, and Windows. Release and parent checks run only after authorized publication.

## Open Gaps
TC-020, TC-021, and the remote half of TC-022 require GitHub state and cannot be proven before publication. TC-024 requires a human reviewer and stays a release-candidate signoff. These are sequenced gates, not waived coverage.
