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
  at: "2026-08-03T21:58:37Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "security-review.md"
  path: "specs/019-whole-codebase-graph/security-review.md"
  workspace: "implementation"
  skill: "ai-sdlc-security-testing"
  flow_mode: "full"
  state_file: "specs/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs/019-whole-codebase-graph/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-04"
  updated_at: "2026-08-04"
  trace_ids:
    - "TC-024"
  related_artifacts:
    - "specs/019-whole-codebase-graph/branch-plan.md"
    - "specs/019-whole-codebase-graph/code-review.md"
    - "specs/019-whole-codebase-graph/decision-log.md"
    - "specs/019-whole-codebase-graph/design.md"
    - "specs/019-whole-codebase-graph/plan.md"
    - "specs/019-whole-codebase-graph/qa.md"
    - "specs/019-whole-codebase-graph/requirements.md"
    - "specs/019-whole-codebase-graph/tasks.md"
    - "specs/019-whole-codebase-graph/test-cases.md"
    - "specs/019-whole-codebase-graph/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-security-testing"
    - "security-review"
    - "approved"
    - "production-ready"
---

# security-review.md

## Trust Boundaries
- Confirmed facts: Repository source and parser wheels are untrusted inputs; direct files remain authoritative evidence. Graph output never grants instruction authority. Each selected source is confined to the repository, capped at 262,144 bytes, screened for credential-like content, and parsed in a bounded child process.
- Evidence: `safe_relative` and `read_source` reject traversal, symlinks, ignored trees, secrets, binary and oversized inputs. `extract_isolated` uses an eight-second subprocess, a minimal environment, denied Python socket access, and TOON-only output validation. Native exit, timeout, malformed output, parse error, or graph bound failure prevents completeness and routes to direct read.
- Open questions/blockers: No release blocker. OS-enforced network sandboxing is host-owned; the runtime additionally pins trusted wheels, removes proxy and credential environment, and makes no network request.

## Authn/Authz
- Confirmed facts: The feature performs local read/index/query operations only and introduces no identity, account, organization, remote service, or privileged business mutation. Retrieved repository text is always `evidence_only` and cannot authorize commands or state transitions.
- Evidence: Cache paths are repository-confined and reject symlink parents. Query and pack results preserve authority labels and the owning StepCard remains mandatory. Installer execution is explicit operator action and lifecycle flags use the shared state machine.
- Open questions/blockers: Authentication is not applicable to the offline local subsystem. Filesystem permissions and host sandbox policy remain the authorization boundary.

## Input Validation
- Confirmed facts: Paths, file count, file size, AST depth/node/fact counts, edge counts, traversal depth, query terms, result caps, TOON schemas, parser versions, hashes, and SQLite statements are bounded or validated.
- Evidence: Paths use `PurePosixPath`, root-relative resolution, regular-file checks, and symlink rejection. SQL values use parameter binding; the only dynamic table names come from a fixed internal tuple. AST facts are accepted only from the expected TOON schema and are retyped before database insertion. Tests cover traversal, unsafe inputs, malformed parsers, missing grammars, corrupt state, concurrency, graph bounds, and strict fallback.
- Open questions/blockers: No unresolved validation blocker.

## Secret Handling
- Confirmed facts: Secret-like names and credential-like source content are excluded before chunking or AST parsing. The parser subprocess no longer inherits arbitrary parent environment variables. Observations retain only allowlisted low-cardinality aggregates and never source text, queries, paths, or identifiers.
- Evidence: `SECRET_NAME`, `CREDENTIAL_CONTENT`, `read_source`, and `_parser_environment`; regression `test_tc_002_parser_environment_excludes_parent_secrets`; TC-024 exclusion and non-leakage coverage.
- Open questions/blockers: Pattern screening is defense in depth, not a universal secret detector; repository owners must still keep real credentials out of source control.

## Data Exposure
- Confirmed facts: All data remains local. The derived SQLite cache is ignored, purge is repository-confined, and portable receipts expose counts, hashes, statuses, and bounded reasons rather than indexed content. Parser stderr is truncated before surfacing.
- Evidence: No runtime downloader or remote provider exists. Offline smoke denies socket access. Direct-read fallback returns authoritative paths instead of partial graph content. Unsafe exclusions are represented by reason without content.
- Open questions/blockers: A user who can read the repository and cache directory can inspect the local SQLite file; this matches the repository filesystem trust boundary and is not a new cross-user access grant.

## Abuse Cases
- Confirmed facts: Reviewed abuse cases include traversal and symlink escape, secret ingestion, malicious repository text as instructions, parser crash/hang, malformed AST, graph explosion, trace clique amplification, stale/corrupt publication, concurrent warmers, wheel substitution, runtime download, ambiguous semantic linking, and forced low-economics packs.
- Evidence: Atomic candidate publication preserves the last valid cache. Per-file parser failures cannot crash the harness. Trace hubs and global/per-kind bounds cap amplification. Unique same-file resolution avoids fabricated calls. Verified wheel bytes are copied into a private temporary staging directory before `pip --no-index --no-deps`, closing the post-hash wheelhouse substitution window found during this review.
- Open questions/blockers: No unresolved exploitable path in the reviewed local threat model.

## Security Validation
- Confirmed facts: No critical, high, medium, or low unresolved finding remains. One medium supply-chain TOCTOU risk, one environment-secret propagation risk, and one incomplete-lock acceptance risk were found during review and fixed before sign-off.
- Evidence: The installer now installs immutable staged bytes that were actually hashed; a disposable Python 3.11 venv completed the real offline install and loaded all twelve grammars. Focused language security tests pass 9/9, including exact lock completeness, native crash containment, and environment stripping. The final validation receipt refreshes all twelve commands after these fixes before commit readiness.
- Open questions/blockers: Cross-platform wheel/ABI jobs remain protected-CI evidence. Local evidence covers CPython 3.11 on macOS arm64.
