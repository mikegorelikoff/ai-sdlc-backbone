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
  at: "2026-09-01T09:51:53Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "requirements.md"
  path: "specs/022-ai-sdlc-loop/requirements.md"
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
    - "DEC-001"
    - "DEC-007"
    - "DEC-008"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
    - "NFR-008"
    - "NFR-009"
    - "NFR-010"
    - "NFR-011"
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
    - "engineering-quality-gate"
    - "ai-sdlc-loop"
---

# Requirements

## Goal
Build and release AI SDLC Loop as a minimal, independently maintained member of the AI SDLC product family that safely delivers bounded repository changes through a small composable skill set and remains compatible with promotion into AI SDLC Harness.

## Problem Statement
AI SDLC Harness exposes a broad lifecycle surface that is increasingly expensive for the maintainer to support when users need only a safe bounded coding loop. There is no independently versioned minimal repository that installs a focused stage-oriented skill set, enforces approvals before code mutation and commit, retains deterministic TOON evidence, and preserves a promotion path into Harness.

## Scope
Create and maintain public repository mikegorelikoff/ai-sdlc-loop; six stage-oriented entrypoint skills (router plus Specify, Implement, Engineering Quality Gate, Verify, and Commit); eleven self-contained delivery-control skills; `ai-sdlc-loop-shared-runtime`; Python standard-library CLI and cross-platform bootstrap; codex-project, claude-code-project, and agent-project installation; Specify → approval → Implement → Engineering Quality Gate → Verify → approval → Commit lifecycle; versioned TOON contracts; tests, CI, security, contributing, license, and release documentation; Harness promotion fixture; `products/ai-sdlc-loop` submodule; and a canonical `ai-sdlc-engineering-quality-gate` skill registered in the Harness `core` module. The engineering gate must inspect the current diff and bounded repository context, compare 2–5 representative implementations where practical, review adversarially, run deterministic checks, safely fix material findings, rerun checks, and emit current evidence.

## Actors
Contributor installs Loop, provides a bounded request, reviews artifacts, and runs authorized stages. Reviewer explicitly approves or rejects the current specification fingerprint and later the verified-change fingerprint. Loop maintainer owns package, CI, documentation, security, and release. Harness maintainer owns promotion compatibility, parent documentation, and submodule pin. QA and security reviewers own acceptance, regression, abuse, and release evidence.

## Inputs
Installer inputs: profile `codex-project`, `claude-code-project`, or `agent-project` plus a safe project-relative `--skills-root` for the custom profile. Specify inputs: feature slug, bounded request text, repository root, and declared allowed paths. Approval inputs: stage action, decision, current fingerprint, and reviewer identity supplied explicitly. Engineering Quality Gate inputs: requested change or accepted specification, current implementation diff or explicit review target, repository root, optional base revision, and available repository verification contracts. Verify inputs: approved change, a current ready quality-gate report bound to the same change fingerprint, relevant commands explicitly supplied or approved, and repository state. Commit inputs: current passing verification fingerprint and explicit approval.

## Outputs
Installation writes the fixed twenty-member Loop package and a local TOON install record plus reusable verifier. The Harness core installer includes `ai-sdlc-engineering-quality-gate`. Requirements review and other focused owners retain their canonical TOON outputs. Engineering Quality Gate writes a bounded deterministic context profile and canonical `ai-sdlc-engineering-quality-gate/v1` report containing repository examples and patterns, fixed and remaining typed findings, verification statuses, change-scope metrics, quality evidence, a current change fingerprint, and an explicit readiness decision; it also presents the concise human report requested by the caller. Verify writes `evidence.toon` only after a current ready quality report exists. Commit, release readiness, and promotion retain their existing contracts.

