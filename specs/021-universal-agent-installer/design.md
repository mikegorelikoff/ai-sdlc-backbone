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
  at: "2026-08-04T13:17:51Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "021-universal-agent-installer"
  artifact: "design.md"
  path: "specs/021-universal-agent-installer/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/021-universal-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/021-universal-agent-installer/decision-log.md"
  status: "review"
  owner: "Harness Maintainers"
  created_at: "2026-08-04"
  updated_at: "2026-08-04"
  trace_ids: []
  related_artifacts:
    - "specs/021-universal-agent-installer/decision-log.md"
    - "specs/021-universal-agent-installer/index.md"
    - "specs/021-universal-agent-installer/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "review"
    - "universal-installer"
---

# Design

## Overview
Extend the source-owned installer. A top-level Python bootstrap resolves an immutable source and delegates to the same native implementation as `install.sh`.

## Architecture
- `install.py`: cross-platform bootstrap and Git verification.
- `install.sh`: POSIX compatibility and option forwarding.
- `ai_sdlc_install.py`: transactional authority and dynamic profile resolver.
- `ai_sdlc_install_record.py`: installed-layout validator.

## Components
- Bootstrap parser and source resolver.
- Target normalizer and containment guard.
- Portable `fcntl`/`msvcrt` lock.
- Existing staging, digests, transaction, TOON records, tests, and CI.

## Interfaces and Contracts
- `python install.py PROFILE [--skills-root PATH] [--module MODULE]`.
- `agent-project` requires `--skills-root`; named profiles reject it.
- Internal installer adds the same option.
- Existing environment overrides remain compatible.

## Data Model
Static profiles retain fixed agent/target. `agent-project` records agent `agent-skills` and a normalized runtime target. Record v3 and lock v2 shapes are unchanged; stored paths use `/`.

## Error Handling
Fail closed for unsafe options/targets, dirty source, invalid tag/revision, collisions, symlinks, or concurrency. Propagate delegated exit codes and restore transaction backups.

## Security Considerations
Use argv subprocesses only. Reject POSIX/Windows absolute or drive paths, `..`, `.git`, `.ai-sdlc`, NUL, root-equivalent targets, symlink ancestors, and resolved escapes.

## Observability
Print selected profile, exact revision, count, normalized target, record, and lock. Diagnostics expose contracts, not repository content.

## Risks and Tradeoffs
- Configurable roots cannot guarantee host discovery; docs make this explicit.
- OS locks differ; isolate helpers and run native CI.
- Two bootstraps add small duplication but share one installation authority.

## Validation Strategy
Unit-test normalization, profiles, locks, and validator. Integration-test Python/shell bootstraps, modules, and custom roots. Run native OS matrix plus docs and SDD gates.

## Migration Notes
No migration. Existing profiles update in place; generic users choose `agent-project` and a project-relative skills root.
