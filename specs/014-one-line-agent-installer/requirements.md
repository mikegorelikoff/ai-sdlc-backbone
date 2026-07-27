---
type: "ai-sdlc.requirements"
title: "Requirements"
description: "Implementation requirements, constraints, and acceptance criteria."
tags:
  - "ai-sdlc"
  - "sdd"
  - "requirements"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-27T19:35:17Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "014-one-line-agent-installer"
  artifact: "requirements.md"
  path: "specs/014-one-line-agent-installer/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/014-one-line-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/014-one-line-agent-installer/decision-log.md"
  status: "validated"
  owner: "Repository Maintainers"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "DEC-001"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
  related_artifacts:
    - "specs/014-one-line-agent-installer/decision-log.md"
    - "specs/014-one-line-agent-installer/design.md"
    - "specs/014-one-line-agent-installer/index.md"
    - "specs/014-one-line-agent-installer/plan.md"
    - "specs/014-one-line-agent-installer/qa.md"
    - "specs/014-one-line-agent-installer/tasks.md"
    - "specs/014-one-line-agent-installer/test-cases.md"
    - "specs/014-one-line-agent-installer/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "validated"
    - "installer"
---

# Requirements

## Goal
Make first installation a memorable one-line command for any explicit Skills CLI agent target.

## Problem Statement
The current quick start exposes installer version, telemetry, repository locator, skill selection, and agent flags. Users must edit a long command before they can evaluate the harness.

## Scope
Add a portable POSIX shell entrypoint, focused offline tests, and concise README/install-guide documentation for project-scoped installation.

## Actors
A harness evaluator runs the command; a repository maintainer owns the wrapper; the third-party Skills CLI performs host-specific placement.

## Inputs
One explicit agent identifier, the current working project, and optional environment overrides for source and Skills CLI version.

## Outputs
All harness skills installed project-scoped for the selected agent, with Skills CLI progress and errors passed through unchanged.

## Functional Requirements
- FR-001: `install.sh AGENT` must invoke the pinned Skills CLI once with all skills, the explicit agent, confirmation disabled, and telemetry disabled.
- FR-002: The script must support stdin execution through `curl ... | sh -s -- AGENT` and direct execution through `./install.sh AGENT`.
- FR-003: Missing help or agent input must return clear usage without starting installation.
- FR-004: `AI_SDLC_SOURCE` and `AI_SDLC_SKILLS_CLI_VERSION` must permit maintainers and tests to override the default GitHub source and pinned CLI version.
- FR-005: Documentation must lead with the one-line wrapper and move raw CLI detail to the advanced path.

## Non-Functional Requirements
- NFR-001: Use POSIX `sh` with no Bash-only syntax.
- NFR-002: Quote all user-controlled values and avoid `eval`.
- NFR-003: Preserve project-scoped installation as the default.
- NFR-004: Tests must run without network access.

## Constraints
The wrapper delegates recognized agent names and host layout to Skills CLI 1.5.19. Global installation and immutable-revision audit flows remain advanced procedures.

## Acceptance Criteria
- AC-001: Given `codex`, when the script runs, then it executes `npx -y skills@1.5.19 add mikegorelikoff/ai-sdlc-harness --skill '*' --agent codex -y` with telemetry disabled.
- AC-002: Given another agent identifier, when the script runs, then that exact identifier is passed as one quoted argument.
- AC-003: Given no agent, help, or extra positional arguments, then the script prints actionable usage and does not invoke npx.
- AC-004: Given source and CLI-version overrides, then the generated invocation uses both overrides.
- AC-005: Given shell syntax and focused tests, then the installer passes under POSIX sh without network access.
- AC-006: Given the public docs, then the first install is shown as one line and raw CLI commands are secondary.

## Out of Scope
Automatic host detection, native PowerShell, global installation, uninstall/update redesign, release publication, and certification of every installer-recognized agent.

## Assumptions
The user wants a thin stable wrapper over Skills CLI rather than a new installer implementation. Agent choice stays explicit because host auto-detection can mutate the wrong directories.

## Open Questions
None blocking. Additional validated hosts can be added to the support matrix independently.

## Decision Status
Resolved blockers: none. Accepted assumptions: the wrapper remains project-scoped, requires one explicit agent identifier, delegates placement to Skills CLI, and keeps immutable/global workflows in advanced documentation. DEC-001 is accepted.
