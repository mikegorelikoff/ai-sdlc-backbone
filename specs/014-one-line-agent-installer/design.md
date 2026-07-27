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
  at: "2026-07-27T19:32:15Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "014-one-line-agent-installer"
  artifact: "design.md"
  path: "specs/014-one-line-agent-installer/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/014-one-line-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/014-one-line-agent-installer/decision-log.md"
  status: "validated"
  owner: "Repository Maintainers"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids: []
  related_artifacts:
    - "specs/014-one-line-agent-installer/decision-log.md"
    - "specs/014-one-line-agent-installer/index.md"
    - "specs/014-one-line-agent-installer/plan.md"
    - "specs/014-one-line-agent-installer/qa.md"
    - "specs/014-one-line-agent-installer/requirements.md"
    - "specs/014-one-line-agent-installer/tasks.md"
    - "specs/014-one-line-agent-installer/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "validated"
    - "installer"
---

# Design

## Overview
A root `install.sh` becomes the public bootstrap interface and delegates file placement to the pinned Skills CLI.

## Architecture
The shell validates its argument, resolves safe environment defaults, checks `npx`, exports `DISABLE_TELEMETRY=1`, and replaces itself with the pinned `npx skills add` process so exit status and signals propagate unchanged.

## Components
`install.sh` owns argument validation and delegation. `tests/test_install_sh.py` provides an offline fake-npx harness. README and install docs present the wrapper first.

## Interfaces and Contracts
Public forms are `curl -fsSL URL/install.sh | sh -s -- AGENT` and `./install.sh AGENT`. Supported options are `-h` and `--help`; exactly one agent argument is required.

## Data Model
No persistent data model changes. Environment inputs are `AI_SDLC_SOURCE` and `AI_SDLC_SKILLS_CLI_VERSION`; defaults are the GitHub slug and `1.5.19`.

## Error Handling
Missing npx returns 127 with a prerequisite message. Invalid arity returns 64 with usage. The delegated installer status is returned directly.

## Security Considerations
No eval, downloads, temporary files, or automatic host discovery inside the wrapper. Values are individually quoted. Curl-pipe trust remains explicit in advanced verification guidance.

## Observability
The wrapper prints the selected agent and source before delegation; Skills CLI owns detailed progress output.

## Risks and Tradeoffs
A mutable main-branch curl URL is easier but less reproducible. The quick path optimizes evaluation; the existing pinned revision procedure remains the audited alternative.

## Validation Strategy
Run `sh -n`, offline fake-npx tests for defaults, alternate agents, overrides, invalid input, and missing npx, then documentation validation and SDD gates.

## Migration Notes
Existing raw `npx skills add` commands continue to work. Users may replace them with the one-line wrapper; automation requiring immutable sources should keep the pinned flow.
