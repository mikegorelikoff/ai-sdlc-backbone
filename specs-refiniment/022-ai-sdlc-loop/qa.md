---
type: "ai-sdlc.qa-plan"
title: "QA Plan"
description: "Acceptance, regression, risk, and manual validation plan."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-17T10:58:55Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "qa.md"
  path: "specs-refiniment/022-ai-sdlc-loop/qa.md"
  workspace: "refinement"
  skill: "ai-sdlc-qa"
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
    - "BR-007"
    - "DEC-001"
    - "DEC-005"
    - "REQ-001"
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
    - "specs-refiniment/022-ai-sdlc-loop/release-slicing.md"
    - "specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md"
    - "specs-refiniment/022-ai-sdlc-loop/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-qa"
    - "qa"
    - "approved"
---

# qa.md

## Feature Summary
QA covers the independently released AI SDLC Loop package, its one-skill installers, the Specify–Implement–Verify lifecycle, two fingerprint-bound approvals, deterministic evidence, Harness-compatible promotion, public repository release, and parent submodule pin. The highest-risk outcomes are unauthorized mutation or commit, damage to unrelated work, unsafe installation, and compatibility loss.

## Actors and Stakeholders
Contributors exercise install and workflow paths; reviewers exercise allow and deny decisions; Loop maintainers own automated suites and release evidence; Harness maintainers own promotion and submodule checks; QA owns scenario coverage and signoff; security reviewers own abuse cases. QA must never fabricate approval, skip a failure, or treat a prose claim as execution evidence.

## Scope and Boundaries
Coverage includes codex-project, claude-code-project, agent-project with safe and unsafe roots, clean and conflicting installs, specification fingerprints, every approval state, scoped and overlapping dirty work, passing and failing commands, Git index and history, valid and incompatible artifacts, CI, license, documentation, release resolution, and submodule pinning. Deployment, telemetry, model quality, and the full Harness catalog are excluded.

## Workflows and Failure Paths
Test WF-001 through WF-005 end to end and at every state boundary. Installation failures must preserve unrelated files. Specify drift must invalidate implementation approval. Mutation denial must leave tracked, untracked, staged, and unstaged fixtures unchanged. Verification failure must retain evidence but deny commit readiness. Commit denial must preserve index and HEAD. Promotion and release failures must not produce partial or falsely successful state.

## Requirements and Business Rules
The QA baseline is REQ-001 through REQ-009, BR-001 through BR-007, AC-001 through AC-006, SAC-001 through SAC-012, and SCN-001 through SCN-014. Each requirement needs a positive assertion, applicable negative assertion, state-preservation assertion, and evidence assertion. Approval and path-safety rules are release blockers and cannot be waived by manual observation.

## Data, Integrations, and Non-Functional Requirements
Fixtures include profile roots, one-skill manifests, bounded specs, normalized fingerprints, approved and stale receipts, clean and dirty Git repositories, command outcomes, validation evidence, compatible and incompatible artifacts, and submodule commits. Tests isolate HOME-like paths, use temporary directories, freeze unstable values, redact secret-like strings, avoid network except explicit release checks, and compare deterministic normalized outputs.

## Dependencies, Risks, and Constraints
Pre-release QA depends on implemented CLI contracts, stable schema version, and a candidate commit. Cross-platform bootstrap confidence depends on Linux, macOS, and Windows CI where available. Git tests require configured disposable identities. GitHub release and submodule tests require network and repository authority and therefore run only in the authorized release path. Local full-flow planning does not claim those future checks passed.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-005 fix the QA scope. Owner: QA and maintainers. Impact: cross-platform and public-release evidence cannot be completed until implementation and CI exist. Resolution and next step: build deterministic local tests first, then require hosted CI and release-resolution evidence before launch. Open questions: none that change coverage; exact workflow command names will be bound to the final CLI help and tested documentation.

## Success Measures
Signoff requires all P0 automated cases to pass, zero unexplained changed paths after denied actions, exact profile/target placement, stable fingerprints, explicit actionable failures, promotion round-trip equality, no secret leakage in evidence, tested README commands, public CI success, and the Harness submodule resolving the approved commit. Any failure in approval, path, dirty-work, evidence, compatibility, or release integrity blocks launch.

