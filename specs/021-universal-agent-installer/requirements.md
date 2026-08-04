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
  at: "2026-08-04T13:18:43Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "021-universal-agent-installer"
  artifact: "requirements.md"
  path: "specs/021-universal-agent-installer/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/021-universal-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/021-universal-agent-installer/decision-log.md"
  status: "review"
  owner: "Harness Maintainers"
  created_at: "2026-08-04"
  updated_at: "2026-08-04"
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
    - "DEC-002"
    - "DEC-003"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
  related_artifacts:
    - "specs/021-universal-agent-installer/branch-plan.md"
    - "specs/021-universal-agent-installer/decision-log.md"
    - "specs/021-universal-agent-installer/design.md"
    - "specs/021-universal-agent-installer/index.md"
    - "specs/021-universal-agent-installer/qa.md"
    - "specs/021-universal-agent-installer/tasks.md"
    - "specs/021-universal-agent-installer/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "review"
    - "universal-installer"
---

# Requirements

## Goal
Make project-scoped AI SDLC Harness installation portable across Windows, macOS, and Linux and configurable for any compatible agent host without weakening provenance, containment, or existing profiles.

## Problem Statement
The public bootstrap is POSIX-shell-only, the native installer imports Unix-only `fcntl`, and only fixed Codex and Claude Code roots are accepted. Windows and other Agent Skills-compatible hosts lack a supported native path.

## Scope
- Add a standard-library Python bootstrap.
- Add `agent-project` with explicit repository-relative `--skills-root`.
- Make installer locking portable.
- Preserve named profiles, module selection, immutable-source verification, TOON records, and transactional writes.
- Add cross-platform tests and canonical docs.

## Actors
- Contributors installing the harness.
- Agent-host users choosing a project-local skills root.
- Maintainers validating installer and release compatibility.

## Inputs
- Exact tag or 40-character revision.
- Clean source or reviewed remote.
- Consumer Git root.
- Named profile, or `agent-project` plus relative skills root.
- Optional modules and reviewed replacement authorization.

## Outputs
- Installed `SKILL.md` packages under the selected root.
- Portable install record, deterministic lock, and inventory.
- Explicit unsafe-path, collision, and lock diagnostics.

## Functional Requirements
- FR-001: Preserve `codex-project` and `claude-code-project` behavior.
- FR-002: `agent-project` shall require `--skills-root`.
- FR-003: Provide a Python 3.10+ bootstrap with immutable Git verification.
- FR-004: Support Unix and Windows mutation locks.
- FR-005: Reject absolute, drive, parent, metadata/Git-overlap, empty, and symlink-escaping targets.
- FR-006: Record and validate normalized profile, agent, target, revision, selection, paths, and digests.
- FR-007: Preserve modules, transactionality, collision review, and rollback.
- FR-008: Publish platform commands while retaining one primary install command in README, Home, and Start here.
- FR-009: Add native Windows, macOS, and Linux CI coverage.

## Non-Functional Requirements
- NFR-001: Use only Python standard library.
- NFR-002: Records remain deterministic and portable.
- NFR-003: Writes remain repository-contained.
- NFR-004: Never shell-interpolate user values.
- NFR-005: Existing records need no migration.
- NFR-006: Distinguish package compatibility from named-host conformance.

## Constraints
- Git and Python 3.10+ remain prerequisites.
- Generic support applies to hosts consuming Agent Skills directories with `SKILL.md`; it does not certify proprietary formats.
- Global installation stays out of scope.
- Generated catalogs remain generator-owned.

## Acceptance Criteria
- AC-001: Given either existing named profile, when its native fixture installs and validates, then the established target and record pass unchanged.
- AC-002: Given a clean Git consumer, when `python install.py agent-project --skills-root .agent/skills` runs, then skills install and the record validator exits zero.
- AC-003: Given a custom target, when records are written, then target paths use forward slashes and automatic target resolution validates them.
- AC-004: Given a missing or unsafe custom target, when installation starts, then it exits nonzero before any install record or managed skill is written.
- AC-005: Given the Windows lock adapter, when a repository lock is acquired and released, then the one-byte lock operations complete without `fcntl`.
- AC-006: Given the context-cache module and custom profile, when Python bootstrap installs it, then the opt-in skill and module selection validate.
- AC-007: Given the release candidate, when focused installer, docs, SDD, and native OS-matrix gates run, then every required gate exits successfully.
- AC-008: Given canonical public docs, when platform guidance is reviewed, then Linux/macOS and Windows commands are present and unnamed hosts are described only as package-compatible.

## Out of Scope
- Proprietary rule-format conversion.
- Per-user/global installation.
- Removing `install.sh`.
- Certifying unnamed agent model execution.

## Assumptions
- A-001: Compatible hosts can discover a user-selected project skills root.
- A-002: Git and Python 3.10+ are acceptable prerequisites.
- A-003: v4.4.0 is the additive release target if every gate passes.

## Open Questions
- No blocking questions remain. Additional named profiles require authoritative host docs and fixtures.

## Decision Status
- Resolved blockers: none.
- Accepted assumptions: A-001 through A-003.
- DEC-001 accepted: one safe configurable `agent-project` profile instead of guessed vendor paths.
- DEC-002 accepted: Python is the cross-platform bootstrap; shell remains compatible.
- DEC-003 accepted: claim Agent Skills package compatibility, not universal host certification.
