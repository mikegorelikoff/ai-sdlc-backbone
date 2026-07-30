---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "012-deduplicate-skill-entrypoints"
  artifact: "design.md"
  path: "specs/012-deduplicate-skill-entrypoints/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/012-deduplicate-skill-entrypoints/_ai_sdlc/state.toon"
  decision_log: "specs/012-deduplicate-skill-entrypoints/decision-log.md"
  status: "approved"
  owner: "Repository Maintainers"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids: []
  related_artifacts:
    - "specs/012-deduplicate-skill-entrypoints/branch-plan.md"
    - "specs/012-deduplicate-skill-entrypoints/decision-log.md"
    - "specs/012-deduplicate-skill-entrypoints/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "approved"
    - "deduplication"
---

# Design

## Overview
Consolidate cross-lifecycle routing into `ai-sdlc-flow` and delete the redundant navigator package.

## Architecture
The flow shared core becomes the only intent classifier. Its route table covers discovery, SDD, review, validation, QA gap review, story decomposition, and other navigator-only signals; Apply remains allow-listed only for lifecycle actions it can safely begin.

## Components
`skills/_shared/ai_sdlc_flow.py` owns classification and DecisionCard logic; `skills/ai-sdlc-flow/` owns CLI/tests; manifests, managed lists, compatibility, install smoke, catalog generator, generated docs, README, and tutorials expose the retained skill.

## Interfaces and Contracts
Keep schema `ai-sdlc-flow/v1`, protected flow flags, Markdown/TOON Explore formats, and direct `$ai-sdlc-*` invocation. Delete the `ai-sdlc-navigator/v1` public entrypoint and document the transition.

## Data Model
Extend intent rules without changing DecisionCard fields. Skill inventory count changes from 45 to 44.

## Error Handling
Ambiguous multi-class intent remains blocked. Unsupported Apply targets remain read-only recommendations rather than executable actions.

## Security Considerations
Do not broaden Apply allow-lists while importing navigator read-only routes. Preserve bounded paths, source hashing, drift checks, and sandbox authority.

## Observability
Catalog, compatibility, install-smoke, and module outputs expose the 44-skill count; no external telemetry.

## Risks and Tradeoffs
Removing a protected ID is breaking; mitigate with a migration note during the release-candidate line. Over-expanding Apply would be unsafe; imported routes default to Explore-only unless already allow-listed.

## Validation Strategy
Add route parity tests for all navigator-only signals, scan tracked files for stale references, regenerate catalogs, and run flow, module, compatibility, docs, install-smoke, and shared contract suites.

## Migration Notes
Replace `ai-sdlc-navigator --quick-flow|--full-flow` with `ai-sdlc-flow Explore` using the same intent and explicit feature. Direct owning-skill calls remain supported.
