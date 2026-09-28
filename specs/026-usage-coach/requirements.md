---
type: "ai-sdlc.requirements"
title: "Requirements"
description: "Implementation requirements, constraints, and acceptance criteria."
tags:
  - "ai-sdlc"
  - "sdd"
  - "requirements"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-09-28T10:00:00Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "026-usage-coach"
  artifact: "requirements.md"
  path: "specs/026-usage-coach/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/026-usage-coach/_ai_sdlc/state.toon"
  decision_log: "specs/026-usage-coach/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-09-28"
  updated_at: "2026-09-28"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "DEC-001"
  related_artifacts:
    - "specs/026-usage-coach/decision-log.md"
    - "specs/026-usage-coach/design.md"
    - "specs/026-usage-coach/index.md"
    - "specs/026-usage-coach/plan.md"
    - "specs/026-usage-coach/qa.md"
    - "specs/026-usage-coach/tasks.md"
    - "specs/026-usage-coach/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "draft"
---

# Requirements

## Goal
Make AI SDLC Loop self-observing through a local, repository-native, event-sourced behavioral feedback loop and evidence-backed interactive usage coach without telemetry, external services, or productivity scoring.

## Problem Statement
Loop users navigate complex multi-skill workflows, iterative delivery, and quality gates, but recurring patterns of friction, rework cycles, evidence lag, and underutilized skills remain invisible across sessions. Existing tools either offer no behavioral feedback or rely on invasive remote telemetry, mutable analytics databases, and superficial metrics that do not provide actionable, evidence-based guidance.

## Scope
Deterministic local usage journaling in shared runtime, append-only TOON session logs, on-demand behavioral signal derivation, interactive usage coach skill (`ai-sdlc-loop-usage-coach`) with CLI and chat output contracts, fail-safe error handling, and end-to-end scenario validation (Scenarios A through F).

## Actors
Software Engineer / Contributor; AI SDLC Loop runtime; interactive usage coach agent; deterministic validator.

## Inputs
User commands and requests; skill execution lifecycles; user interactions and decisions; verification outcomes; existing Loop receipts and session journals.

## Outputs
Append-only session journals in `.ai-sdlc-loop/usage/sessions/<date>/<session_id>.toon`; derived behavioral analysis (skill coverage, discoverability, transition graphs, rework cycles, gate timing, evidence lag, decision churn, context switching, ignored recommendations, capability gaps); structured evidence-backed coaching suggestions; feedback records.

## Functional Requirements
AC-001: Store one append-only event journal per agent session in `.ai-sdlc-loop/usage/sessions/<date>/<session_id>.toon` using a keyed `events` dictionary with monotonically increasing local sequence keys (`e000001`, `e000002`).
AC-002: Enforce strict data minimization and secret redaction: record semantic facts, identifiers, and references; never persist full user prompts, raw source code, model-generated prose, secrets, or arbitrary command stdout.
AC-003: Provide fail-safe and fail-open recording resilience: any journal read/write error, missing directory, or permission failure must be gracefully suppressed without interrupting or failing the user's SDLC execution.
AC-004: Capture a comprehensive event taxonomy: session lifecycle (`session.start`, `session.end`), skill execution (`skill.start`, `skill.end`), user interactions and decisions, artifact lifecycle, quality gate and verification outcomes, and workflow transitions.
AC-005: Derive behavioral signals purely on-demand by scanning session `.toon` files without maintaining a mutable global analytics database, summary, or skill score.
AC-006: Provide an interactive `ai-sdlc-loop-usage-coach` skill with deterministic CLI commands (`report`, `analyze`, `suggest`, `feedback`, `explain`) and deterministic execution contract.
AC-007: Structure coaching recommendations with fact-based evidence (Observation, Pattern, Evidence, Suggestion, Alternative, Value rationale) and enforce respectful timing policy (silent during rapid flow, speaks on friction, milestone, or request).
AC-008: Preserve existing SDLC contracts, quality gates, approvals, and full backwards compatibility: coach suggestions are advisory and cannot grant approvals or bypass gates.

## Non-Functional Requirements
Deterministic performance with sub-second journal appending; minimal disk footprint; zero network calls or remote telemetry; repository-local storage; fail-open reliability; strict UTF-8 TOON encoding.

## Constraints
All persistent analytics data must be in `.toon` format (no SQLite, JSON, CSV, or remote databases). Journal must be strictly append-only; historical events are immutable. No mutable global summary file. Compatible with Python 3.10+.

## Acceptance Criteria
Given the observed user workflow and event stream, the usage coach and journal must satisfy these criteria:

AC-001: Session journal files are created under `.ai-sdlc-loop/usage/sessions/<date>/<session_id>.toon` with root metadata and append-only keyed events matching `schema: ai-sdlc-loop-usage/v1`.
AC-002: Recorded events contain semantic identifiers, status values, and artifact references; no secret tokens, passwords, raw source lines, or conversation transcripts appear in journal files.
AC-003: Simulated filesystem errors or permission faults during event recording log warnings internally and return gracefully without blocking SDLC task completion.
AC-004: Recorded sessions accurately reflect skill invocations, statuses, durations, user choices, verification pass/fail events, and transitions between skills.
AC-005: Scanned session histories correctly compute skill coverage, discoverability modes (manual vs handoff vs router vs coach), sequence graphs, rework cycles, evidence lag, and capability gaps.
AC-006: `ai-sdlc-loop-usage-coach` CLI provides operable `report`, `analyze`, `suggest`, `feedback`, and `explain` subcommands adhering to the skill contract.
AC-007: Coaching suggestions provide exact citations to historical sessions and event counts, provide concrete next actions, and avoid intrusive interjections during rapid user flow.
AC-008: Existing Loop test suites, verification gates, approvals sandbox, and documentation remain intact; doctor verifies all 28 registered skills.

## Out of Scope
Remote telemetry or cloud aggregation services; automatic code modification without human review; developer productivity scoring or performance surveillance; altering core SDLC security policies.

## Assumptions
The user operates locally within a Git workspace with filesystem access. Default session ID is derived from UTC timestamp and short random token. The journal directory `.ai-sdlc-loop/usage/` is repository-local.

## Open Questions
None blocking implementation. Timing threshold defaults (e.g., 3 rework cycles for unsolicited suggestion) are configurable via standard skill arguments.

## Decision Status
DEC-001 accepted. All blocking decisions are resolved. Accepted assumptions: local append-only event-sourced journal in .ai-sdlc-loop/usage/sessions/ and advisory coach selected; global mutable database and remote analytics explicitly rejected.
