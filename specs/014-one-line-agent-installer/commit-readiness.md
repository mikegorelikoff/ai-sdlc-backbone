---
type: "ai-sdlc.commit-readiness"
title: "Commit Readiness"
description: "Staging, validation, traceability, and residual-risk evidence."
tags:
  - "ai-sdlc"
  - "commit"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-27"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "014-one-line-agent-installer"
  artifact: "commit-readiness.md"
  path: "specs/014-one-line-agent-installer/commit-readiness.md"
  workspace: "implementation"
  skill: "ai-sdlc-commit-prep"
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
    - "DEC-002"
  related_artifacts:
    - "specs/014-one-line-agent-installer/branch-plan.md"
    - "specs/014-one-line-agent-installer/validation.md"
    - "specs/014-one-line-agent-installer/_ai_sdlc/validation-receipt.json"
  validation:
    - "check_commit_ready.py --quick-flow: passed before staging"
    - "ai-sdlc-validation-receipt/v1: current; 9 commands; 0 failures"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-commit-prep"
    - "commit-readiness"
    - "validated"
---

# Commit Readiness

## Result

Feature 014 is ready for one focused commit on
`feature/014-one-line-agent-installer`.

## Staging

- Include `install.sh` and `tests/test_install_sh.py` as the installer contract
  and its offline regression coverage.
- Include README and install-guide changes because they expose the new public
  command.
- Include Feature 014 and generated implementation-index artifacts because
  they provide the accepted decision, branch, task, and validation trace.
- Exclude unrelated paths: none are present.

## Validation

- The current machine receipt records nine commands and zero failures.
- Seven installer tests, 44 documentation tests, the 186-page documentation
  validator, SDD gates, installed-package smoke, and diff hygiene pass.
- The commit-readiness preflight passes with the complete related worktree.

## Residual Risk

The public raw-GitHub URL cannot be live-smoked until this branch is merged to
`main`; remote installation remains covered by the existing publication CI.
