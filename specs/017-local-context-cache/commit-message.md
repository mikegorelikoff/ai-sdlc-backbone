---
type: "ai-sdlc.commit-message"
title: "Commit Message"
description: "Validated Conventional Commit message for the optional local context cache."
tags:
  - "ai-sdlc"
  - "commit"
  - "context-cache"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "commit-message.md"
  path: "specs/017-local-context-cache/commit-message.md"
  workspace: "implementation"
  skill: "ai-sdlc-conventional-commit"
  flow_mode: "full"
  state_file: "specs/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs/017-local-context-cache/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "DEC-004"
    - "T001"
    - "T002"
    - "T003"
    - "T004"
    - "T005"
    - "T006"
    - "T007"
    - "T008"
  related_artifacts:
    - "specs/017-local-context-cache/commit-readiness.md"
    - "specs/017-local-context-cache/validation.md"
    - "specs/017-local-context-cache/code-review.md"
    - "specs/017-local-context-cache/security-review.md"
  validation:
    - "validate_commit_msg.py --full-flow --require-traceability"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-conventional-commit"
    - "commit-message"
    - "approved"
---

# Commit Message

````text
feat(context-cache): add deterministic local retrieval

Business context

Reduce repeated repository reads and token use while preserving authoritative
sources, deterministic evidence, and safe direct-read recovery.

Implementation details

- add opt-in SQLite FTS5 lexical and typed graph-enhanced retrieval with
  incremental indexing, freshness checks, bounded traversal, and safe purge
- add context-pack/v4 assembly with mandatory owning steps, complete critical
  anchors, evidence-only repository ranges, and a 15 percent savings gate
- add deterministic TOON benchmarks, module installation, compatibility,
  documentation, security review, and full-flow lifecycle evidence

Change flow

Repository sources -> local deterministic index -> bounded evidence pack ->
freshness and authority gates -> packed context or direct read

Mermaid diagram

```mermaid
flowchart LR
  S[Repository sources] --> I[Local FTS5 index]
  I --> R[Lexical and graph retrieval]
  R --> G[Freshness and authority gates]
  G -->|sufficient and economic| P[Context pack v4]
  G -->|stale or incomplete| D[Direct read]
```

How to test

- build and query the optional cache in a temporary Git repository
- add, modify, delete, or hide eligible sources and confirm safe fallback
- install default and context-cache module profiles and compare inventories

Validation

- 17/17 canonical validation commands passed
- 100/100 skill-owned test files passed
- 8/8 focused context-cache tests passed
- 18/18 refinement artifacts complete with zero blockers
- repository diff hygiene and TOON-only interchange checks passed

Spec: specs/017-local-context-cache
Task: T001, T002, T003, T004, T005, T006, T007, T008
Validation: specs/017-local-context-cache/_ai_sdlc/validation-receipt.toon
````
