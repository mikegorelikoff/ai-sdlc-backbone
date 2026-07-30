---
type: "ai-sdlc.test-cases"
title: "Test Cases"
description: "Test scenarios, expected outcomes, and coverage mapping."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-30T08:41:38Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "015-executable-skill-harness-v4"
  artifact: "test-cases.md"
  path: "specs/015-executable-skill-harness-v4/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/015-executable-skill-harness-v4/_ai_sdlc/state.toon"
  decision_log: "specs/015-executable-skill-harness-v4/decision-log.md"
  status: "review"
  owner: "QA and Repository Maintainers"
  created_at: "2026-07-30"
  updated_at: "2026-07-30"
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
  related_artifacts:
    - "specs/015-executable-skill-harness-v4/branch-plan.md"
    - "specs/015-executable-skill-harness-v4/decision-log.md"
    - "specs/015-executable-skill-harness-v4/design.md"
    - "specs/015-executable-skill-harness-v4/index.md"
    - "specs/015-executable-skill-harness-v4/plan.md"
    - "specs/015-executable-skill-harness-v4/qa.md"
    - "specs/015-executable-skill-harness-v4/requirements.md"
    - "specs/015-executable-skill-harness-v4/research.md"
    - "specs/015-executable-skill-harness-v4/tasks.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "review"
    - "harness-v4"
---

# Test Cases

## Scope
- In scope: v2 manifest semantics, graph selection, generated routers, step context, StepCards, flow Apply boundary, run replay and idempotency, cross-contract integration, hard-cut schema diagnostics, canonical TOON conformance, repository absence scanning, all-skill deterministic evals, and live protocol validation.
- Out of scope: distributed scheduling, external provider certification inside offline CI, embedding retrieval, backward-compatible legacy execution, and in-runtime conversion.
- Behavior under test: a repository skill is deterministically transformed from intent and repository evidence into a context-sufficient, durable, replayable sequence of semantic steps using one canonical machine representation.

