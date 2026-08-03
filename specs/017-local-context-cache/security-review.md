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
  at: "2026-08-03T10:28:14Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "security-review.md"
  path: "specs/017-local-context-cache/security-review.md"
  workspace: "implementation"
  skill: "ai-sdlc-security-testing"
  flow_mode: "full"
  state_file: "specs/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs/017-local-context-cache/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-002"
    - "AC-007"
    - "AC-009"
    - "AC-013"
    - "TC-002"
    - "TC-007"
    - "TC-009"
    - "TC-013"
  related_artifacts:
    - "specs/017-local-context-cache/branch-plan.md"
    - "specs/017-local-context-cache/decision-log.md"
    - "specs/017-local-context-cache/design.md"
    - "specs/017-local-context-cache/index.md"
    - "specs/017-local-context-cache/plan.md"
    - "specs/017-local-context-cache/qa.md"
    - "specs/017-local-context-cache/requirements.md"
    - "specs/017-local-context-cache/tasks.md"
    - "specs/017-local-context-cache/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-security-testing"
    - "security-review"
    - "approved"
    - "context-cache"
---

# security-review.md

## Trust Boundaries
- Protected assets: repository source, instruction authority, credentials, the derived SQLite cache, TOON receipts, and the purge boundary.
- Trusted control plane: the installed skill manifest, step documents, schemas, runtime code, and caller supplied bounds.
- Untrusted evidence plane: repository text, filenames, imports, path references, benchmark queries, and cached chunks. Retrieved repository text remains evidence_only and cannot override system, user, skill, or step instructions.
- External boundary: the runtime performs no network access, plugin execution, model call, or shell command. SQLite is project-local derived state.
- Filesystem boundary: discovery and purge are confined to resolved project/cache roots. Symlinks, generated trees, cache trees, binaries, oversized files, secret-like names, and credential-like content are excluded.
- Transaction boundary: builds use a temporary database and atomic replacement; queries are read-only and verify source freshness before packing.
- Residual risk: a repository can contain adversarial natural language that influences a downstream model. Authority labels, mandatory owning-step inclusion, provenance, and direct-read fallback reduce but cannot eliminate model-layer prompt-injection risk.

## Authn/Authz
- The module has no identity, account, network service, multi-user endpoint, or privileged API; authentication is out of scope.
- Authorization is represented as local process and filesystem permissions. The runtime never elevates privileges.
- Root and cache paths are normalized and containment-checked before access. Purge can remove only the explicit cache database and its SQLite sidecars within the configured cache directory.
- Repository evidence cannot become instruction authority. The pack marks skill and step content as skill_instruction and repository results as evidence_only.
- Installer activation is explicit through --module context-cache; the default managed inventory is unchanged.
- Security decision: no hidden authorization layer is invented for a local optional component; host filesystem controls remain authoritative.

## Input Validation
- CLI bounds for limits, graph depth, chunk size, overlap, budgets, and benchmark cases are type-checked and range-bounded.
- Paths are resolved before containment checks; symlinks and unsafe cache targets are rejected.
- FTS input is tokenized and normalized into a restricted lexical expression. SQL values use bound parameters; repository text is never concatenated as executable SQL.
- Benchmark cases require the strict TOON schema ai-sdlc-context-cache-benchmark-cases/v1 and validated fields. Unknown or malformed structure fails closed.
- Skill and step identifiers are resolved through the manifest; an owning step must exist before packed context is eligible.
- Chunk decoding is deterministic and invalid encodings, binary content, and oversized inputs are skipped with explained counters.
- Graph traversal has explicit depth and result limits, preventing unbounded expansion.

## Secret Handling
- Discovery rejects secret-like paths and filenames, including common environment, key, credential, and token artifacts.
- Content scanning rejects credential-like material before indexing. This is defense in depth, not a guarantee against every custom secret format.
- Query, inspect, verify, benchmark, and pack receipts do not intentionally echo excluded secret values.
- No credentials are required, persisted, transmitted, or logged by the cache.
- The SQLite database is derived local state and can contain non-secret repository text; it inherits repository filesystem sensitivity and must not be published.
- Residual risk: heuristic secret detection can have false negatives. Teams must keep secret scanning and least-privilege repository access as independent controls.

## Data Exposure
- Data stays local; there is no telemetry or remote embedding provider in the MVP.
- Indexed data is limited to eligible repository text plus hashes, paths, chunk coordinates, typed edges, and FTS terms.
- Receipts expose provenance and scores needed for audit but do not upgrade evidence authority.
- The cache directory is ignored by Git and optional installation does not add cached content to distributable artifacts.
- Inspect reports metadata and counts; query and pack return only bounded results.
- Purge removes the derived database and sidecars while preserving repository sources.
- Residual risk: anyone who can read the cache may infer or read indexed repository content. Filesystem access to the cache must be no broader than access to the repository.

## Abuse Cases
- Prompt injection in source text: a malicious file asks the agent to ignore policy. Control: evidence_only labeling, mandatory authoritative step document, provenance, bounded retrieval, and no execution.
- Path escape: a caller points cache or purge outside the project. Control: resolved containment checks and explicit target allowlist.
- Symlink exfiltration: a repository symlink targets credentials. Control: symlinks are excluded from discovery.
- SQL or FTS injection: a crafted query changes database behavior. Control: bound SQL parameters and restricted lexical query construction.
- Cache poisoning or stale evidence: source changes after build. Control: semantic fingerprints, freshness verification, incremental invalidation, atomic replacement, and direct_read fallback.
- Resource exhaustion: huge files, broad graph traversal, or oversized benchmark suites consume resources. Control: file size, chunk, result, depth, token-budget, and case-count bounds.
- Secret indexing: credentials use unusual names or encodings. Control: filename and content heuristics plus documented residual risk and independent secret scanning.
- Authority confusion: graph neighbors appear authoritative due to relevance. Control: explicit authority field, stable explanation fields, and critical-anchor completeness gate.
- Non-deterministic evaluation: wall-clock timing changes receipts. Control: golden correctness receipts exclude timing; latency is a separate observational tier.

## Security Validation
- SEC-001 discovery tests cover symlink, binary, oversized, secret-name, credential-content, generated-tree, and cache-tree exclusions.
- SEC-002 query tests cover parameterized lexical retrieval, stable scoring, bounded graph traversal, typed edges, and byte-stable TOON output.
- SEC-003 pack tests require the owning step document, 100 percent declared critical anchors, source freshness, evidence_only repository chunks, and at least 15 percent savings before packed mode.
- SEC-004 purge tests verify confinement to the explicit project-local cache target.
- SEC-005 installer tests verify opt-in activation and an unchanged default skill inventory.
- SEC-006 benchmark tests compare lexical, graph-enhanced, and pack modes with deterministic fingerprints, expected path and anchor recall, and separate observational latency.
- SEC-007 compatibility and documentation checks protect the benchmark contracts, context-pack/v4, TOON-only public contracts, and generated catalogs.
- Review result: no known critical, high, or medium finding remains in the reviewed local-only MVP. Accepted residual risks are heuristic secret detection, downstream model susceptibility to adversarial evidence, cache readability matching filesystem permissions, and SQLite build compatibility.
- Traceability: FR-002, FR-004, FR-005, FR-006, FR-008, FR-009, FR-012, FR-013; AC-002 through AC-007, AC-009 through AC-013; TC-002 through TC-007 and TC-009 through TC-013.
