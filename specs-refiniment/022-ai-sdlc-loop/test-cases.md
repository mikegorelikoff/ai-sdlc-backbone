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
  at: "2026-08-17T11:03:14Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "test-cases.md"
  path: "specs-refiniment/022-ai-sdlc-loop/test-cases.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-cases"
  flow_mode: "full"
  state_file: "specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
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
    - "BR-001"
    - "BR-002"
    - "BR-004"
    - "BR-005"
    - "BR-006"
    - "BR-007"
    - "DEC-001"
    - "DEC-005"
    - "REQ-001"
    - "REQ-002"
    - "REQ-003"
    - "REQ-004"
    - "REQ-005"
    - "REQ-006"
    - "REQ-007"
    - "REQ-008"
    - "REQ-009"
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
    - "TC-021"
    - "TC-022"
    - "TC-023"
    - "TC-024"
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
    - "specs-refiniment/022-ai-sdlc-loop/qa-strategy.md"
    - "specs-refiniment/022-ai-sdlc-loop/qa.md"
    - "specs-refiniment/022-ai-sdlc-loop/release-slicing.md"
    - "specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md"
    - "specs-refiniment/022-ai-sdlc-loop/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-test-cases"
    - "test-cases"
    - "approved"
---

# test-cases.md

## Feature Summary
These cases prove the complete AI SDLC Loop MVP through observable filesystem, process, artifact, and Git outcomes. The matrix emphasizes denial invariants and deterministic evidence, then covers profile installation, the approved happy path, promotion compatibility, public release, and parent submodule identity. Every case maps to one primary layer and an explicit automation path.

## Actors and Stakeholders
Contributor cases cover install, specify, implementation, verification, and commit requests. Reviewer cases cover approve, reject, and stale authority. Loop maintainer cases cover package, CI, documentation, and release. Harness maintainer cases cover promotion and submodule. QA and security own assertions and abuse fixtures. No test treats the runtime, maintainer, or test harness as a substitute reviewer.

## Scope and Boundaries
In scope are all P0 requirements and acceptance criteria for three install profiles, one skill, state transitions, two approvals, scoped mutation, commands, evidence, Git, compatibility, public release, and submodule. Cases for model quality, UI, notifications, load, telemetry, deployment, and unrelated Harness catalog features are excluded. Parent regression is limited to paths changed for Loop integration.

## Workflows and Failure Paths
Cases cover WF-001 through WF-005 and SCN-001 through SCN-014. Negative variants include missing, malformed, conflicting, interrupted, stale, mismatched, traversing, symlinked, dirty, failing, timed-out, secret-bearing, incompatible, and drifted states. Retry and idempotency are tested where install and verification can safely repeat; approvals intentionally become invalid after relevant content changes.

## Requirements and Business Rules
TC-001 through TC-024 cover REQ-001 through REQ-009, BR-001 through BR-007, AC-001 through AC-006, and SAC-001 through SAC-012. Authority rules receive distinct absent, rejected, stale, mismatched, and matching cases. BR-007 is asserted as a before/after digest or Git identity for each denied path. No expected result uses subjective language.

## Data, Integrations, and Non-Functional Requirements
Factories create isolated profile roots, repositories, specs, receipts, command fixtures, artifacts, and parent/submodule candidates. Tests normalize time, path prefixes, line endings, and ordering before comparing evidence. Integrations are black-box CLI, filesystem, subprocess, Git, GitHub release, and Harness promotion. Secret fixtures use synthetic markers. Public-network cases execute only in the authorized release job.

## Dependencies, Risks, and Constraints
Automation paths assume final modules tests.test_install, tests.test_workflow, tests.test_security, tests.test_promotion, and tests.test_release; implementation must preserve these traceable groupings or update this artifact before test coding. Hosted Windows and GitHub cases cannot be fully proven by local execution. Symlink cases require platform support. External writes remain explicitly authorized and occur only after all read-only and local gates pass.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-005 define expected behavior. Owner: developer and QA. Impact: final CLI spelling and schema version may change exact invocations but not scenarios. Resolution: bind test helpers to public parser and schema constants; assert README commands against --help. Open questions: none. Decisions required: none, because exclusions, authority, failure states, environment ownership, and release gates are already accepted.

## Success Measures
The case set is complete when every requirement and acceptance criterion maps to at least one P0 case, each permission denial checks protected-state equality, every automation path is implemented and green, hosted cases cover advertised environments, and manual release visibility checks are recorded. A failing P0 case blocks implementation completion or release; P1 platform or identity failures block the associated support or publication claim.

