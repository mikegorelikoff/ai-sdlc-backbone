---
type: "ai-sdlc.validation"
title: "Validation Evidence"
description: "Focused validation outcomes for the universal Agent Skills installer."
tags:
  - "ai-sdlc"
  - "validation"
status: "stable"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "021-universal-agent-installer"
  artifact: "validation.md"
  path: "specs/021-universal-agent-installer/validation.md"
  workspace: "implementation"
  skill: "ai-sdlc-validation"
  flow_mode: "quick"
  state_file: "specs/021-universal-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/021-universal-agent-installer/decision-log.md"
  status: "validated"
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
    - "TC-001"
    - "TC-002"
    - "TC-004"
    - "TC-006"
    - "TC-007"
  related_artifacts:
    - "specs/021-universal-agent-installer/_ai_sdlc/validation-plan.toon"
    - "specs/021-universal-agent-installer/_ai_sdlc/validation-receipt.toon"
    - "specs/021-universal-agent-installer/security-review.md"
    - "specs/021-universal-agent-installer/requirements.md"
    - "specs/021-universal-agent-installer/test-cases.md"
  validation:
    - "ai-sdlc-validation-receipt/v1: 14 current commands; 0 failures"
    - "Python 3.11 portable installer tests: 20 passed"
    - "custom, Codex, and Claude installed-layout smokes: passed"
    - "documentation source, strict build, rendered links, SDD, compatibility, and diff gates: passed"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-validation"
    - "validation"
    - "validated"
---

# Validation Evidence

## Scope

Validate the portable Python bootstrap, configurable Agent Skills project
root, preserved Codex and Claude profiles, native Windows lock adapter, safe
path and remote handling, dynamic install records, installed runtime root
discovery, and the public cross-platform installation contract.

## Results

- PASS: the canonical argv-only receipt records 14 current commands and zero
  failures.
- PASS: all 20 portable installer tests pass on Python 3.11, including the
  simulated Windows lock adapter, unsafe/case-variant paths, symlink escape,
  credential URL non-echo, bootstrap, module, rollback, and named-profile
  regressions.
- PASS: `agent-project` at `.agent/skills`, `codex-project`, and
  `claude-code-project` each pass the complete native installed-layout smoke.
- PASS: the full shared-runtime regression suite, generated skill graph,
  compatibility, SDD plan links and structure, and diff hygiene.
- PASS: generated catalog, source documentation validation, 47 documentation
  tests, strict MkDocs build, and rendered-link validation for 207 HTML pages
  and 5,557 local targets.
- PASS: security review has no open findings after adding case-insensitive
  protected-root rejection and credential-bearing remote rejection.

## Residual Risk

Local macOS validation simulates the Windows lock API but cannot reproduce
native Windows filesystem semantics. The pull-request matrix on Ubuntu 24.04,
macOS 15, and Windows 2025 is required before publishing the release tag.
The generic profile certifies safe package placement for Agent Skills-compatible
hosts; it does not certify discovery or model behavior for every agent product.