## Functional Requirements
FR-001: install exactly `ai-sdlc-loop-orchestrate`, five stage owners, eleven delivery-control owners, and `ai-sdlc-loop-shared-runtime` into the selected project skills root.
FR-002: verify package digests, profile, target, and exact Loop-owned skill inventory without network while preserving unrelated skills.
FR-003: Specify must normalize a bounded request, validate the feature and allowed paths, persist versioned TOON, and compute a deterministic fingerprint before mutation.
FR-004: Implement eligibility requires an explicit approve receipt matching the current spec fingerprint; reject, missing, stale, or mismatched receipts deny mutation.
FR-005: implementation and quality-gate fixes must stay within allowed paths and preserve unrelated tracked, staged, unstaged, and untracked work.
FR-006: Verify must require a current ready quality-gate report for the same change fingerprint, execute only explicitly supplied commands, record deterministic redacted TOON evidence, and set readiness false on any nonzero, missing, interrupted, or timed-out command.
FR-007: commit requires passing current evidence and an explicit approve receipt matching its fingerprint; invalid authority leaves index and HEAD unchanged.
FR-008: promote must validate the Loop TOON schema, preserve supported fields and trace IDs, include quality-gate evidence when present, and reject incompatible input without partial output.
FR-009: repository must be public, Apache-2.0, tested in CI, and pin-able as `products/ai-sdlc-loop` in Harness.
FR-010: every working skill must route through a canonical `steps/manifest.toon` and bounded step documents; orchestration must not collapse stage ownership into one monolithic instruction.
FR-011: the routed lifecycle must place `ai-sdlc-loop-engineering-quality-gate` after Implement and before Verify, while remaining independently callable after any implementation step.
FR-012: QA must produce a canonical TOON plan with structured acceptance scenarios, regression targets, validation evidence, manual checks, residual risk, and explicit signoff.
FR-013: requirements review must emit evidence-backed typed gaps and reject `ready` while critical/high findings or missing coverage remain.
FR-014: release readiness must bind every gate to one exact commit and reject `ready` while any gate is incomplete or any blocker remains.
FR-015: every installed skill directory, frontmatter name, manifest skill ID, runtime reference, and public example must use `ai-sdlc-loop-{slug}`; the root router slug is `orchestrate`.
FR-016: publish a strict-build MkDocs site with the required six-section navigation, source-backed commands and skill inventory, product-family context, and automated GitHub Pages deployment.
FR-017: Engineering Quality Gate must understand the request and diff, build the smallest relevant repository profile, and identify 2–5 representative implementations where practical; fewer examples require explicit evidence that practical candidates were unavailable.
FR-018: it must inspect repository contracts, tests, architecture boundaries, validation, error handling, naming, security/reliability concerns, anti-AI code smells, and diff budget; create typed High/Medium/Low findings before mutation; and fix High plus safe localized Medium findings without broad refactors or unrelated cleanup.
FR-019: it must detect repository-owned build, typecheck, lint, test, and static-analysis commands, run the smallest relevant set first, record `pass`, `fail`, `not_run`, or `unavailable`, rerun relevant checks after fixes, and never claim unexecuted success.
FR-020: it must finalize a structured evidence-based report whose readiness rules forbid PASS with unresolved High, blocking Medium, failed required verification, or a stale change fingerprint; the canonical Harness skill must be registered in `modules/core/module.toon` and default managed inventory.

## Non-Functional Requirements
NFR-001 deterministic normalized TOON, ordering, and SHA-256 fingerprints.
NFR-002 path containment rejects absolute roots, traversal, and symlink escape.
NFR-003 denied or failed operations preserve unrelated filesystem and Git state.
NFR-004 evidence redacts token, password, secret, and private-key-like values.
NFR-005 runtime uses Python 3 standard library and requires no telemetry, hosted service, or runtime network.
NFR-006 installer supports POSIX shell and native Python invocation, with hosted Linux, macOS, and Windows validation.
NFR-007 errors are actionable and never imply approval.
NFR-008 public documentation commands are parser- and fixture-verified.
NFR-009 Non-TOON object notation must not be used for Loop-owned durable machine artifacts.
NFR-010 quality-gate context, candidate ranking, paths, commands, findings, report encoding, and fingerprints use documented stable ordering and tie-breakers; volatile timestamps and durations are excluded from signed readiness identity.
NFR-011 discovery is diff-bounded by default, avoids unnecessary full-repository scans, adds no dependency casually, does not weaken configuration, and preserves unrelated work byte-for-byte.

## Constraints
Seventeen visible Loop skills and one internal shared runtime; one namespaced Harness counterpart in the `core` module; no copied full Harness discovery/refinement catalog or dependency cascade. All current profile names must remain source-backed. Repository-local TOON state is authoritative. Install targets stay inside the project. Code mutation and command execution occur only within user-authorized scope; quality fixes are limited to evidence-backed High and safe localized Medium findings; commit is never implicit. Public repository push remains external. Parent navigation, canonical documentation contracts, product-family wording, generated catalogs, and existing paths remain stable.

## Acceptance Criteria
The implementation must satisfy every observable criterion below.