## Source Coverage
Consumed specs-refiniment/022-ai-sdlc-loop/index.md, specs-refiniment/022-ai-sdlc-loop/discovery.md, specs-refiniment/022-ai-sdlc-loop/prfaq.md, specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md, specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md, specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md, specs-refiniment/022-ai-sdlc-loop/backlog-gap-review.md, specs-refiniment/022-ai-sdlc-loop/backlog.md, specs-refiniment/022-ai-sdlc-loop/user-stories.md, specs-refiniment/022-ai-sdlc-loop/release-slicing.md, specs-refiniment/022-ai-sdlc-loop/business-context.md, specs-refiniment/022-ai-sdlc-loop/delivery-spec.md, specs-refiniment/022-ai-sdlc-loop/qa.md, specs-refiniment/022-ai-sdlc-loop/qa-gap-review.md, specs-refiniment/022-ai-sdlc-loop/qa-strategy.md, specs-refiniment/022-ai-sdlc-loop/decision-log.md, and specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon.

## Scenario Matrix
| Scenario ID | Requirement Ref | Type | Preconditions | Expected Outcome |
| --- | --- | --- | --- | --- |
| TSC-001 | REQ-001, REQ-006, AC-001 | Positive table | Clean roots for all three profiles | Exactly one ai-sdlc directory and valid install record exist at each resolved target |
| TSC-002 | REQ-001, BR-007 | Negative | Unsupported profile, unsafe root, collision, and injected interruption fixtures | Nonzero result, actionable error, and unrelated-tree digest unchanged |
| TSC-003 | REQ-001, REQ-006 | Retry/drift | Verified install, repeated install, then changed managed file | Safe retry is idempotent; drift is reported and not overwritten |
| TSC-004 | REQ-002, AC-002 | Positive | Bounded valid request | Schema-valid spec and stable fingerprint persist before mutation |
| TSC-005 | REQ-002, BR-002 | Boundary | Equivalent normalized requests and one-byte semantic drift | Equivalent input hashes equally; semantic drift changes fingerprint |
| TSC-006 | REQ-003, AC-003 | Authorization negative | Missing, rejected, stale, and mismatched spec approvals | Implement is denied and repository digest is unchanged |
| TSC-007 | REQ-003, AC-003 | Authorization positive | Approval matches current spec fingerprint | Approval receipt persists and Implement becomes eligible |
| TSC-008 | REQ-004, BR-007 | Positive | Approved scope and clean target | Only declared files change and change fingerprint is recorded |
| TSC-009 | REQ-004, BR-007 | Security/boundary | Traversal, absolute, symlink escape, overlap, and unrelated dirty fixtures | Mutation is denied or safely isolated; unrelated state is byte-identical |
| TSC-010 | REQ-005, AC-004 | Positive | Approved change and passing relevant commands | Commands, exits, normalized summaries, and verified fingerprint persist |
| TSC-011 | REQ-005, BR-004 | Failure | Failing, missing, timed-out, and signaled commands | Commit readiness is false and exact failure evidence persists |
| TSC-012 | REQ-005, BR-004 | Security/privacy | Command emits synthetic secret patterns | Evidence is redacted and retains enough non-secret diagnostic context |
| TSC-013 | REQ-005, AC-005 | Authorization negative | Missing, rejected, stale, or mismatched verified-change approval | Commit is denied; index tree and HEAD remain unchanged |
| TSC-014 | REQ-005, AC-005 | Authorization positive | Passing evidence and matching commit approval | Exactly approved paths form one traceable commit |
| TSC-015 | REQ-005, BR-005 | Drift/retry | Approval exists, then file, index, or evidence changes | Prior approval is invalid and no additional commit is created |
| TSC-016 | REQ-007, AC-006 | Contract positive | Valid minimal Loop artifact | Harness promotion preserves every supported field and trace ID |
| TSC-017 | REQ-007, BR-006 | Contract negative | Malformed, unknown incompatible, older, and newer fixtures | Unsupported input is rejected without partial output |
| TSC-018 | REQ-008 | Documentation/CLI | Candidate README and parser | Every documented command parses and matches help |
| TSC-019 | REQ-008 | Security/release | Candidate repository tree | Apache-2.0, security guidance, no secrets, and required CI files exist |
| TSC-020 | REQ-008 | Hosted matrix | Candidate commit in public CI | Linux, macOS, and Windows required jobs pass |
| TSC-021 | REQ-008, REQ-009 | Release identity | Authorized public candidate and tag | Tag resolves to validated commit and repository is public |
| TSC-022 | REQ-009 | Parent integration | Clean Harness branch and validated public commit | products/ai-sdlc-loop is a submodule pinned to that commit |
| TSC-023 | REQ-009, BR-007 | Parent regression | Parent docs and submodule changes | Required Harness docs, unit, build, render, and diff checks pass |
| TSC-024 | REQ-001 through REQ-009 | End-to-end UAT | Installed Loop and bounded disposable change | Contributor and reviewer complete happy path with two explicit approvals and promotion evidence |

