# Prepare

## Entry

The contributor invoked the usage coach or requested behavioral workflow feedback.

## Procedure

Resolve safe project-relative paths, active or requested session identifier, and establish read-only coaching advisory authority. Fail open if the usage session directory does not yet exist.

### 0.1 Required Inputs

- Active repository root or target project path.
- Local append-only session event journal directory (`.ai-sdlc/usage/sessions/`).
- Optional session identifier or window threshold in days (default: 30 days, 10 sessions).

### 0.2 Clarification Rules

- Derive observations strictly from recorded session events; never invent historical actions.
- When no session logs are present, report a clean zero-event status with guidance rather than blocking.
- Present actionable suggestions with evidence, pattern description, and value rationale.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.

### 0.3 Output Rules

- Keep output structured with clear summary, coverage, transition motifs, and suggestions.
- Return deterministic findings without remote telemetry or productivity grading.
- Before final response, emit the `ai-sdlc-handoff/v2` contract.

### 0.4 Artifact Routing

- Usage events are recorded into append-only local files under `.ai-sdlc/usage/sessions/<date>/<session_id>.toon`.
- Feedback records are appended to `.ai-sdlc/usage/feedback.toon`.
- Read-only coaching reports are presented in chat output without mutating project source code.

## Execution contract

Read the [shared execution decisions](../../skills/ai-sdlc-shared-runtime/references/execution-contract.md) once for this invocation.
Coach provides evidence-backed suggestions and reports; it never mutates source code or grants workflow approvals.

## Exit

Input paths are resolved and journal discovery bounds are established.

## Chat presentation

Before a result, warning, blocker or question, apply the local [chat schema](../references/chat-output.toon) and the Chat Output Contract in `SKILL.md`. Preserve native artifact and tool-input formats.
