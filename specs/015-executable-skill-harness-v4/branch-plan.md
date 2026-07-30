---
type: "ai-sdlc.branch-plan"
title: "Branch Plan"
description: "Branch alignment, delivery boundary, and handoff plan."
tags:
  - "ai-sdlc"
  - "git"
  - "planning"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-29T22:13:58Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "015-executable-skill-harness-v4"
  artifact: "branch-plan.md"
  path: "specs/015-executable-skill-harness-v4/branch-plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-branching"
  flow_mode: "quick"
  state_file: "specs/015-executable-skill-harness-v4/_ai_sdlc/state.toon"
  decision_log: "specs/015-executable-skill-harness-v4/decision-log.md"
  status: "validated"
  owner: "Repository Maintainers"
  created_at: "2026-07-30"
  updated_at: "2026-07-30"
  trace_ids: []
  related_artifacts:
    - "specs/015-executable-skill-harness-v4/decision-log.md"
    - "specs/015-executable-skill-harness-v4/index.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-branching"
    - "branch-plan"
    - "validated"
    - "harness-v4"
---

# branch-plan.md

## Implementation
- Implement hard-cut v4 contracts for executable skill DAGs, per-step context packs, StepCards, durable run journals, host adapter execution, and eval gates.
- Migrate every repository skill through deterministic generated manifests and routers while preserving skill-owned procedures.
- Keep Explore zero-write; create durable state only after Apply.

## Testing
- Add schema, graph, selector, context, runtime replay, idempotency, migration, router-drift, and all-skill deterministic tests.
- Run shared-runtime, owning-skill, documentation, compatibility, and repository-wide validation; keep provider-neutral live eval as a release gate.

## Documentation
- Update canonical contracts, maintainer guidance, public reference pages, spec registry, decision logs, compatibility baseline, and changelog.
- Generated catalogs and routers are regenerated from canonical manifests and checked for drift.
