---
type: "ai-sdlc.design"
title: "Design"
description: "Technical design, interfaces, architecture, and migration decisions."
tags:
  - "ai-sdlc"
  - "sdd"
  - "design"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-09-08T10:32:51Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "024-skill-execution-reinforcement"
  artifact: "design.md"
  path: "specs/024-skill-execution-reinforcement/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/024-skill-execution-reinforcement/_ai_sdlc/state.toon"
  decision_log: "specs/024-skill-execution-reinforcement/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-09-08"
  updated_at: "2026-09-08"
  trace_ids: []
  related_artifacts:
    - "specs/024-skill-execution-reinforcement/decision-log.md"
    - "specs/024-skill-execution-reinforcement/index.md"
    - "specs/024-skill-execution-reinforcement/plan.md"
    - "specs/024-skill-execution-reinforcement/qa.md"
    - "specs/024-skill-execution-reinforcement/reinforcement-report.md"
    - "specs/024-skill-execution-reinforcement/requirements.md"
    - "specs/024-skill-execution-reinforcement/tasks.md"
    - "specs/024-skill-execution-reinforcement/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "review"
---

# Design

## Overview
Harden existing mechanisms and preserve product boundaries.

## Architecture
Harness uses semantic StepCards and feature lifecycle profiles. Loop keeps Specify -> Implement -> engineering gate -> Verify -> separately authorized Commit.

## Components
Shared execution guidance, completion closure validation, Loop snapshot checks, owning skill procedures and deterministic evaluation.

## Interfaces and Contracts
Preserve existing schema names, flags, skill IDs, canonical routes and approval boundaries.

## Data Model
Existing manifests, context packs, journals, state and handoffs remain authoritative. Failure records name code, gate, evidence, recovery action and attempts.

## Error Handling
Missing material input blocks dependent work. Invalid/stale evidence returns to its producer. Respect manifest attempts; bound synthesis repair to two cycles; never blindly replay side effects.

## Security Considerations
Preserve path containment, approval binding and source trust boundaries. Fingerprints prove local consistency, not reviewer identity.

## Observability
Record exact command outcomes and per-skill before/after evidence; distinguish structural checks from semantic judgment.

## Risks and Tradeoffs
Shared guidance costs one read; remove identical redundant instructions where possible. Preserve dirty branches and disclose mismatch rather than mix commits.

## Validation Strategy
Run mutation tests before fixes, existing suites after fixes, all-skill evals and product docs/install checks.

## Migration Notes
No schema or public path migration. Invalid completion claims now fail closed.
