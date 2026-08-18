---
type: "ai-sdlc.requirements"
title: "Requirements"
description: "Implementation requirements, constraints, and acceptance criteria."
tags:
  - "ai-sdlc"
  - "sdd"
  - "requirements"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-17T11:55:09Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "requirements.md"
  path: "specs/022-ai-sdlc-loop/requirements.md"
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
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
    - "NFR-008"
  related_artifacts:
    - "specs/022-ai-sdlc-loop/branch-plan.md"
    - "specs/022-ai-sdlc-loop/decision-log.md"
    - "specs/022-ai-sdlc-loop/design.md"
    - "specs/022-ai-sdlc-loop/index.md"
    - "specs/022-ai-sdlc-loop/plan.md"
    - "specs/022-ai-sdlc-loop/qa.md"
    - "specs/022-ai-sdlc-loop/security-review.md"
    - "specs/022-ai-sdlc-loop/tasks.md"
    - "specs/022-ai-sdlc-loop/test-cases.md"
    - "specs/022-ai-sdlc-loop/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "approved"
    - "ai-sdlc-loop"
---

# Requirements

## Goal
Build and release AI SDLC Loop as a minimal, independently maintained member of the AI SDLC product family that safely delivers bounded repository changes through a small composable skill set and remains compatible with promotion into AI SDLC Harness.

## Problem Statement
AI SDLC Harness exposes a broad lifecycle surface that is increasingly expensive for the maintainer to support when users need only a safe bounded coding loop. There is no independently versioned minimal repository that installs a focused stage-oriented skill set, enforces approvals before code mutation and commit, retains deterministic TOON evidence, and preserves a promotion path into Harness.

## Scope
Create public repository mikegorelikoff/ai-sdlc-loop; five stage-oriented entrypoint skills; eleven self-contained delivery-control skills for approvals, branching, requirements review, test cases, QA, validation, code review, security testing, commit preparation, Conventional Commits, and release readiness; `ai-sdlc-loop-shared-runtime`; Python standard-library CLI and cross-platform bootstrap; codex-project, claude-code-project, and agent-project --skills-root installation; Specify, approval, Implement, Verify, approval, commit lifecycle; versioned TOON contracts; tests, CI, security, contributing, license, and release documentation; Harness promotion fixture; products/ai-sdlc-loop submodule; parent product-family, decision-log, and changelog updates.

## Actors
Contributor installs Loop, provides a bounded request, reviews artifacts, and runs authorized stages. Reviewer explicitly approves or rejects the current specification fingerprint and later the verified-change fingerprint. Loop maintainer owns package, CI, documentation, security, and release. Harness maintainer owns promotion compatibility, parent documentation, and submodule pin. QA and security reviewers own acceptance, regression, abuse, and release evidence.

## Inputs
Installer inputs: profile codex-project, claude-code-project, or agent-project plus a safe project-relative --skills-root for the custom profile. Specify inputs: feature slug, bounded request text, repository root, and declared allowed paths. Approval inputs: stage action, decision approve or reject, current fingerprint, and reviewer identity supplied explicitly. Verify inputs: approved change, relevant commands explicitly supplied or approved, and repository state. Commit inputs: current passing verification fingerprint and explicit approval.

## Outputs
Installation writes the fixed seventeen-member Loop package and a local TOON install record plus reusable verifier. Requirements review writes typed gaps and coverage as canonical TOON. Specify writes `.ai-sdlc-loop/<feature>/spec.toon` and `state.toon` with schema version, bounded request, allowed paths, trace IDs, status, and SHA-256 fingerprint. Approval writes action-scoped TOON receipts. QA writes a canonical TOON plan with typed acceptance, regression, evidence, manual-check, risk, and signoff fields. Verify writes `evidence.toon` with commands, exits, bounded redacted output, change fingerprint, and readiness. Commit creates exactly one approved Git commit. Release readiness binds gates, blockers, risks, and status to an exact commit in canonical TOON. Promotion emits a Harness-compatible TOON artifact without supported-field loss.

## Functional Requirements
FR-001: install exactly `ai-sdlc-loop-orchestrate`, the four stage owners, eleven delivery-control owners, and `ai-sdlc-loop-shared-runtime` into the selected project skills root. FR-002: verify package digests, profile, target, and exact Loop-owned skill inventory without network while preserving unrelated skills. FR-003: Specify must normalize a bounded request, validate the feature and allowed paths, persist versioned TOON, and compute a deterministic fingerprint before mutation. FR-004: Implement eligibility requires an explicit approve receipt matching the current spec fingerprint; reject, missing, stale, or mismatched receipts deny mutation. FR-005: implementation changes must stay within allowed paths and preserve unrelated tracked, staged, unstaged, and untracked work. FR-006: Verify must execute only explicitly supplied commands, record deterministic redacted TOON evidence, and set readiness false on any nonzero, missing, interrupted, or timed-out command. FR-007: commit requires passing current evidence and an explicit approve receipt matching its fingerprint; invalid authority leaves index and HEAD unchanged. FR-008: promote must validate the Loop TOON schema, preserve supported fields and trace IDs, and reject incompatible input without partial output. FR-009: repository must be public, Apache-2.0, tested in CI, and pin-able as products/ai-sdlc-loop in Harness. FR-010: every working skill must route through a canonical `steps/manifest.toon` and bounded step documents; orchestration must not collapse stage ownership into one monolithic instruction. FR-011: stage entrypoints must route relevant work to the eleven delivery-control owners without requiring the rest of the Harness discovery/refinement catalog. FR-012: QA must produce a canonical TOON plan with structured acceptance scenarios, regression targets, validation evidence, manual checks, residual risk, and explicit signoff without depending on the Harness refinement cascade. FR-013: requirements review must emit evidence-backed typed gaps and reject `ready` while critical/high findings or missing coverage remain. FR-014: release readiness must bind every gate to one exact commit and reject `ready` while any gate is incomplete or any blocker remains. FR-015: every installed skill directory, frontmatter name, manifest skill ID, runtime reference, and public example must use `ai-sdlc-loop-{slug}`; the root router slug is `orchestrate`. FR-016: publish a strict-build MkDocs site with Home, Start here, How it works, Guides, Reference, and Project navigation, source-backed commands and skill inventory, product-family context, and automated GitHub Pages deployment.

