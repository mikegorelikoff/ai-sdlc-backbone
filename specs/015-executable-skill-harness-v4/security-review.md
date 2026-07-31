---
type: "ai-sdlc.security-review"
title: "Security Review"
description: "Security threats, controls, findings, and validation evidence."
tags:
  - "ai-sdlc"
  - "security"
  - "review"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-30T10:53:44Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "015-executable-skill-harness-v4"
  artifact: "security-review.md"
  path: "specs/015-executable-skill-harness-v4/security-review.md"
  workspace: "implementation"
  skill: "ai-sdlc-security-testing"
  flow_mode: "full"
  state_file: "specs/015-executable-skill-harness-v4/_ai_sdlc/state.toon"
  decision_log: "specs/015-executable-skill-harness-v4/decision-log.md"
  status: "approved"
  owner: "software-engineering"
  created_at: "2026-07-30"
  updated_at: "2026-07-30"
  trace_ids:
    - "AC-001"
    - "AC-003"
    - "AC-005"
    - "AC-008"
    - "AC-009"
    - "AC-013"
    - "NFR-007"
    - "NFR-008"
    - "TC-001"
    - "TC-003"
    - "TC-005"
    - "TC-008"
    - "TC-009"
    - "TC-012"
    - "TC-013"
    - "DEC-009"
  related_artifacts:
    - "specs/015-executable-skill-harness-v4/branch-plan.md"
    - "specs/015-executable-skill-harness-v4/code-review.md"
    - "specs/015-executable-skill-harness-v4/decision-log.md"
    - "specs/015-executable-skill-harness-v4/design.md"
    - "specs/015-executable-skill-harness-v4/index.md"
    - "specs/015-executable-skill-harness-v4/plan.md"
    - "specs/015-executable-skill-harness-v4/qa.md"
    - "specs/015-executable-skill-harness-v4/requirements.md"
    - "specs/015-executable-skill-harness-v4/research.md"
    - "specs/015-executable-skill-harness-v4/tasks.md"
    - "specs/015-executable-skill-harness-v4/test-cases.md"
    - "specs/015-executable-skill-harness-v4/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-security-testing"
    - "security-review"
    - "approved"
    - "harness-v4"
---

# security-review.md

## Trust Boundaries
- Confirmed facts: Repository files, skill manifests, plans, context sources, journal events, and host capability reports are treated as potentially untrusted inputs. The principal transitions are path-to-filesystem writes, Explore-to-Apply authorization, plan-to-runtime execution, runtime-to-host effects, and local evidence-to-provider or release claims. Repository-bounded writers reject traversal and symlink targets; Explore remains zero-write; Apply binds reviewed plan, step, context, attempt, and idempotency fingerprints; runtime persists terminal evidence and effect receipts before projecting results.
- Evidence: `ai_sdlc_safe_io.py`; `ai_sdlc_step_context.py`; `ai_sdlc_flow.py`; `skills/ai-sdlc-runtime/scripts/runtime.py`; AC-003 through AC-008; TC-003 through TC-008; focused path-escape, stale-plan, tamper, replay, and interrupted-completion tests.
- Open questions/blockers: No unresolved repository implementation blocker. Provider execution and remote publication cross external trust boundaries and remain separately evidenced release operations.

## Authn/Authz
- Confirmed facts: The repository harness is a local CLI and does not implement end-user authentication. Identity and permission enforcement stay with the operating system, sandbox, source-control host, and negotiated host adapter. Mutating flow requires explicit Apply execution after fingerprint revalidation; unsupported operations or missing host capabilities fail closed. Runtime task identity, attempt, idempotency key, and operation must match the reviewed plan and journal state.
- Evidence: `skills/ai-sdlc-flow/scripts/flow.py`; `skills/ai-sdlc-host-adapter/scripts/adapter.py`; `skills/ai-sdlc-runtime/scripts/runtime.py`; AC-005 through AC-009; TC-005 through TC-009.
- Open questions/blockers: Product authentication and repository-host access policy are outside this package. Publication uses the authenticated source-control client as a separate release boundary; no unresolved in-repository authorization defect remains.

## Input Validation
- Confirmed facts: Structured inputs use versioned canonical TOON contracts with exact required fields, bounded identifiers, deterministic ordering, and fail-closed diagnostics. Repository paths are normalized and contained; symlinked inputs and write targets are rejected where authority could cross a boundary. Runtime replay validates event type, sequence, payload shape, task identity, attempt, operation, and idempotency key. The validation runner accepts reviewed argv arrays only, rejects shell execution and executable paths, bounds output, and restricts command families.
- Evidence: `ai_sdlc_toon.py`; `ai_sdlc_safe_io.py`; `ai_sdlc_steps.py`; `skills/ai-sdlc-runtime/scripts/runtime.py`; `skills/ai-sdlc-validation/scripts/run_validation.py`; `test_v4_contracts.py`; `test_runtime.py`; `test_run_validation.py`.
- Open questions/blockers: Reviewed repository test programs remain trusted code and may perform their own actions; the validation runner is an evidence boundary, not a sandbox for hostile source code. This scope is explicit and not a release blocker.

