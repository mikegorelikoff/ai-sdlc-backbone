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
  at: "2026-08-04T13:44:58Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "021-universal-agent-installer"
  artifact: "security-review.md"
  path: "specs/021-universal-agent-installer/security-review.md"
  workspace: "implementation"
  skill: "ai-sdlc-security-testing"
  flow_mode: "quick"
  state_file: "specs/021-universal-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/021-universal-agent-installer/decision-log.md"
  status: "validated"
  owner: "Harness Maintainers"
  created_at: "2026-08-04"
  updated_at: "2026-08-05"
  trace_ids: []
  related_artifacts:
    - "specs/021-universal-agent-installer/branch-plan.md"
    - "specs/021-universal-agent-installer/decision-log.md"
    - "specs/021-universal-agent-installer/design.md"
    - "specs/021-universal-agent-installer/index.md"
    - "specs/021-universal-agent-installer/plan.md"
    - "specs/021-universal-agent-installer/qa.md"
    - "specs/021-universal-agent-installer/requirements.md"
    - "specs/021-universal-agent-installer/tasks.md"
    - "specs/021-universal-agent-installer/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-security-testing"
    - "security-review"
    - "validated"
    - "universal-installer"
---

# security-review.md

## Trust Boundaries
- Protected assets: the consumer repository, its Git metadata, installed skill bytes, and TOON provenance records.
- Externally controlled inputs are CLI arguments, environment variables, Git remotes/revisions, source checkout content, and the existing consumer filesystem.
- The native installer writes only below the resolved Git repository root. It serializes mutations through Git metadata, rejects linked managed ancestors, stages content, verifies digests, and applies with rollback.
- Source trust is bound to a clean Git HEAD and either an exact SHA or an annotated release tag. Copied skill trees reject symbolic links, non-regular files, and legacy machine artifacts.

## Authn/Authz
- The installer has no application identity or network authorization model; filesystem authority is the operating-system user running it and Git transport authentication remains external.
- Named profiles have fixed destinations. The configurable profile requires an explicit project-relative root, and replacing divergent managed content requires the separate reviewed-replacement signal.
- The public update action derives its write target and selection only from the
  existing record after its record, lock, inventory, paths, and current content
  digests agree. CLI input cannot redirect an update to another root.
- Assumption: repository membership, branch protection, and credential policy are enforced by the host project and Git provider, not by the package installer.

## Input Validation
- Profile and option relationships fail closed. Custom roots reject absolute and drive-qualified paths, empty/current/parent segments, case-insensitive `.git` or `.ai-sdlc` overlap, non-portable characters, trailing dot/space, and Windows reserved names.
- Every existing destination ancestor is checked for symlink escape before directory creation; installed records must match the normalized target and deterministic digests.
- HTTP, HTTPS, and Git remote URLs containing userinfo are rejected, whitespace/control-bearing locators are rejected, and GitHub shorthand is limited to `owner/repository`.
- Findings: none open. The review added case-insensitive protected-root checks and credential-bearing remote rejection before signoff.

## Secret Handling
- The installer accepts no token, password, private key, or bearer-token option. Git credentials must be configured through Git credential facilities outside the command and remote URL.
- Credential-bearing HTTP-family remote URLs fail before Git invocation, and automated tests assert that a secret marker is absent from stdout and stderr.
- Provenance records contain profile, target, revision, selection, paths, and digests; they do not store credentials.

## Data Exposure
- Normal output exposes the selected profile and immutable revision. Errors use bounded operational messages; the rejected credential URL is never interpolated into the diagnostic.
- Installation records are project-local governance evidence and intentionally disclose installed paths and SHA-256 digests, not file contents or identities.
- No telemetry, provider call, or external data upload is introduced.

## Abuse Cases
- Traversal or absolute target attempts are rejected before writes.
- Case-variant `.GIT` or `.AI-SDLC` overlap is rejected on case-insensitive platforms.
- A symlinked target ancestor cannot redirect writes outside the repository.
- Concurrent installer mutation fails on the repository-owned lock; divergent existing managed content requires explicit review and replacement.
- Tampered update metadata, missing installed content, or any managed digest
  drift fails before replacement; the updater does not expose a drift-bypass flag.
- A credential embedded in an HTTP-family remote cannot reach Git or diagnostic output.
- Residual risk: a separate local process with the same OS permissions can race filesystem mutations outside the installer lock; this is within the trusted local-user boundary.

## Security Validation
- Findings: none open after the two hardening changes recorded in Input Validation.
- Automated coverage: unsafe root matrix, case-variant protected roots, linked ancestors, Windows lock adapter, collision/rollback, clean immutable source, credential URL non-echo, dynamic record validation, install-to-update profile recovery, local-drift refusal, and named-profile regressions.
- Focused result: 23 native installer tests pass under Python 3.11; shell syntax validation passes.
- Release gate: GitHub Actions must pass the portable installer matrix on Ubuntu, macOS, and Windows before tag publication.
- Residual validation gap: local execution cannot reproduce native Windows filesystem and locking semantics; the remote Windows job is the release authority for that surface.
