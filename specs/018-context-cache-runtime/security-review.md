---
type: "ai-sdlc.security-review"
title: "Security Review"
description: "Full-flow security review of automatic local context-cache runtime integration."
tags:
  - "ai-sdlc"
  - "security"
  - "context-cache-runtime"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "security-review.md"
  path: "specs/018-context-cache-runtime/security-review.md"
  workspace: "implementation"
  skill: "ai-sdlc-security-testing"
  flow_mode: "full"
  state_file: "specs/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs/018-context-cache-runtime/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers and Security"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "TC-003"
    - "TC-004"
    - "TC-006"
    - "TC-007"
    - "TC-009"
    - "TC-011"
  related_artifacts:
    - "specs/018-context-cache-runtime/requirements.md"
    - "specs/018-context-cache-runtime/design.md"
    - "specs/018-context-cache-runtime/code-review.md"
    - "specs/018-context-cache-runtime/validation.md"
  validation:
    - "path and symlink negative tests passed"
    - "aggregate observation privacy test passed"
    - "source-drift and corrupt-state recovery tests passed"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-security-testing"
    - "security-review"
    - "approved"
---

# Security Review

## Trust Boundaries

- Confirmed facts: Repository sources and owning StepCards remain authoritative;
  cache rows are derived evidence only. Project-installed module paths, policy,
  cache files, control files, subprocess output, and SQLite contents are treated
  as untrusted until structurally and semantically validated.
- Evidence: Installed module and policy paths reject symlink components and path
  escape. Cache and control paths remain below the repository root and reject
  linked roots or parents. A returned pack must pass context-pack/v4 owner,
  anchor, freshness, ordering, authority, budget, and sufficiency validation.
- Open questions/blockers: None.

## Authn/Authz

- Confirmed facts: This is a single-repository, local-process feature with no
  remote identity, tenant, account, service, webhook, or authorization API.
  Filesystem access is inherited from the invoking user and is not broadened.
- Evidence: Automatic activation requires a complete project-local install in
  an allowlisted skills root. Source checkout presence alone does not activate
  the adapter.
- Open questions/blockers: None. Multi-user cache isolation and remote service
  authorization are outside the accepted local-only scope.

## Input Validation

- Confirmed facts: Policy accepts only the declared schema, exact field sets,
  typed values, bounded numeric ranges, and exact skill/step overrides. Manifest
  budget and savings requirements cannot be weakened. CLI paths are confined,
  query output is decoded as TOON, and pack acceptance uses the v4 validator.
- Evidence: Negative tests cover unknown policy fields, bounds, path escape,
  symlink parents, unsafe sources, missing cache, corrupt state, source drift,
  and stale or uneconomical packs.
- Open questions/blockers: None.

## Secret Handling

- Confirmed facts: No credential, token, network secret, or provider key is
  introduced. Source discovery excludes secret-shaped paths and content using
  the existing heuristic boundary. Observations accept only allowlisted enums,
  normalized bounded reasons, counts, and token totals.
- Evidence: Tests prove observations contain no query, prompt, content,
  credential, or identity field. Subprocess stderr is suppressed at the adapter
  boundary and cache errors are bounded.
- Open questions/blockers: Heuristic source exclusion does not replace repository
  secret scanning; this is a documented residual risk, not a release blocker.

## Data Exposure

- Confirmed facts: Cache and control databases remain local derived state. The
  adapter performs no network operation, loads no SQLite extension, and emits
  machine-facing output as TOON. Cached repository instructions are explicitly
  classified as evidence-only and cannot gain instruction authority.
- Evidence: Static inspection found no network client or extension-loading path.
  Authority and observation privacy tests pass. Purge is confined to the chosen
  derived database and does not remove sources.
- Open questions/blockers: Local readers already authorized for the repository
  may read its derived cache. Encryption at rest is not claimed.

## Abuse Cases

| Abuse or failure attempt | Required control | Evidence and outcome |
| --- | --- | --- |
| Install the cache through a linked parent | Reject activation | Linked installation parent test passes. |
| Redirect cache, control, or policy through a symlink | Reject before read or write | Linked cache root, cache parent, and policy parent controls fail closed. |
| Widen token budget or lower savings through policy | Clamp to manifest | Exact policy and clamp tests pass. |
| Inject instruction-shaped text through indexed files | Preserve evidence-only authority | Root and nested instruction filename tests plus v4 validation pass. |
| Race multiple warmers or mutate sources during build | Serialize and reject stale publication | Four-process convergence and deterministic mutation tests pass. |
| Supply corrupt or partial SQLite state | Rebuild or direct-read fallback | Corrupt-state recovery and error-path tests pass. |
| Exfiltrate prompt or content through observations | Store aggregate allowlisted dimensions only | Privacy and reset tests pass. |
| Remove FTS5 or make the process time out | Return authoritative direct reads | Adapter exception boundary and fallback tests pass. |

## Security Validation

- Confirmed facts: No unresolved high, medium, or low security finding remains.
  The review covered identity applicability, authorization scope, inputs, state,
  retry and concurrency behavior, secrets, dependencies, logging, data exposure,
  negative paths, and workflow abuse.
- Evidence: 11 focused cache tests, 19 focused StepCard tests, a visible
  178-test shared-runtime regression, documentation checks, SDD gates, and patch
  hygiene pass. The final canonical validation receipt will be regenerated after
  all lifecycle files are synchronized.
- Open questions/blockers: None. Residual risks are local-at-rest visibility,
  heuristic secret detection, host-dependent latency, and recoverable FTS5
  absence.