## Secret Handling
- Confirmed facts: Context discovery excludes secret-named paths, symlinks, and credential-shaped content before excerpts enter context packs. External specification snapshots apply the same credential-content rejection and bounded-source rules. Validation receipts retain output digests and byte counts rather than command output. No credential is required or persisted by runtime, flow, workflow, adapter, evaluation, or test-suite contracts.
- Evidence: `skills/ai-sdlc-project-context/scripts/project_context.py`; `context_engine.py`; `external_spec_snapshot.py`; their credential and symlink regressions; `run_validation.py`; AC-003; AC-013; NFR-008.
- Open questions/blockers: Operators must still keep credentials out of ordinary source files and must review any program selected in a validation plan. Host and source-control credentials remain managed by their native clients and are not copied into release artifacts.

## Data Exposure
- Confirmed facts: The harness performs no implicit network upload. Context excerpts, journals, state, evidence receipts, and local environment summaries are repository-local unless an operator deliberately commits or transmits them. Context and snapshot builders reject credential-like material; validation receipts store hashes instead of captured output; tagged publication contains only explicitly committed files.
- Evidence: Context-engine and snapshot implementations and tests; `ai_sdlc_validation_receipt.py`; `run_validation.py`; package and installation validation; release inventory checks.
- Open questions/blockers: Local evidence may contain repository paths, platform details, task descriptions, or non-secret source excerpts. Teams must classify repositories and provider prompts according to their own data policy before external execution. This is a documented operational responsibility, not an undisclosed transfer.

## Abuse Cases
- Confirmed facts: The review exercised traversal and symlink overwrite attempts, stale or modified Apply cards, journal truncation and tampering, duplicate sequence creation, repeated side effects with changed evidence, interruption between terminal evidence and result projection, retry after exhausted failure budget, unsupported host capabilities, arbitrary validation command forms, credential-shaped context sources, and forged or stale local receipts. Controls fail closed or preserve an explicit unauthenticated-local-evidence disclosure.
- Evidence: `test_safe_io.py`; `test_step_context_v4.py`; `test_flow.py`; `test_runtime.py`; `test_adapter.py`; `test_run_validation.py`; `test_skill_eval.py`; code-review resolutions tied to AC-003 through AC-013.
- Open questions/blockers: Filesystem journals are not authenticated distributed ledgers and cannot make an external side effect transactional. Hosts must honor idempotency keys and return durable effect receipts; provider certification must preserve execution identity and recovery evidence.

## Security Validation
- Confirmed facts: Independent review corrected completion-identity drift, interrupted terminal recovery, pre-lock replay, replaceable journal sequences, failure-budget retry bypass, under-validated event payloads, evaluation-output path escape, and the non-conforming external consumer-install boundary. The native installer allows only a clean exact Git revision and project-scoped Codex target; rejects source, destination, and metadata links; rejects alternate machine artifacts and unknown inventory entries; compares staged and installed tree digests; refuses unreviewed replacement; serializes mutations through Git metadata; and restores the accepted tree after caught apply failures. The full 17-command plan, receipt freshness check, 10 native-installer cases, native 44-skill consumer workflow, strict documentation build, rendered-link validation, compatibility audit, canonicality scan, and diff hygiene pass.
- Evidence: `ai_sdlc_install.py`; `ai_sdlc_install_record.py`; `install.sh`; `test_native_install.py`; `install_smoke.py`; `specs/015-executable-skill-harness-v4/code-review.md`; AC-001 through AC-013; NFR-007; TC-001 through TC-013; DEC-009; the canonical validation plan and current receipt.
- Open questions/blockers: No unresolved security implementation finding. Provider-executed TC-012 and remote publication evidence cannot be fabricated locally and remain disclosed release-owner evidence; local fingerprints detect drift but do not provide cryptographic signer identity. No external security-standard conformance claim is made by this review.

## Native Installer Residual Boundary
- Confirmed facts: The bootstrap fetches a sanitized exact tag or lowercase commit, requires an annotated release tag when a name is used, and persists no source-control credential or absolute source path. Local source overrides remain an explicit trust decision. Existing differing managed content requires the reviewed replacement flag; unrelated skills are not changed.
- Evidence: Shell syntax check; clean-source and revision checks; missing-local-path, dirty-source, link, alternate-artifact, existing-difference, concurrency, rollback, and installed-digest regressions; install and update guides.
- Open questions/blockers: Annotated does not mean cryptographically signed. Remote identity, transport credentials, signature policy, and source-host authorization remain adopter controls. Abrupt process or machine termination can bypass caught-failure rollback, so the consumer Git baseline and exact-revision recovery procedure remain required.
