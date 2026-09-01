---
type: "ai-sdlc.design"
title: "Design"
description: "Technical design, interfaces, architecture, and migration decisions."
tags:
  - "ai-sdlc"
  - "sdd"
  - "design"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-09-01T09:52:02Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "design.md"
  path: "specs/022-ai-sdlc-loop/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-09-01"
  trace_ids:
    - "TC-032"
    - "TC-039"
  related_artifacts:
    - "specs/022-ai-sdlc-loop/branch-plan.md"
    - "specs/022-ai-sdlc-loop/code-review.md"
    - "specs/022-ai-sdlc-loop/commit-message.md"
    - "specs/022-ai-sdlc-loop/commit-readiness.md"
    - "specs/022-ai-sdlc-loop/decision-log.md"
    - "specs/022-ai-sdlc-loop/index.md"
    - "specs/022-ai-sdlc-loop/plan.md"
    - "specs/022-ai-sdlc-loop/qa.md"
    - "specs/022-ai-sdlc-loop/requirements.md"
    - "specs/022-ai-sdlc-loop/security-review.md"
    - "specs/022-ai-sdlc-loop/tasks.md"
    - "specs/022-ai-sdlc-loop/test-cases.md"
    - "specs/022-ai-sdlc-loop/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "approved"
    - "engineering-quality-gate"
    - "ai-sdlc-loop"
---

# Design

## Overview
Add one canonical Harness core skill, `ai-sdlc-engineering-quality-gate`, plus the autonomous Loop adaptation `ai-sdlc-loop-engineering-quality-gate`. Both use the same v1 context/report contract and five-node v2 skill graph. The gate runs after implementation, inspects the bounded diff and repository evidence, produces findings before mutation, applies only authorized localized High/Medium fixes, reruns verification, and finalizes a current deterministic report. Loop changes its mandatory route to Specify → Implement → Engineering Quality Gate → Verify → Commit and hard-blocks Verify when the report is missing, non-ready, invalid, or stale.

## Architecture
The skill package follows existing code-review, validation, and quality-lenses conventions: thin `SKILL.md` router; deterministic `steps/manifest.toon`; prepare/context/execute/validate/handoff step documents; reference schemas and examples; one Python-standard-library helper; and skill-local tests. Semantic repository judgment remains with the agent, while the helper deterministically captures the change surface, validates typed evidence, enforces readiness invariants, canonicalizes TOON, fingerprints stable fields, and writes atomically. Harness registers the canonical package in `modules/core/module.toon` and managed inventory. Loop carries a namespaced local adaptation and remains independently installable.

## Components
- Context profiler: resolves a Git diff or working-tree target, emits sorted repository-relative changed files and scope metrics, ranks bounded neighboring/test/config candidates with documented tie-breakers, and fingerprints stable evidence.
- Engineering reviewer: reads the requested change, selects and inspects 2–5 representative implementations where practical, builds a repository profile, records typed findings, checks correctness/repository fit/simplicity/maintainability/testing/security/scope, and performs anti-AI-code checks.
- Fix loop: applies only authorized High and safe localized Medium fixes, never Low-only cleanup, then regenerates context so every report binds to the post-fix diff.
- Verification adapter: detects repository-owned commands, records the smallest relevant checks before and after fixes, and preserves explicit `pass`, `fail`, `not_run`, or `unavailable` status.
- Report finalizer: validates the v1 schema and PASS invariants, sorts all stable collections, computes a report fingerprint, and atomically writes canonical TOON.
- Loop enforcement: installer includes the new skill, orchestrator routes through it, and Verify compares the report change fingerprint with the current approved snapshot before running commands.

## Interfaces and Contracts
The helper exposes inspectable CLI help and three deterministic actions: create a bounded context profile, finalize a draft report against the current context, and verify an existing report against repository state. Inputs use repository-relative paths, optional base revision, optional Loop feature, explicit TOON draft/report paths, and no shell command strings. The finalizer accepts only the documented finding, verification, repository-profile, change-scope, evidence, and decision fields. Harness durable outputs use schema `ai-sdlc-engineering-quality-gate/v1`; the Loop adaptation uses the same payload contract with its namespaced skill ID. Loop stores the current report below `.ai-sdlc-loop/<feature>/quality-gate.toon`.

## Data Model
Context contains schema, review target, base/head identity when available, sorted changed-file records, line totals, bounded candidate records, detected verification sources, and `context_fingerprint`. A finding contains stable ID, severity, category, file, optional location, issue, non-empty evidence list, impact, recommended fix, resolution state, and optional applied fix. Verification contains a stable ID, kind, command argv, phase, required flag, status, evidence, and optional counts/reason. Report contains summary, repository profile, fixed and remaining findings, verification, change scope, quality evidence, final decision, context fingerprint, and report fingerprint. Timestamps, durations, absolute paths, and raw nondeterministic command output are excluded from signed identity.

## Error Handling
Fail closed for non-Git targets, unsafe or escaping paths, malformed/unsupported TOON, unsorted or duplicate stable IDs, invalid enums, missing finding evidence, PASS with unresolved High or blocking Medium findings, PASS with a failed or unexecuted required available check, readiness/status disagreement, context drift, and report output outside the repository or with a non-TOON extension. Write no partial report on failure. Product clarification remains an explicit unresolved finding rather than guessed behavior.

## Security Considerations
Use subprocess argv without a shell, read only the bounded repository surface by default, contain all paths, reject symlinks for canonical outputs, and never persist secrets or unbounded raw command output. Quality-gate mutations require the existing implementation authority and approved path scope in Loop. The helper validates evidence structure; it does not authenticate reviewers or authorize broader writes. Security findings require repository evidence and remain scoped to the changed behavior.

## Observability
The agent returns the concise structured quality report and exact commands/outcomes. Canonical TOON records stable context, examples, patterns, findings, verification status, change scope, decision, and fingerprints. `verify` reports the specific invariant or drift that blocks promotion. Loop `status` and promotion include current quality-gate state when available. No telemetry is added.

## Risks and Tradeoffs
The new gate overlaps existing review and validation skills by design but owns a different boundary: it combines repository-fit review, safe remediation, rerun evidence, and a delivery decision. It reuses existing conventions instead of replacing those skills. Deterministic helpers cannot prove semantic correctness; they make evidence selection and PASS policy reproducible while the agent supplies repository-grounded judgment. Bounded candidate ranking may yield fewer than two useful comparisons, which must be disclosed rather than padded with weak examples. Making the gate mandatory is a deliberate Loop workflow change and requires migration notes and tests.

## Validation Strategy
Implement TC-032 through TC-039. Unit-test canonical context/report output, equivalent-root path independence, stable ordering, path safety, schema invariants, finding validation, verification status policy, atomic writes, current/stale fingerprints, and PASS/PASS_WITH_FINDINGS/FAIL decisions. Integration-test Harness module/default discovery, v2 step selection, script contracts, generated catalogs, Loop exact installation, orchestrator order, Verify denial before current evidence, success after ready evidence, and stale denial after drift. Run focused skill tests first, then complete Loop and Harness validation sequences.

## Migration Notes
This is additive in Harness core and a mandatory stage addition in Loop. Existing public paths remain. After incorporating the upstream Flow and Doctor additions, Loop installed inventory changes from nineteen to twenty packages; working skills change from eighteen to nineteen plus shared runtime. Existing Loop feature state without a current quality report cannot enter Verify after upgrade until the gate is run for the current diff. No existing skill is renamed or removed; generated catalogs are refreshed from source.
