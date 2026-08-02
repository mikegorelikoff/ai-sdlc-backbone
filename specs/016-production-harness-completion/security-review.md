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
  at: "2026-08-02T22:03:08Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "016-production-harness-completion"
  artifact: "security-review.md"
  path: "specs/016-production-harness-completion/security-review.md"
  workspace: "implementation"
  skill: "ai-sdlc-security-testing"
  flow_mode: "full"
  state_file: "specs/016-production-harness-completion/_ai_sdlc/state.toon"
  decision_log: "specs/016-production-harness-completion/decision-log.md"
  status: "validated"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-002"
    - "AC-003"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "AC-010"
    - "TC-002"
    - "TC-003"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-010"
  related_artifacts:
    - "specs/016-production-harness-completion/decision-log.md"
    - "specs/016-production-harness-completion/design.md"
    - "specs/016-production-harness-completion/index.md"
    - "specs/016-production-harness-completion/plan.md"
    - "specs/016-production-harness-completion/qa.md"
    - "specs/016-production-harness-completion/requirements.md"
    - "specs/016-production-harness-completion/tasks.md"
    - "specs/016-production-harness-completion/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-security-testing"
    - "security-review"
    - "validated"
---

# security-review.md

## Trust Boundaries
- Scheduler workers cross from caller-supplied plan, state, dispatch, and clock inputs into repository mutation. Every mutable path is confined before read or mutation, and dispatch commits bind repository-relative state, run, plan, revision, task, context, nonce, and runtime plan fingerprints.
- Effect requests cross from negotiated StepCards into workspace or HTTPS side effects. Only two registered drivers exist; the external driver rejects credentials and redirects, while the workspace driver rejects traversal and symlinks.
- Provider observations are maintainer and active-agent attestations committed with release evidence, not independent cryptographic statements by the provider. Their scope is the exact recorded provider, host, model family, scenario version, execution identity, and protocol fingerprint.
- Installer inputs cross from a clean immutable Git checkout into one project-scoped host root. Static profiles, digest verification, locks, symlink rejection, staging, and rollback bound this transition.

## Authn/Authz
- The harness does not authenticate people or providers. The surrounding host supplies identity and authorization; a TOON field never grants authority by itself.
- External and destructive effects require a non-empty approval reference after compatible negotiation. The adapter ID, operation, capabilities, side-effect class, StepCard, and context fingerprints must match exactly before execution.
- Scheduler completion requires the current repository-bound dispatch, expected revision, worker identity, lease nonce, unexpired lease, terminal runtime state, and matching plan fingerprints.
- Install replacement remains opt-in after review; neither profile grants global-scope installation.

## Input Validation
- TOON request objects use exact field sets, versioned schemas, bounded enums, SHA-256 formats, complete scenario identity, and non-coercing integer checks.
- Effect URLs require credential-free HTTPS, an exact hostname allowlist, a 1–30 second timeout, no fragment, and no redirect following. Workspace paths must be relative, contained, non-symlinked, and satisfy the prior-content precondition.
- Provider receipts reject duplicate or missing scenarios, contradictory status and score, stale protocol or scenario versions, invalid execution IDs, and timestamps without an offset.
- Install profiles are selected from a closed registry; revisions, inventory names, source cleanliness, targets, file types, and installed digests are validated before acceptance.

## Secret Handling
- No production credential is accepted or stored by scheduler, evaluator, or installer contracts.
- Effect arguments recursively reject keys associated with credentials, authorization, cookies, passwords, private keys, secrets, or tokens. External URLs reject embedded user information.
- Diagnostics contain bounded structural errors and response digests, not response bodies or request credentials. Provider and install receipts contain identity and evidence references only.
- Residual boundary: content placed under an innocuous key cannot be proven non-secret mechanically; operators must keep external payloads credential-free and apply repository data policy.

## Data Exposure
- External driver responses are capped at one MiB and persisted only as status and SHA-256 digest. Request payloads and receipt evidence remain canonical TOON under repository ownership.
- Context packs expose selected source ranges by design; instruction authority, token budgets, exclusions, and direct-read fallback are explicit. Teams must not run provider scenarios over restricted source unless host policy permits it.
- Install locks contain relative paths, modes, lengths, and content digests but no timestamps, absolute machine paths, or credentials.
- No cross-tenant service is implemented; hosted multi-tenant operation remains out of scope.

## Abuse Cases
- Duplicate effects return the existing request-bound receipt; a changed payload with a reused key fails. Redirect-based allowlist escape, path traversal, symlink writes, missing approval, secret-bearing keys, and foreign receipts are negative tests.
- Expired, stale, foreign, or cross-state scheduler workers cannot commit. Outside-repository state is rejected before mutation, concurrent revisions fail, and terminal runtime evidence is required.
- Offline, unattested, incomplete, duplicate, stale, or score-contradictory provider observations cannot become passing receipts.
- Dirty or mismatched sources, symbolic roots, unexpected inventory, digest drift, concurrent install mutation, partial apply failure, and unreviewed replacement fail closed.

## Security Validation
Findings:
- None open after remediation. The review found and fixed outside-repository worker mutation and external redirect allowlist escape before release.

Evidence:
- AC-002 and TC-002 cover stale-worker and recovery safety; AC-003 and TC-003 cover effect authorization and idempotency; AC-006, AC-007, TC-006, and TC-007 cover provider authenticity states; AC-008 and TC-008 cover install confinement; AC-010 and TC-010 cover security and TOON-only release gates.
- Focused scheduler worker and effect-driver security tests pass, including repository confinement, cross-state dispatch, redirect rejection, replay, approval, traversal, symlink, and secret-key cases.
- The complete per-file suite, both native installed workflows, provider verifier, compatibility, semantic graph, SDD gates, documentation validation, strict site build, and repository-wide TOON check must be current after the fixes.

Residual risk:
- Provider identity is an active-session and release-maintainer attestation, not a provider-signed cryptographic assertion.
- Local filesystem attackers racing directory components and DNS rebinding are outside the repository-local reference threat model; hostile co-tenancy requires stronger OS or network isolation.
