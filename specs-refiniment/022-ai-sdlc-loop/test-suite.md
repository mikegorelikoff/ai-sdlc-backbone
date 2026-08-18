---
type: "ai-sdlc.test-suite"
title: "Test Suite"
description: "Executable smoke, regression, and acceptance suite definitions."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-17T11:05:04Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "test-suite.md"
  path: "specs-refiniment/022-ai-sdlc-loop/test-suite.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-case-and-suite-synthesis"
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
    - "BR-002"
    - "BR-003"
    - "BR-004"
    - "BR-005"
    - "BR-006"
    - "BR-007"
    - "DEC-001"
    - "DEC-004"
    - "DEC-005"
    - "REQ-001"
    - "REQ-009"
    - "TC-001"
    - "TC-002"
    - "TC-004"
    - "TC-005"
    - "TC-006"
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
    - "TC-019"
    - "TC-020"
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
    - "specs-refiniment/022-ai-sdlc-loop/test-cases.md"
    - "specs-refiniment/022-ai-sdlc-loop/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-test-case-and-suite-synthesis"
    - "test-suite"
    - "approved"
---

# test-suite.md

## Feature Summary
This artifact groups TC-001 through TC-024 into executable suites that balance fast feedback and release assurance. Smoke proves the product is alive and fail-closed on its two most important authority boundaries. Regression covers every maintained contract. Security isolates abuse and preservation risks. Hosted release covers platform and identity. UAT preserves genuine human approval instead of automating it away.

## Actors and Stakeholders
Developers own unit and local integration execution; QA owns smoke, regression, evidence, and readiness; security reviewers own the abuse suite; Loop maintainers own hosted matrix and public release checks; Harness maintainers own promotion and submodule checks; contributors and reviewers execute UAT. A suite failure routes to its owner and blocks dependent suites; no owner may waive a P0 authority or preservation failure.

## Scope and Boundaries
Suites cover exactly the 24 designed cases and all nine requirements. They do not add cases for excluded UI, notification, performance, telemetry, deployment, model quality, or unrelated Harness behavior. Parent regression is limited to documentation, generated catalogs, build/render validation, and the submodule integration. Public network writes appear only in the authorized release sequence.

## Workflows and Failure Paths
Smoke traverses install, Specify, approved Implement, passing Verify, approved commit, and promotion while also proving mutation and commit denials. Regression expands every WF-001 through WF-005 state and exception. Security focuses on traversal, symlinks, replay, redaction, and repository trust. Hosted release checks cross-platform install and identity. UAT observes the full contributor/reviewer handoff and exact fingerprints.

## Requirements and Business Rules
REQ-001 through REQ-009 are covered across suites without relying on one monolithic end-to-end test. BR-001, BR-002, BR-004, and BR-006 have contract coverage; BR-003, BR-005, and BR-007 appear in smoke, regression, and security where applicable. AC-001 through AC-006 and SAC-001 through SAC-012 map through TC IDs. Any coverage removal requires an updated strategy and accepted decision, not an informal skip.

## Data, Integrations, and Non-Functional Requirements
Local suites consume generated temporary roots, Git repositories, specs, approvals, command fixtures, and promotion artifacts. Hosted suites add real OS shells, PowerShell, GitHub Actions metadata, public repository visibility, tag targets, and the parent gitlink. Evidence includes command, commit, environment, exit, normalized result, and relevant digests. Synthetic secrets never leave fixtures; real credentials are neither collected nor written to evidence.

## Dependencies, Risks, and Constraints
Unit tests precede local integration; local integration precedes smoke; smoke and security precede full regression; promotion and docs precede hosted release; hosted release precedes parent pin and UAT signoff. Windows, macOS, and public GitHub evidence depend on hosted infrastructure. Release identity tests require a published tag and therefore run after explicit external-write authorization. A missing critical environment blocks the claim it supports.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-005 define suite boundaries and authority. Owner: QA and maintainers. Impact: exact CI job names and release tag are implementation-bound. Resolution: bind suite triggers to final workflow configuration and candidate identity, then store commit-specific evidence. Open questions: none. Manual UAT is intentional and permanent because automatic approval would contradict DEC-004; all observable system behavior around it remains automated.

## Success Measures
A pull request is locally ready when unit, integration, smoke, security, promotion, docs, compile, and diff suites pass. A release candidate is ready when the full regression and hosted OS matrix pass for one commit. Publication is ready when public identity and parent gitlink equal that commit. Final signoff requires UAT with two genuine explicit approvals. Zero P0 failure, unexpected mutation, secret exposure, lossy promotion, or required-suite skip is acceptable.

## Source Coverage
Consumed specs-refiniment/022-ai-sdlc-loop/index.md, specs-refiniment/022-ai-sdlc-loop/discovery.md, specs-refiniment/022-ai-sdlc-loop/prfaq.md, specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md, specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md, specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md, specs-refiniment/022-ai-sdlc-loop/backlog-gap-review.md, specs-refiniment/022-ai-sdlc-loop/backlog.md, specs-refiniment/022-ai-sdlc-loop/user-stories.md, specs-refiniment/022-ai-sdlc-loop/release-slicing.md, specs-refiniment/022-ai-sdlc-loop/business-context.md, specs-refiniment/022-ai-sdlc-loop/delivery-spec.md, specs-refiniment/022-ai-sdlc-loop/qa.md, specs-refiniment/022-ai-sdlc-loop/qa-gap-review.md, specs-refiniment/022-ai-sdlc-loop/qa-strategy.md, specs-refiniment/022-ai-sdlc-loop/test-cases.md, specs-refiniment/022-ai-sdlc-loop/decision-log.md, and specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon.

