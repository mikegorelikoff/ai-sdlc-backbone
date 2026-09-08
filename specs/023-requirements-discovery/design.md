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
  at: "2026-09-07T18:49:56Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "023-requirements-discovery"
  artifact: "design.md"
  path: "specs/023-requirements-discovery/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/023-requirements-discovery/_ai_sdlc/state.toon"
  decision_log: "specs/023-requirements-discovery/decision-log.md"
  status: "review"
  owner: "implementation agent"
  created_at: "2026-09-07"
  updated_at: "2026-09-07"
  trace_ids:
    - "TC-001"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-009"
    - "TC-010"
  related_artifacts:
    - "specs/023-requirements-discovery/decision-log.md"
    - "specs/023-requirements-discovery/index.md"
    - "specs/023-requirements-discovery/plan.md"
    - "specs/023-requirements-discovery/qa.md"
    - "specs/023-requirements-discovery/requirements.md"
    - "specs/023-requirements-discovery/tasks.md"
    - "specs/023-requirements-discovery/test-cases.md"
    - "specs/023-requirements-discovery/validation.md"
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
Use one coherent elicitation workflow with product-local names and handoff routes. Share the behavioral contract through equivalent instructions; each package remains portable on its own.

## Architecture
Each product owns the same bounded offline CLI in its skill scripts directory, importing only its sibling TOON runtime. The CLI prepares source contexts, scaffolds model-authored drafts, validates references/coverage, finalizes canonical reports and verifies freshness. Existing lifecycle runtimes remain unchanged.

## Components
Product-local requirements_discovery.py, machine schemas, valid/invalid fixtures and deterministic behavior tests. Harness additionally renders a Markdown projection; Loop persists TOON only. Graph steps invoke the CLI instead of instructing the agent to hand-write final artifacts.

## Interfaces and Contracts
CLI commands: prepare, scaffold, validate, finalize and verify. All default to stdout/read-only; --write writes only fixed product-local feature paths, and --replace authorizes changed output replacement. prepare accepts a bounded project-relative UTF-8 request file or an explicit stdin snapshot plus optional source files. Shared context/draft schemas make analysis portable; product-local report schemas retain product identity. --full-flow takes precedence. --state-check checks existing feature identity without writing state; begin/complete transitions are rejected because discovery owns no lifecycle stage.

## Data Model
Content-bound source contexts contain stable path-derived source IDs, exact SHA-256 digests and UTF-8 text. Drafts contain explicit as_of dates, typed observations, precedents, options, questions, recommendation and owner decision evidence. Canonical collections are sorted by IDs and reference sets are sorted; report digests exclude only their own fingerprint field.

## Error Handling
Reject unknown keys/types, duplicate IDs, dangling links, ungrounded facts/outcomes, missing material-gap or option question coverage, unsupported acceptance and stale sources. Bounded inputs and contained nonsymlink outputs fail before writes. Changed existing output requires --replace; multi-file Harness output rolls back on failure.

## Security Considerations
Treat source text as evidence rather than instructions. Do not execute embedded commands or transmit raw private data in external searches. Preparing questions grants no communication authority.

## Observability
Emit canonical TOON for preparation, scaffold, validation results and finalized reports. Return stable nonzero errors and exact output paths without claiming semantic truth or authenticated approval.

## Risks and Tradeoffs
Scripts guarantee structural and byte determinism for the same analysis, not identical model reasoning or factual truth. Source hashes detect local drift but are not authenticated stakeholder approval. Two independently installed product-local copies keep portability and receive parity tests.

## Validation Strategy
TC-001 through TC-004 retain packaging and docs coverage. TC-005 byte determinism and canonical ordering; TC-006 malformed inputs and reference/coverage failures; TC-007 stale or tampered evidence; TC-008 output containment, idempotence and rollback; TC-009 installed helpers across products; TC-010 Markdown/TOON preservation.

## Migration Notes
The new skill has not been released. Replace its provisional instruction-only contract before publication. Preserve existing product paths and API 4.1.0; add canonical Harness machine report under the existing feature _ai_sdlc directory. No lifecycle state migration.
