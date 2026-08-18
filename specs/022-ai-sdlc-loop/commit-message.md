---
type: "ai-sdlc.commit-message"
title: "Loop Corrective Commit Message"
description: "Validated Conventional Commit message for the corrected AI SDLC Loop skill graph and TOON boundary."
tags:
  - "ai-sdlc"
  - "commit"
status: "stable"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "commit-message.md"
  path: "specs/022-ai-sdlc-loop/commit-message.md"
  workspace: "implementation"
  skill: "ai-sdlc-conventional-commit"
  flow_mode: "full"
  state_file: "specs/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-08-17"
  trace_ids:
    - "T001"
    - "T002"
    - "T003"
    - "T005"
    - "T006"
    - "T007"
  related_artifacts:
    - "specs/022-ai-sdlc-loop/commit-readiness.md"
    - "specs/022-ai-sdlc-loop/security-review.md"
    - "specs/022-ai-sdlc-loop/validation.md"
  validation:
    - "validate_commit_msg.py --full-flow specs/022-ai-sdlc-loop/loop-final-pack-commit.txt"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-conventional-commit"
    - "commit-message"
    - "approved"
    - "ai-sdlc-loop"
---

# Commit Message

Canonical parent integration commit input: `harness-loop-integration-commit.txt`.

The raw file is authoritative so `git commit -F` consumes the same bytes that
the full-flow Conventional Commit validator checked. It covers the exact Loop
gitlink, live MkDocs site, product-family documentation, release evidence, and
SDD traceability for T004 and T006 through T010.