## Source Coverage
Consumed specs-refiniment/022-ai-sdlc-loop/index.md, specs-refiniment/022-ai-sdlc-loop/discovery.md, specs-refiniment/022-ai-sdlc-loop/prfaq.md, specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md, specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md, specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md, specs-refiniment/022-ai-sdlc-loop/backlog-gap-review.md, specs-refiniment/022-ai-sdlc-loop/backlog.md, specs-refiniment/022-ai-sdlc-loop/user-stories.md including Scenario Coverage Matrix line 145, specs-refiniment/022-ai-sdlc-loop/release-slicing.md, specs-refiniment/022-ai-sdlc-loop/business-context.md, specs-refiniment/022-ai-sdlc-loop/delivery-spec.md, specs-refiniment/022-ai-sdlc-loop/decision-log.md, and specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon.

## Acceptance Scenarios
AS-001 verifies each supported profile installs exactly one skill and an invalid or interrupted install preserves unrelated files. AS-002 verifies Specify produces schema-valid deterministic output. AS-003 verifies absent, rejected, stale, mismatched, and matching specification approvals. AS-004 verifies scoped mutation, path containment, symlink handling, and dirty-work preservation. AS-005 verifies relevant pass, fail, unavailable, and nondeterministic command evidence. AS-006 verifies absent, stale, and matching commit approval plus unchanged index and HEAD on denial. AS-007 verifies promotion round trip and incompatible rejection. AS-008 verifies public release and submodule identity.

## Regression Targets
Preserve Harness profile semantics and safe custom-root rules; avoid changes to existing parent installers or the 45-skill package; preserve repository user changes during submodule integration; keep documentation navigation order and product-family wording; keep generated catalogs generated; preserve Git behavior outside the Loop disposable fixtures; and ensure Loop remains independently usable without its parent checkout. Parent docs, build, unit, rendered, and diff checks are regression gates after integration.

## Risk-Based Coverage
P0: approval bypass/replay, path traversal or symlink escape, unrelated-work mutation, commit without passing evidence, secret leakage, and lossy promotion. P1: profile drift, interrupted installation recovery, command selection mismatch, deterministic output, cross-platform bootstrap, submodule pin mismatch, and stale documentation. P2: diagnostic wording and cosmetic README layout. P0 requires automated positive and negative tests plus state snapshots; P1 requires automated fixtures and hosted matrix evidence; P2 may use manual review.

## Test Data and Environment
Use temporary repositories with clean, staged, unstaged, untracked, renamed, and conflicting paths; fixture specs differing by one normalized byte; approvals for current and prior fingerprints; command fixtures returning zero, nonzero, signal, timeout, missing executable, and secret-like output; valid, newer, older, malformed, and unknown-field promotion artifacts; clean and conflicting profile roots; and a disposable parent repository with a known submodule commit. No fixture may target the real home directory or workspace root recursively.

## Validation Commands
Planned Loop checks: python3 -m unittest discover -s tests -v; python3 -m compileall install.py skills tests; python3 install.py --help; each documented install verification against temporary codex-project, claude-code-project, and agent-project roots; git diff --check. Planned parent checks: python3 docs/scripts/build_catalog.py --check; python3 docs/scripts/validate_docs.py; python3 -m unittest discover -s docs/tests -v; mkdocs build --strict; python3 docs/scripts/validate_rendered.py site; git diff --check. Results remain planned until implementation execution records exact exit status.

## Manual Checks
Review the installed skill discovery in each host-shaped directory; inspect approval prompts for clear action, scope, and fingerprint; confirm denial messages explain recovery without implying approval; inspect evidence redaction and command previews; read the one-command install, separate verify, workflow, security, compatibility, and escalation docs; confirm public repository visibility, Apache-2.0 license rendering, CI badge/link, release tag, and submodule link; and verify no full Harness-only claim appears in Loop documentation.

## Signoff Criteria
QA signoff is Pass only when every P0 case and all documented commands pass on the candidate commit, hosted profile/platform evidence is green, security review has no open critical or high finding, promotion is lossless, and the parent pins that exact commit. Signoff is Blocked for any approval bypass, unexpected mutation, failed relevant check accepted as ready, secret exposure, unsafe path, invalid profile claim, incompatible partial output, failing CI, or submodule mismatch. Residual low-risk cosmetic issues require an owner and release note.
