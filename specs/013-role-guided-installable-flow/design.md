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
  at: "2026-07-27T12:13:45Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "013-role-guided-installable-flow"
  artifact: "design.md"
  path: "specs/013-role-guided-installable-flow/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/013-role-guided-installable-flow/_ai_sdlc/state.toon"
  decision_log: "specs/013-role-guided-installable-flow/decision-log.md"
  status: "review"
  owner: "Engineering"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids: []
  related_artifacts:
    - "specs/013-role-guided-installable-flow/branch-plan.md"
    - "specs/013-role-guided-installable-flow/code-review.md"
    - "specs/013-role-guided-installable-flow/decision-log.md"
    - "specs/013-role-guided-installable-flow/plan.md"
    - "specs/013-role-guided-installable-flow/qa.md"
    - "specs/013-role-guided-installable-flow/requirements.md"
    - "specs/013-role-guided-installable-flow/tasks.md"
    - "specs/013-role-guided-installable-flow/test-cases.md"
    - "specs/013-role-guided-installable-flow/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "review"
    - "accepted"
---

# Design

## Overview
The solution separates orchestration data from execution code and separates skill discovery from procedural context. The canonical runtime owns flow parsing, role/action selection, selector validation, context assembly, fingerprints, state prerequisites, v2 serialization, and skill-step selection. Each SKILL.md becomes a concise router; its complete normative workflow lives in phase-addressable files declared by a skill-owned manifest.

## Architecture
`skills/ai-sdlc-flow/scripts/flow.py` imports only `skills/ai-sdlc-shared-runtime/scripts`. It loads repository configuration and the flow-owned registries, calls the runtime router, and emits a v2 DecisionCard. All other skills import the same runtime directly. Documentation generation reads the same registries rather than maintaining hand-written copies.

## Components
1. Canonical shared runtime: artifact, state, config, install, context, flow, and skill-step selector modules.
2. Flow registry: schema-validated role, action, flow-step, and context-selector declarations.
3. Role contracts: five source-neutral Markdown references.
4. Flow steps: complete clarification, routing, execution, handoff, validation, and completion instructions.
5. Per-skill step packages: `steps/manifest.json` plus prepare, execute, and validate/handoff Markdown procedures, or a more specific phase set where the skill requires it.
6. Concise SKILL.md routers: trigger metadata, skill card, selector table, and mandatory progressive-disclosure rules.
7. Flow entrypoint: argument parsing, repository wiring, and selected owning-skill step evidence.
8. Documentation generator and install smoke harness.
9. Unit, contract, integration, drift, size-budget, installation, and context-economics tests.

## Interfaces and Contracts
DecisionCard schema id remains `ai-sdlc-flow/v2`. The skill-step manifest schema is `ai-sdlc-skill-steps/v1`; each selector contains id, path, phases, roles, actions, load rule, max_tokens, and reason. The canonical selector CLI accepts `--skill`, `--phase`, optional `--role` and `--action`, repository root, and output format. A SKILL.md router links every declared step and requires prepare before action, execute only for the selected work, and validation/handoff before completion.

## Data Model
Role records contain id, label, and aliases. Action records map stable action ids and codes to skills and owners. Flow selectors choose role/flow references. Skill-step manifests map a skill and selector ids to contained Markdown paths, lifecycle phases, canonical roles, optional actions, load rules, token caps, and human-readable reasons. Selection results contain selected/skipped records, token counts, manifest and selection fingerprints, and the broad per-skill baseline. Fingerprints are SHA-256 hashes of canonical JSON.

## Error Handling
Reject unsupported schemas, unknown role/action/skill/phase ids, ambiguous aliases, invalid menu modes, unknown selector fields, invalid priorities/token caps/load rules, duplicate selector ids or paths, missing or unlinked step files, non-regular files, absolute paths, traversal, symlink escapes, oversized selections, and missing installed runtime modules. Errors identify the invalid field and remediation; v1 errors name the v2 migration.

## Security Considerations
Resolve every selected path against the repository root, require it to remain contained after symlink resolution, accept only regular files matched by trusted registry entries, never execute selected content, cap bytes/tokens, ignore secrets and VCS internals by default, and run global-install tests under a temporary home.

## Observability
Decision output records route source, requested/active role, handoff reason, action, state prerequisite, current step, selected/skipped references with reasons, token estimates, selector fingerprint, and effective configuration fingerprint. Tests snapshot deterministic fields while excluding environment-specific absolute paths.

## Risks and Tradeoffs
A hard v2 cut intentionally breaks v1 consumers but avoids dual semantics. JIT context can omit useful background, mitigated by required-reference tests and explicit selector reasons. Five roles simplify comprehension while requiring careful cross-role handoffs. One runtime removes drift but makes install packaging a critical dependency, covered by three install modes.

## Validation Strategy
Validate registry/schema fixtures, 44 manifest inventories, router line and aggregate word budgets, instruction preservation, role uniqueness, routing precedence, ambiguity menus, handoffs, v1 rejection, per-package path containment, configuration bounds, deterministic fingerprints, owning-skill JIT selection, context recall/token reduction, generated-doc drift, all import sites, skill inventory, project/selective/global installs, focused unit suites, and repository-wide tests.

## Migration Notes
Mechanically preserve existing SKILL.md sections while relocating them into prepare, execute, and validate/handoff step files. Keep the Skill Card and a generated selector table in SKILL.md. Expand flow's six phase files rather than replacing them with generic steps. Add manifests after content exists, validate links and token caps, update docs generation to read the router plus ordered steps, then enable flow integration. No instruction may be deleted merely to satisfy the size budget.

Migrate Feature 013 implementation and refinement directories as complete OKF bundles. Future durable writes migrate an entire legacy feature atomically; untouched historical features remain unchanged. Replace human workspace specs indexes with feature-local reserved indexes, keep the compact TOON router, and move project context to `_ai_sdlc/context/project-context.md` with no legacy runtime fallback.

## OKF Artifact Architecture
- `ai_sdlc_okf.py` is the standard-library authority for concept rendering, controlled frontmatter merge, provenance, status mapping, conformance checks, atomic bundle migration, and progressive indexes.
- Artifact profiles own stable `type`, `title`, and `description`; generators must not infer a type at write time. Existing nested `artifact_metadata` remains an extension and preserves lifecycle status separately from OKF `status`.
- `specs/<feature>/`, `specs-refiniment/<feature>/`, and `changes/<change-id>/` are independent bundles. `_ai_sdlc/` is the repository runtime bundle. Reserved root indexes declare OKF v0.2; nested indexes contain no frontmatter.
- `specs[-refiniment]/_ai_sdlc/specs-index.toon` becomes a v2 compact projection. It indexes OKF type/title/status/trust plus existing trace metadata and excludes reserved `index.md` and `log.md`.
- A concept refresh preserves `generated.by` unless explicitly overridden, updates `generated.at` only for meaningful content/provenance changes, and clears verification when body, sources, resource, type, title, or description changes.
- Internal draft/review/blocked maps to OKF draft; approved/validated/done maps to stable; superseded/deprecated maps to deprecated. No lifecycle state creates `verified`.
- Project context writes only `_ai_sdlc/context/project-context.md`; module discovery writes `_ai_sdlc/modules.md`; no root-path compatibility read or write remains.
- Existing source snapshots are wrapped as `External Specification Snapshot` concepts, retain source bytes in the body, and record explicit logical source/hash evidence.