## Detailed Test Cases
| Test ID | Scenario Ref | Steps | Expected Result | Priority | Automation |
| --- | --- | --- | --- | --- | --- |
| TC-001 | TSC-001 | Create three roots; invoke each profile; run verify; enumerate visible skills | Each target contains only ai-sdlc and verification exits 0 | P0 | tests/test_install.py; python3 -m unittest tests.test_install.InstallProfileTests -v |
| TC-002 | TSC-002 | Snapshot root; run each invalid/interrupted fixture; resnapshot | Each invocation exits nonzero and before/after unrelated digest matches | P0 | tests/test_install.py; python3 -m unittest tests.test_install.InstallFailureTests -v |
| TC-003 | TSC-003 | Install twice; alter managed file; invoke verify/update check | Second clean install is no-op; drift is reported without overwrite | P1 | tests/test_install.py; python3 -m unittest tests.test_install.InstallDriftTests -v |
| TC-004 | TSC-004 | Run Specify twice on same request; validate artifact | Both runs yield valid identical fingerprint and no source mutation | P0 | tests/test_workflow.py; python3 -m unittest tests.test_workflow.SpecifyTests -v |
| TC-005 | TSC-005 | Hash normalized equivalents and semantic drift variant | Equivalent pair matches; semantic variant differs | P0 | tests/test_workflow.py; python3 -m unittest tests.test_workflow.FingerprintTests -v |
| TC-006 | TSC-006 | Snapshot repo; attempt Implement for four invalid approval states | All fail and full repository digest matches snapshot | P0 | tests/test_workflow.py; python3 -m unittest tests.test_workflow.ImplementDenialTests -v |
| TC-007 | TSC-007 | Approve current spec; request Implement eligibility | Receipt fields match feature, action, fingerprint, and decision | P0 | tests/test_workflow.py; python3 -m unittest tests.test_workflow.ImplementApprovalTests -v |
| TC-008 | TSC-008 | Apply approved fixture; compare changed paths | Changed path set equals approved set and unrelated digest matches | P0 | tests/test_workflow.py; python3 -m unittest tests.test_workflow.ScopedMutationTests -v |
| TC-009 | TSC-009 | Run traversal, absolute, symlink, overlap, and dirty fixtures | No path escapes root and unrelated Git/file snapshots match | P0 | tests/test_security.py; python3 -m unittest tests.test_security.PathSafetyTests -v |
| TC-010 | TSC-010 | Run passing relevant commands twice; compare evidence | Exit records are complete and normalized evidence/fingerprint match | P0 | tests/test_workflow.py; python3 -m unittest tests.test_workflow.VerifyPassTests -v |
| TC-011 | TSC-011 | Run fail, missing, timeout, and signal commands | Each blocks readiness and records distinguishable failure evidence | P0 | tests/test_workflow.py; python3 -m unittest tests.test_workflow.VerifyFailureTests -v |
| TC-012 | TSC-012 | Emit synthetic token/password/private-key markers | Raw markers are absent; redaction labels and non-secret context remain | P0 | tests/test_security.py; python3 -m unittest tests.test_security.EvidenceRedactionTests -v |
| TC-013 | TSC-013 | Snapshot index and HEAD; attempt commit for invalid approvals | All fail; index tree and HEAD IDs are unchanged | P0 | tests/test_workflow.py; python3 -m unittest tests.test_workflow.CommitDenialTests -v |
| TC-014 | TSC-014 | Approve current verified fingerprint; commit | HEAD advances once and committed paths/digest equal approved change | P0 | tests/test_workflow.py; python3 -m unittest tests.test_workflow.CommitApprovalTests -v |
| TC-015 | TSC-015 | Approve; alter file/index/evidence separately; retry commit | Each invalidates receipt and HEAD does not advance | P0 | tests/test_security.py; python3 -m unittest tests.test_security.ApprovalReplayTests -v |
| TC-016 | TSC-016 | Promote valid fixture; compare canonical field map | All supported fields and trace IDs are equal | P0 | tests/test_promotion.py; python3 -m unittest tests.test_promotion.PromotionRoundTripTests -v |
| TC-017 | TSC-017 | Promote invalid version/shape fixtures into empty target | Each fails and target remains empty | P0 | tests/test_promotion.py; python3 -m unittest tests.test_promotion.PromotionRejectionTests -v |
| TC-018 | TSC-018 | Extract documented commands; run parser/help checks | Commands parse, help lists them, and docs contain no unsupported option | P1 | tests/test_docs.py; python3 -m unittest tests.test_docs.DocumentedCommandTests -v |
| TC-019 | TSC-019 | Scan candidate tree and tracked content | License/security/CI exist; no synthetic or detected secret is tracked | P0 | tests/test_security.py; python3 -m unittest tests.test_security.RepositoryTrustTests -v |
| TC-020 | TSC-020 | Run required GitHub Actions matrix on candidate | Every required OS job succeeds for the same commit | P1 | CI step loop-test-matrix; gh pr checks --required |
| TC-021 | TSC-021 | Query repository visibility and tag target | Repository is public and tag object resolves to candidate commit | P1 | tests/test_release.py; python3 -m unittest tests.test_release.ReleaseIdentityTests -v |
| TC-022 | TSC-022 | Inspect .gitmodules, gitlink, and remote commit | Path and URL match contract; gitlink equals released commit | P0 | parent integration test; git submodule status products/ai-sdlc-loop |
| TC-023 | TSC-023 | Run parent canonical validation commands | Every command exits 0 and generated output is unchanged | P0 | Parent AGENTS.md validation sequence |
| TC-024 | TSC-024 | Human follows install, Specify, approve, Implement, Verify, approve commit, promote checklist | Each prompt names current fingerprint and final evidence traces to one commit | P0 | Manual — execute at release candidate — blocker: requires human approval decisions |

