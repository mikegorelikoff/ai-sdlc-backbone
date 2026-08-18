---
type: "ai-sdlc.qa-strategy"
title: "QA Scope and Strategy"
description: "Risk-based QA scope, layers, data, environments, and suite intent."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-17T11:01:31Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "qa-strategy.md"
  path: "specs-refiniment/022-ai-sdlc-loop/qa-strategy.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-scope-and-strategy-design"
  flow_mode: "full"
  state_file: "specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-08-17"
  trace_ids:
    - "AC-001"
    - "AC-006"
    - "BR-001"
    - "BR-003"
    - "BR-005"
    - "BR-006"
    - "BR-007"
    - "DEC-001"
    - "DEC-005"
    - "REQ-001"
    - "REQ-006"
    - "REQ-009"
    - "WF-001"
    - "WF-005"
  related_artifacts:
    - "specs-refiniment/022-ai-sdlc-loop/backlog-gap-review.md"
    - "specs-refiniment/022-ai-sdlc-loop/backlog.md"
    - "specs-refiniment/022-ai-sdlc-loop/business-context.md"
    - "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
    - "specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md"
    - "specs-refiniment/022-ai-sdlc-loop/delivery-spec.md"
    - "specs-refiniment/022-ai-sdlc-loop/discovery.md"
    - "specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md"
    - "specs-refiniment/022-ai-sdlc-loop/index.md"
    - "specs-refiniment/022-ai-sdlc-loop/prfaq.md"
    - "specs-refiniment/022-ai-sdlc-loop/qa-gap-review.md"
    - "specs-refiniment/022-ai-sdlc-loop/qa.md"
    - "specs-refiniment/022-ai-sdlc-loop/release-slicing.md"
    - "specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md"
    - "specs-refiniment/022-ai-sdlc-loop/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-test-scope-and-strategy-design"
    - "qa-strategy"
    - "approved"
---

# qa-strategy.md

## Feature Summary
The strategy verifies that AI SDLC Loop remains small while enforcing high-assurance authority and state preservation. It prioritizes deterministic unit and integration coverage for installer, fingerprints, approvals, filesystem scope, command evidence, Git commit gating, promotion, and release identity, with hosted platform checks and concise stakeholder-readable UAT.

## Actors and Stakeholders
Contributors and reviewers drive functional and UAT scenarios; QA owns risk coverage, fixtures, and evidence; developers own unit and integration testability; security reviewers own abuse cases; Loop maintainers own hosted CI and release gates; Harness maintainers own promotion and submodule checks. Human approval semantics are tested as external authority inputs, never simulated as automatic policy.

## Scope and Boundaries
In scope are REQ-001 through REQ-009 across codex-project, claude-code-project, and agent-project, lifecycle and approvals, filesystem and Git invariants, evidence and redaction, compatible artifacts, public release, and Harness integration. Out of scope are model-output quality, UI/accessibility, notifications, performance load, telemetry, deployment, and unrelated Harness skills. Reliability is assessed through interruption, retry, drift, and deterministic rerun cases.

## Workflows and Failure Paths
WF-001 to WF-005 receive end-to-end integration coverage. State-transition tests cover uninstalled, installed, specified, spec-approved, implemented, verified-failed, verified-passing, commit-approved, committed, promoted, and released states. Every invalid transition is denied with invariant snapshots. Retry tests distinguish safe idempotency from stale evidence and never reuse approval across fingerprint changes.

## Requirements and Business Rules
All P0 requirements have functional, negative, permission, state, and traceability coverage. BR-003 and BR-005 receive the deepest combinatorial coverage because authority failures are critical. BR-007 adds preservation assertions to each error. BR-006 uses schema contract and round-trip tests. BR-001 and REQ-006 use table-driven profile tests. Acceptance and scenario IDs label cases and evidence.

## Data, Integrations, and Non-Functional Requirements
Test data is generated in temporary directories and disposable Git repositories. Unit tests avoid process and network dependence. Integration tests execute the Python CLI and controlled subprocess fixtures. Contract tests compare normalized schemas and profile manifests. Hosted tests cover OS/bootstrap differences. Security tests probe paths, symlinks, command arguments, receipts, secrets, and remote bootstrap. Performance benchmarking is not required because no threshold or scale claim exists.

## Dependencies, Risks, and Constraints
Detailed cases bind to final CLI help and schema constants. Symlink and executable-permission cases may be platform-specific. Windows locking and PowerShell bootstrap require hosted Windows. Public release and submodule resolution require authorized GitHub state and run last. Local suites must remain network-free and fast enough for every commit. Any unavailable critical hosted environment blocks the corresponding support claim or release.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-005 set suite scope. Owner: QA and maintainers. Impact: the matrix needs final command names, schema version, and CI jobs. Resolution: generate or assert public contracts from implementation constants, then require documentation and release tests to use those same contracts. Open questions: none. Excluded performance, UI, notification, and analytics testing is evidence-based because those surfaces and claims are absent from MVP.

## Success Measures
Strategy success is 100 percent traceability for AC-001 through AC-006 and SAC-001 through SAC-012, full P0 positive and negative automation, exact state-preservation assertions, promotion field equality, redaction checks, green local and hosted suites, and reproducible release/submodule identity. Smoke remains under a few launch-critical cases; regression covers all contract-sensitive paths; UAT remains readable to contributors, reviewers, and maintainers.