## Non-Functional Requirements
NFR-001 deterministic normalized TOON, ordering, and SHA-256 fingerprints. NFR-002 path containment rejects absolute roots, traversal, and symlink escape. NFR-003 denied or failed operations preserve unrelated filesystem and Git state. NFR-004 evidence redacts token, password, secret, and private-key-like values. NFR-005 runtime uses Python 3 standard library and requires no telemetry, hosted service, or runtime network. NFR-006 installer supports POSIX shell and native Python invocation, with hosted Linux, macOS, and Windows validation. NFR-007 errors are actionable and never imply approval. NFR-008 public documentation commands are parser- and fixture-verified. NFR-009 JSON must not be used for Loop-owned durable machine artifacts.

## Constraints
Sixteen visible skills and one internal shared runtime; no copied full Harness discovery/refinement catalog or dependency cascade. All current profile names must remain source-backed. Repository-local TOON state is authoritative. Install targets must stay inside the project. Code mutation and command execution occur only within user-authorized scope; commit is never implicit. Public repository creation and push are external operations. Parent navigation, canonical documentation contracts, product-family wording, generated catalogs, and existing paths must remain stable.

## Acceptance Criteria
The implementation must satisfy every observable criterion below.

AC-001: each advertised profile installs and verifies the exact seventeen-member Loop package, including manifests and step documents, while preserving unrelated skills; unsafe, conflicting, interrupted, or drifted states fail without unrelated changes. AC-002: Specify on the same normalized request yields a schema-valid identical TOON fingerprint, while semantic drift changes it before mutation. AC-003: Implement is denied for missing, rejected, stale, or mismatched approval with an unchanged repository, and eligible only for a matching approval receipt. AC-004: approved implementation changes only allowed paths; Verify records commands and deterministic redacted TOON evidence, and any failed check blocks readiness. AC-005: commit is denied for missing, rejected, stale, mismatched, or drifted verification approval with unchanged index and HEAD; matching passing approval creates exactly one traceable commit. AC-006: valid Loop TOON artifacts promote with supported-field equality; incompatible artifacts create no partial output. AC-007: public repository CI, documentation, license, release identity, and Harness submodule pin resolve to the validated commit. AC-008: no Loop-owned state, approval, evidence, install record, or promotion file uses a `.json` extension or JSON encoding. AC-009: every added delivery-control helper loads, every manifest parses, and the shared selector resolves each skill's prepare step without the absent Harness catalog. AC-010: QA emits deterministic schema-valid TOON with complete typed acceptance scenarios, rejects unsafe or non-TOON output paths, and cannot mark planned evidence as executed signoff. AC-011: requirements review deterministically emits typed TOON gaps and fails readiness when severe or missing coverage remains. AC-012: release readiness deterministically emits commit-bound TOON gates and fails readiness for incomplete gates or blockers. AC-013: installation exposes exactly seventeen `ai-sdlc-loop-{slug}` directories, each `SKILL.md` and manifest ID equals its directory name, and no packaged instruction or runtime path references a superseded Loop skill ID. AC-014: MkDocs builds with `--strict`, preserves the six-section navigation order, documents all 17 source skills, keeps the primary install command aligned across README, Home, and Start here, and runs build/deploy workflows from source.

## Out of Scope
The full AI SDLC Harness catalog and 18-stage runtime; multiple public skills; hosted orchestration; deployment; telemetry or analytics; model-quality guarantees; UI; notifications; performance/load claims; organizational policy engines; automatic approval; automatic commit without explicit approval; a promise to reduce model calls; changes to unrelated Harness installers or public documentation paths.

## Assumptions
Python 3 and Git are available for workflow and verification operations. The installer bootstrap may fetch a pinned repository revision, but the installed skill runs locally without network. A human or host supplies explicit approval decisions; Loop validates receipts but does not authenticate organizational identity. Relevant validation commands are provided by the user or repository context and still require host command approval. The first corrected public package release is `v0.1.1`.

## Open Questions
None that block implementation. Binding items: schema identifier ai-sdlc-loop/v1, CLI command names, CI job names, and first release tag are implementation constants governed by AC-002, AC-006, and AC-007. Owner: Loop maintainer. Impact: fixtures and documentation. Resolution: define in design, test against public help and schemas, and update the spec before code if a material contract changes.

## Decision Status
All blocking decisions are resolved. Accepted assumptions and refinement decisions: DEC-001 public AI SDLC Loop repository and products/ai-sdlc-loop submodule; DEC-002 one ai-sdlc skill with Specify, Implement, Verify; DEC-003 all current profiles and one-command install; DEC-004 approval before code mutation and before commit; DEC-005 Harness-compatible artifacts, Apache-2.0, local authority, and escalation path. Implementation DEC-001 selects feature/022-ai-sdlc-loop from refreshed main. No decision is pending.