## Permission and Negative Cases
TC-006 and TC-013 separately cover missing, rejected, stale, and mismatched approvals; TC-015 covers replay after file, index, and evidence drift. TC-009 covers traversal, absolute roots, symlinks, overlapping scope, and unrelated dirty work. TC-002 covers unsupported and interrupted installation. TC-011 covers process failure modes, TC-012 secret output, TC-017 schema/version rejection, and TC-023 parent regressions. For every denial, assert nonzero status, actionable reason, no protected transition, and exact protected-state equality.

## Expected Results
Filesystem preservation uses sorted relative-path, type, mode where portable, and SHA-256 content maps. Git preservation uses HEAD object ID, index tree or staged diff digest, tracked diff, and untracked content map. Artifact equality uses parsed canonical fields rather than formatting. Approval success requires receipt action, feature, fingerprint, decision, and timestamp; denial requires no new valid receipt. Verification success requires command, cwd, exit, normalized summary, and fingerprint; failure requires readiness false. Promotion failure requires no target artifact. Release identity requires public visibility and exact commit equality.

## Layer Mapping
Unit: TC-005 plus pure helpers behind profile, receipt, path, evidence, and schema cases. Integration: TC-001 through TC-004, TC-006 through TC-011, TC-013, TC-014, TC-016 through TC-018, and TC-021. Security: TC-009, TC-012, TC-015, TC-019. Hosted contract: TC-020, TC-022, TC-023. QA/manual: TC-024 only because it validates human comprehension and explicit authority. Execution order: units first; local integration/security second; promotion/docs third; hosted matrix fourth; public release and parent integration fifth; UAT/signoff last. Any failure blocks later dependent layers.

## Automation Plan
Implement traceable classes and methods whose names include TC IDs. Every pull request runs unit, install, workflow, security, promotion, docs, compile, and diff checks without network. Release candidates additionally run the hosted OS matrix, release identity checks after authorized publication, parent submodule checks, and canonical Harness validation. Evidence records the exact invocation and commit. TC-024 remains manual because automating approval would invalidate the requirement; execute it for the release candidate and retain the checklist. There are no deferred automation dates or unowned cases.