## Source Coverage
Consumed specs-refiniment/022-ai-sdlc-loop/index.md, specs-refiniment/022-ai-sdlc-loop/discovery.md, specs-refiniment/022-ai-sdlc-loop/prfaq.md, specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md, specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md, specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md, specs-refiniment/022-ai-sdlc-loop/backlog-gap-review.md, specs-refiniment/022-ai-sdlc-loop/backlog.md, specs-refiniment/022-ai-sdlc-loop/user-stories.md, specs-refiniment/022-ai-sdlc-loop/release-slicing.md, specs-refiniment/022-ai-sdlc-loop/business-context.md, specs-refiniment/022-ai-sdlc-loop/delivery-spec.md, specs-refiniment/022-ai-sdlc-loop/qa.md, specs-refiniment/022-ai-sdlc-loop/qa-gap-review.md, specs-refiniment/022-ai-sdlc-loop/decision-log.md, specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon. These sources cover goals, requirements, roles, workflows, accepted decisions, release slices, acceptance and scenario matrices, QA scope, testability findings, state, and index provenance.

## Test Scope
Must test: profile resolution and safe targets; exactly one installed skill; collisions, interruption, update drift, and verification; deterministic spec normalization and fingerprints; every approval decision and drift state; containment, symlink, and dirty-work preservation; command selection, preview, outcomes, timeouts, and redaction; Git index/HEAD invariants and exact approved commit; schema validation and promotion round trip; README commands, license, CI, release commit, and submodule pin. Nice to test: diagnostic wording variants and extra malformed-input combinations after P0 coverage.

## Risk and Coverage Priorities
| Risk | Likelihood | Impact | Coverage Layer | Priority | Owner |
| --- | --- | --- | --- | --- | --- |
| Approval bypass, replay, or stale fingerprint | Medium | Critical unauthorized mutation or commit | Unit state machine, integration CLI, security negative, UAT denial | P0 | Developer, QA, security |
| Path escape, symlink escape, or unrelated-work damage | Medium | Critical data loss or corruption | Unit path policy, filesystem integration, disposable Git regression | P0 | Developer, QA, security |
| Failed or misleading verification accepted as ready | Medium | Critical unverified commit | Unit evidence normalization, subprocess integration, end-to-end workflow | P0 | Developer and QA |
| Secret-like data retained in evidence | Medium | High exposure | Unit redaction, integration output fixture, security review | P0 | Security and developer |
| Lossy or permissive promotion | Low | High escalation failure | Schema contract, round-trip and rejection integration | P0 | Harness maintainer and QA |
| Profile or bootstrap drift | Medium | High install failure | Table-driven profile unit, hosted OS matrix, docs smoke | P1 | Loop maintainer |
| Release or submodule identity mismatch | Low | High supply-chain/integration risk | Hosted release and parent contract tests | P1 | Loop and Harness maintainers |
| Diagnostic wording regression | Medium | Low support friction | Snapshot subset and manual review | P2 | Docs and QA |

## Layer and Suite Strategy
Unit suite covers pure normalization, hashing, receipt validation, state transitions, path containment, profile mapping, evidence redaction, schema validation, and command selection. Integration suite invokes CLI against temporary roots and disposable Git repos. Security suite composes traversal, symlink, injection, replay, and secret fixtures. Contract suite verifies install manifest, compatible artifacts, docs commands, promotion, and submodule identity. Smoke proves install, approved happy path, denied mutation, failed verification, denied commit, and promotion. Regression adds all edge states. UAT mirrors contributor, reviewer, and maintainer outcomes.

## Test Data Strategy
Use table-driven values and factory helpers so every case declares profile, repository state, spec fingerprint, approval receipt, command outcome, expected transition, and preserved-state digest. Generate one-byte spec drift, reordered semantically equivalent input, current and previous receipts, clean/staged/unstaged/untracked/renamed/conflicting Git states, traversal and symlink targets, secret patterns, malformed and versioned artifacts, and known release commits. Seed or normalize time, paths, line endings, and ordering; never use real credentials or home paths.

## Environment Dependencies
Required local baseline: Python 3 supported by the product, Git, writable temporary directory, and POSIX shell where install.sh is exercised. Hosted matrix: Linux and macOS for POSIX bootstrap and permissions; Windows for install.py, path separators, locking, and PowerShell invocation. GitHub network and repository permissions are needed only for release and submodule evidence. Symlink cases declare capability skips, but at least one supported hosted OS must execute them. Missing matrix evidence blocks the affected compatibility claim.

## Automation Strategy
Run fast unit and local integration suites on every pull request. Run full security, docs, and promotion contracts on every candidate and protected branch. Run OS matrix for every release candidate. Make tests hermetic, standard-library-first, and parallel-safe through unique temporary roots. Capture command, exit code, normalized summary, and relevant artifact digests. Avoid broad snapshot tests for volatile prose. A case may be manual only when it validates human comprehension or external visibility; all authority and preservation rules remain automated.

## Strategy Risks
SR-001 over-broad end-to-end tests could be slow and brittle; mitigate with pure units plus few critical E2E paths. SR-002 platform skips could hide support gaps; mitigate with required hosted jobs and claim gating. SR-003 fixtures could accidentally touch user state; mitigate with validated temporary roots and explicit guard tests. SR-004 tests could duplicate implementation logic; mitigate with black-box contract assertions and independent expected fixtures. SR-005 release tests could mutate external state unexpectedly; mitigate with explicit authorization, dry checks first, and execution only in the release workflow.