## Scenario Matrix
| ID | Requirement | Scenario | Setup | Trigger | Verifiable outcome | Layer | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-001 | AC-001 | Validate the complete v2 skill inventory | Source checkout with 44 skills | Run all-manifest validation | Validation exits 0 and reports exactly 44 skills and at least five nodes per skill | integration | Shared graph check plus shared-runtime unit suite |
| TC-002 | AC-002 | Detect and repair generated-router drift | Copy one fixture skill and alter its router | Run generator check and regenerate | Check exits nonzero naming the stale router; regeneration followed by check exits 0 and bytes match the canonical projection | service | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_skill_graph.py --check --skills-root skills` |
| TC-003 | AC-003 | Compile byte-stable sufficient context | Fixture contains mandatory anchors and related trace files | Compile the same StepCard twice | Both TOON outputs and SHA-256 fingerprints are identical and critical recall equals 1.0 | unit | focused `test_step_context_v4.py` determinism case |
| TC-004 | AC-004 | Fall back to direct reading on weak packing | Fixture omits one critical anchor or saves under 15 percent | Evaluate context sufficiency | Result is `direct_read`, step is not executable from packed context, and reason names recall or savings | unit | focused `test_step_context_v4.py` fallback cases |
| TC-005 | AC-005 | Journal every Apply-owned graph step | Approved Apply fixture selects read and write nodes | Compile and execute a local run | Every task has stable identity plus planned, started, terminal, evidence, and result records; replay projection is complete | integration | focused runtime v2 journal test |
| TC-006 | AC-006 | Resume without duplicate side effects | Fixture interrupts after a side-effect receipt but before caller completion | Resume twice with the same idempotency key | Completed result is reused, side-effect receipt count stays one, and payload mismatch is rejected | integration | focused runtime v2 idempotency and resume tests |
| TC-007 | AC-007 | Prove Explore is zero-write | Clean temporary repository snapshot | Run every Explore path | Before and after file inventories, mtimes, and hashes are identical; no run, journal, cache, lock, state, or context file appears | integration | focused flow v3 zero-write snapshot test |
| TC-008 | AC-008 | Reject stale Apply before run creation | Explore card fingerprint is captured then a selected source changes | Run Apply | Command exits nonzero with stale-fingerprint diagnostic and no run directory exists | integration | focused flow v3 stale Apply test |
| TC-009 | AC-009 | Preserve StepCard semantics across components | Contract fixtures cover flow, workflow, runtime, adapter, and handoff | Compile and validate fixture exchange | Every component agrees on step ID, operation, capabilities, side effects, status, evidence, and fingerprint fields | integration | v4 contract integration test |
| TC-010 | AC-010 | Fail closed on every older schema | Canonical TOON fixtures name older manifest, flow, workflow, run, and context schemas | Load each fixture through a v4 entrypoint | Each attempt exits nonzero, reports received and expected schema, invokes no compatibility reader, and writes no output | unit | hard-cut schema diagnostic table tests |
| TC-011 | AC-011 | Evaluate every skill offline | Repository contains deterministic scenario matrix | Run deterministic eval mode twice | Both receipts are byte-identical, list 44 skills, include happy, blocked, invalid, resume, and context cases, and report zero failures | integration | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_skill_eval.py --mode deterministic --skills-root skills --format toon` |
| TC-012 | AC-012 | Validate provider-neutral live protocol | Representative lifecycle scenario catalog and portable receipt template | Validate protocol then execute in an authorized host during release | Offline protocol validation exits 0; release receipt contains routing, compliance, evidence, recovery, and context scores without changing deterministic fingerprints | QA/manual | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_skill_eval.py --mode live-protocol --skills-root skills --format toon`; provider execution is release-owned |
| TC-013 | AC-013 | Enforce repository-wide TOON-only canonicality | Complete source tree plus strict documentation output | Run absence scan, decode all TOON files, and canonicalize repository-owned generated artifacts | No alternate-format extension or identifier exists; every TOON file decodes; canonical artifacts round-trip byte-for-byte | integration | shared-runtime conformance test plus post-build repository scan |

## Layer Mapping
Execution order:
1. Canonical representation layer: run absence, decoder, malformed-input, schema-contract, and byte-canonicalization checks; blocks every later layer.
2. Schema and unit layer: run graph, context, and hard-cut diagnostic tests; blocks integration; failure action is fix contracts and rerun focused tests.
3. Service layer: run selector, generator, and StepCard tests; blocks runtime integration; failure action is repair canonical source or projection.
4. Integration layer: run workflow, flow, runtime, adapter, all-skill deterministic evals, and every skill-owned suite; blocks documentation and installation smoke; failure action is preserve journals and repair the first failed invariant.
5. Installed-layout and documentation layer: run package smoke, catalogs, compatibility, strict docs build, rendered validation, and a second absence scan; blocks release candidate.
6. Live QA layer: run TC-012 only in an authorized provider host; blocks v4 release certification but not deterministic implementation completion.

## Automation Plan
- TC-001 and TC-002: semantic graph validator and router generator plus golden drift fixtures.
- TC-003 and TC-004: standard-library unit tests for exact ranges, anchors, token estimates, recall, savings, authority, sufficiency, skipped-source reasons, and fingerprint stability.
- TC-005 and TC-006: temporary-directory runtime fixtures that enforce event order and count side-effect receipts across interruption and replay.
- TC-007 and TC-008: before and after filesystem snapshot fixtures around Explore and Apply.
- TC-009 and TC-010: schema fixture table spanning every public v4 component and each rejected older schema.
- TC-011: deterministic eval CLI writes only to stdout unless an explicit TOON receipt path is provided and is run twice for byte equality.
- TC-012: offline protocol lint in CI; authorized release maintainers provide the external live receipt.
- TC-013: repository scanner constructs the forbidden token defensively, checks tracked and generated paths, decodes every TOON artifact, and compares canonical bytes where repository ownership requires them.

## Open Gaps
- Decision: provider and model certification matrix. Options are one reference host, one host per adapter, or every advertised host. Recommended default is one reference host per adapter family because it tests contract portability without coupling the deterministic core to vendors. Owner: Release maintainers. Blocking: only v4 release certification, not implementation or offline validation.
- External credentials and live-provider availability are intentionally absent from repository fixtures; the residual risk is model-specific instruction compliance that deterministic tests cannot measure.
