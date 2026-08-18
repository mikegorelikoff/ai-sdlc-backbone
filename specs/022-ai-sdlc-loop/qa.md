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
  at: "2026-08-17T11:13:45Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "qa.md"
  path: "specs/022-ai-sdlc-loop/qa.md"
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
    - "TC-024"
  related_artifacts:
    - "specs/022-ai-sdlc-loop/branch-plan.md"
    - "specs/022-ai-sdlc-loop/decision-log.md"
    - "specs/022-ai-sdlc-loop/design.md"
    - "specs/022-ai-sdlc-loop/index.md"
    - "specs/022-ai-sdlc-loop/requirements.md"
    - "specs/022-ai-sdlc-loop/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "approved"
    - "ai-sdlc-loop"
---

# QA

## Change Summary
Create the public AI SDLC Loop repository, its namespaced seventeen-member portable skill package and approval-gated Specify → Implement → Verify runtime, then pin the validated repository as the Harness submodule `products/ai-sdlc-loop` and add minimal product-family documentation.

## Acceptance Scenarios
QA-001: each supported profile installs and verifies the exact sixteen-skill plus shared-runtime package, including v1/v2 step manifests, while preserving unrelated skills. QA-002: identical bounded requests yield the same TOON spec fingerprint. QA-003: missing, rejected, stale, or mismatched Implement approval denies eligibility without repository change. QA-004: passing explicit checks produce redacted TOON evidence; failures block readiness. QA-005: commit authority is separately fingerprint-bound and invalid states preserve HEAD/index. QA-006: TOON promotion round-trips supported fields and rejects incompatible input atomically. QA-007: the public repository, tag/commit identity, submodule pin, and parent validations agree. QA-008: Loop-owned durable machine artifacts never use JSON encoding or `.json` paths. QA-009: every delivery-control helper imports and every prepare step resolves through the packaged shared selector without the omitted Harness catalog. QA-010: QA planning produces canonical TOON with typed acceptance, regression, validation, manual, risk, and signoff fields and rejects unsafe output. QA-011: requirements review fails closed on severe findings or missing coverage. QA-012: release readiness fails closed on incomplete commit-bound gates or blockers. QA-013: all installed directories and declared IDs use the `ai-sdlc-loop-{slug}` namespace and the router resolves as `ai-sdlc-loop-orchestrate`. QA-014: Loop documentation builds strictly, keeps the six-section route, and derives public install/inventory claims from source-backed tests.

## Regression Targets
Harness navigation/order, product-family wording, canonical docs ownership, generated catalogs, existing install profiles, unrelated dirty work, Git index/HEAD, public paths, and documentation build/render contracts. Loop regression targets include deterministic artifacts, one-skill inventory, path containment, approval replay protection, evidence redaction, and parser/help consistency.

## Risk Notes
High: an authorization or path-containment bypass could mutate or commit unintended work. High: stale approval reuse could violate reviewer intent. Medium: cross-platform subprocess/path variance. Medium: promoted artifact drift from Harness expectations. Medium: public repo/submodule identity mismatch. Low: product-family documentation regression. All high-risk paths need executable negative tests before release.

## Validation Commands
Loop: `python3 -m unittest discover -s tests -v`; `python3 -m compileall install.py skills tests`; installer profile smoke; `sh -n install.sh`; `git diff --check`. Parent: refinement and SDD gates, security testing, focused submodule checks, the full AGENTS.md documentation sequence, and code review. Hosted: required Linux/macOS/Windows jobs and exact public commit/tag/submodule identity.

## Manual Checks
Inspect installed skill trees for each profile; read help and README commands side by side; execute TC-024 in a disposable repository with two real approval decisions; inspect redacted evidence; verify GitHub public visibility, license, security guidance, required CI, release tag, and parent submodule link.

## Signoff
Status: execution not yet signed off. Owner: maintainer. Impact: release cannot proceed until local Loop checks, hosted matrix, public identity, submodule identity, parent canonical validation, security review, code review, and TC-024 human approval evidence pass. Resolution: execute the listed gates in order and record their receipts before release.