## Suite Coverage Matrix
| Suite | Purpose | Test IDs | Trigger | Environment | Owner |
| --- | --- | --- | --- | --- | --- |
| UNIT | Prove deterministic pure contracts quickly | TC-005 plus helper-level assertions supporting TC-001, TC-006, TC-009, TC-010 through TC-017 | Every change and pull request | Local Python, no network | Developer |
| SMOKE | Prove launch-critical happy path and fail-closed authority | TC-001, TC-004, TC-006, TC-008, TC-010, TC-011, TC-013, TC-014, TC-016 | Pull request after unit/integration; every candidate | Disposable local roots and Git | QA |
| SECURITY | Prove containment, replay resistance, redaction, and repository trust | TC-002, TC-006, TC-009, TC-012, TC-013, TC-015, TC-017, TC-019 | Pull request and candidate | Local isolated fixtures | Security reviewer |
| REGRESSION | Prove every maintained contract and negative path | TC-001 through TC-019 | Candidate and protected branch | Local Linux plus portable fixtures | QA |
| HOSTED-RELEASE | Prove platforms, public identity, parent pin, and parent regressions | TC-020 through TC-023 | Authorized release candidate and parent integration | GitHub Linux, macOS, Windows; parent checkout | Loop and Harness maintainers |
| UAT | Prove user value and explicit human authority end to end | TC-024 | Candidate after all automated suites | Disposable consumer repository | Contributor, reviewer, QA |

## Smoke Suite
Run python3 -m unittest tests.test_install.InstallProfileTests tests.test_workflow.SpecifyTests tests.test_workflow.ImplementDenialTests tests.test_workflow.ScopedMutationTests tests.test_workflow.VerifyPassTests tests.test_workflow.VerifyFailureTests tests.test_workflow.CommitDenialTests tests.test_workflow.CommitApprovalTests tests.test_promotion.PromotionRoundTripTests -v. Entry: code compiles and unit helpers pass. Exit: TC-001, TC-004, TC-006, TC-008, TC-010, TC-011, TC-013, TC-014, and TC-016 pass on one commit with no leftover fixture state. Failure action: stop all release-dependent work and route to developer plus QA.

## Regression Suite
Run python3 -m unittest discover -s tests -v, python3 -m compileall install.py skills tests, documented CLI help/verification fixtures, and git diff --check. This executes TC-001 through TC-019 including install drift, fingerprint boundaries, all approval states, filesystem/Git preservation, subprocess failures, redaction, promotion rejection, docs, and repository trust. Entry: smoke and security pass. Exit: all local tests pass twice where determinism is asserted, with no unowned skip or workspace mutation. Failure blocks hosted release.

## UAT Suite
TC-024 checklist: install Loop into a disposable supported profile; verify exactly one skill; submit a bounded change; inspect and approve the displayed spec fingerprint; confirm only approved paths change; inspect passing evidence; approve the displayed verified-change fingerprint; confirm exactly one commit; promote the artifact and compare trace fields. Entry: regression, hosted matrix, promotion, and release identity pass. Exit: contributor, reviewer, and QA record Pass with candidate commit and both fingerprints. Any confusing authority prompt or mismatched evidence is Fail.

## Entry Criteria
UNIT requires readable source and fixtures. SMOKE requires compiled candidate, final CLI help, schema constants, and disposable Git identity. SECURITY requires containment and secret fixtures. REGRESSION requires all designed test modules and smoke/security green. HOSTED-RELEASE requires one immutable candidate commit, public CI configuration, authorized GitHub access, and green local regression. Parent integration requires the validated public commit. UAT requires all automated suites green, published candidate identity, and available independent contributor and reviewer.

## Exit Criteria
UNIT exits with all pure assertions green. SMOKE exits with nine critical cases green and zero protected-state delta. SECURITY exits with no open critical/high finding and all abuse cases green. REGRESSION exits with TC-001 through TC-019 green, deterministic reruns stable, and no unowned skip. HOSTED-RELEASE exits with TC-020 through TC-023 green for the same commit. UAT exits with TC-024 signed by contributor, reviewer, and QA. Overall release exits only when every suite passes and evidence references one exact commit.

## Execution Dependencies
Order: UNIT; local integration; SMOKE and SECURITY; REGRESSION; promotion/docs checks; HOSTED-RELEASE platform matrix; authorized repository/tag identity; Harness submodule and parent regression; UAT; signoff. Parallelism: SMOKE and SECURITY may run after shared units; platform jobs run in parallel; promotion/docs may run alongside local regression after schema stability. Serialization: tag publication precedes release identity, which precedes submodule pin. On failure, cancel downstream work, retain evidence, fix without rewriting user state, and restart from the earliest affected suite.
