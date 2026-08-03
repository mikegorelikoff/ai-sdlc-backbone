---
type: "ai-sdlc.qa-plan"
title: "QA Plan"
description: "Acceptance, regression, risk, and manual validation plan."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T09:43:21Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "qa.md"
  path: "specs/017-local-context-cache/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs/017-local-context-cache/decision-log.md"
  status: "approved"
  owner: "QA and Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-009"
    - "TC-012"
  related_artifacts:
    - "specs/017-local-context-cache/decision-log.md"
    - "specs/017-local-context-cache/design.md"
    - "specs/017-local-context-cache/index.md"
    - "specs/017-local-context-cache/requirements.md"
    - "specs/017-local-context-cache/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "approved"
    - "context-cache"
---

# QA

## Change Summary
Introduce an opt-in, local, deterministic graph-enhanced RAG cache while preserving repository authority, context-pack/v4, default installation, offline portability, and TOON-only machine interfaces.

## Acceptance Scenarios
- QA-001: build twice and verify deterministic logical receipts (TC-001).
- QA-002: update changed and deleted sources and inspect stale-row removal (TC-002).
- QA-003: repeat lexical and graph queries under tie, depth, and node bounds (TC-003/TC-004).
- QA-004: validate packed and direct-read context-pack/v4 outcomes across budgets and stale state (TC-005/TC-006).
- QA-005: exercise unsafe content and instruction-injection fixtures (TC-007/TC-008).
- QA-006: verify TOON-only output, installation selection, purge confinement, and complete regression gates (TC-009 through TC-012).

## Regression Targets
All 46 installable skill graphs and routers, the 45-skill default profiles, shared TOON codec, context-pack/v4 validation, module discovery, project-context behavior, scheduler freshness gates, docs catalogs, compatibility counts, and security scans.

## Risk Notes
- High: stale or poisoned evidence could alter implementation decisions.
- High: cache path or purge traversal could damage repository content.
- High: indexed credentials could persist sensitive data locally.
- Medium: graph-enhanced expansion could negate token savings.
- Medium: optional installation could accidentally change default inventory.
Controls are hash verification, evidence-only authority, strict confinement, secret exclusion, hard budgets, and install matrix tests.

## Validation Commands
- `python3 skills/ai-sdlc-context-cache/tests/test_context_cache.py`
- `python3 skills/ai-sdlc-shared-runtime/tests/test_each_skill_tests.py`
- `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_test_suite.py --format toon`
- `python3 docs/scripts/build_catalog.py --check`
- `python3 docs/scripts/validate_docs.py`
- `python3 -m unittest discover -s docs/tests -v`
- `mkdocs build --strict`
- `git diff --check`

## Manual Checks
Inspect one query receipt and its source ranges, one graph path, one stale fallback, the disposable database location, default and opt-in install records, and a purge receipt. Confirm that retrieved instruction-shaped content remains labeled evidence-only.

## Signoff
Signoff requires current evidence for TC-001 through TC-012, no alternate machine format machine interface, no default install regression, no unresolved high-severity security finding, and successful validation of every emitted context pack.