AC-001: each advertised profile installs and verifies the exact twenty-member Loop package, including manifests and step documents, while preserving unrelated skills; unsafe, conflicting, interrupted, or drifted states fail without unrelated changes.
AC-002: Specify on the same normalized request yields a schema-valid identical TOON fingerprint, while semantic drift changes it before mutation.
AC-003: Implement is denied for missing, rejected, stale, or mismatched approval with an unchanged repository, and eligible only for a matching approval receipt.
AC-004: approved implementation changes only allowed paths; Verify records commands and deterministic redacted TOON evidence, and any failed check blocks readiness.
AC-005: commit is denied for missing, rejected, stale, mismatched, or drifted verification approval with unchanged index and HEAD; matching passing approval creates exactly one traceable commit.
AC-006: valid Loop TOON artifacts promote with supported-field equality; incompatible artifacts create no partial output.
AC-007: public repository CI, documentation, license, release identity, and Harness submodule pin resolve to the validated commit.
AC-008: every Loop-owned durable machine artifact uses a `.toon` extension and canonical TOON encoding.
AC-009: every delivery-control helper loads, every manifest parses, and the shared selector resolves each skill's prepare step without the absent Harness catalog.
AC-010: QA emits deterministic schema-valid TOON with complete typed acceptance scenarios and rejects unsafe output.
AC-011: requirements review deterministically emits typed TOON gaps and fails readiness when severe or missing coverage remains.
AC-012: release readiness deterministically emits commit-bound TOON gates and fails readiness for incomplete gates or blockers.
AC-013: installation exposes exactly twenty `ai-sdlc-loop-{slug}` directories, each `SKILL.md` and manifest ID equals its directory name, and no packaged instruction or runtime path references a superseded Loop skill ID.
AC-014: MkDocs builds with `--strict`, preserves the six-section navigation order, documents every source skill, and keeps the primary install command aligned across README, Home, and Start here.
AC-015: both namespaced engineering-quality-gate skills are discoverable and selectable through their existing loaders; Loop installs the gate in every profile and routes Implement → Engineering Quality Gate → Verify, while direct invocation remains supported.
AC-016: unchanged fixtures produce byte-identical bounded context profiles and quality reports with stable fingerprints, ordered 2–5 representative examples when available, repository-supported patterns, and deterministic status fields; diff drift invalidates readiness.
AC-017: the gate records schema-valid findings with severity, category, location, evidence, impact, and concrete fix; fixes only High and safe localized Medium findings; preserves remaining Low or clarification-blocked items and unrelated work.
AC-018: available repository checks run in a justified deterministic order before and after fixes; every check is `pass`, `fail`, `not_run`, or `unavailable`; failed required checks or unresolved blocking findings make status non-PASS and readiness false.
AC-019: canonical TOON schema/templates, three realistic usage examples, an example final report, skill-level tests, Harness core registration, managed inventory, generated catalogs, Loop docs/inventory, and repository validation all agree with source.

## Out of Scope
The full AI SDLC Harness catalog inside Loop; hosted orchestration; deployment; telemetry or analytics; model-quality guarantees; UI; notifications; performance/load claims; organizational policy engines; automatic approval; automatic commit without explicit approval; a promise to reduce model calls; broad architecture redesign; opportunistic cleanup; changes to unrelated public documentation paths.

## Assumptions
Python 3 and Git are available for workflow and verification operations. The installer bootstrap may fetch a pinned repository revision, but the installed skill runs locally without network. A human or host supplies explicit approval decisions; Loop validates receipts but does not authenticate organizational identity. Relevant validation commands are provided by the user or repository context and still require host command approval. The first corrected public package release is `v0.1.1`.

## Open Questions
None that block implementation. Binding items: schema identifier ai-sdlc-loop/v1, CLI command names, CI job names, and first release tag are implementation constants governed by AC-002, AC-006, and AC-007. Owner: Loop maintainer. Impact: fixtures and documentation. Resolution: define in design, test against public help and schemas, and update the spec before code if a material contract changes.

## Decision Status
All blocking decisions are resolved. Accepted assumptions and refinement decisions remain DEC-001 through DEC-007. DEC-008 adds the mandatory deterministic engineering quality gate, uses repository-required names `ai-sdlc-engineering-quality-gate` and `ai-sdlc-loop-engineering-quality-gate`, places the Harness skill in `core`, places the Loop adaptation in every fixed install profile, and routes the Loop stage after Implement and before Verify. No decision is pending.
