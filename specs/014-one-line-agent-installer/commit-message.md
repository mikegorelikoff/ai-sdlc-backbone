---
type: "ai-sdlc.commit-message"
title: "Commit Message"
description: "Validated Conventional Commit message for the one-line agent installer."
tags:
  - "ai-sdlc"
  - "commit"
  - "traceability"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-27"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "014-one-line-agent-installer"
  artifact: "commit-message.md"
  path: "specs/014-one-line-agent-installer/commit-message.md"
  workspace: "implementation"
  skill: "ai-sdlc-conventional-commit"
  flow_mode: "quick"
  state_file: "specs/014-one-line-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/014-one-line-agent-installer/decision-log.md"
  status: "approved"
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
    - "T001"
    - "T002"
    - "T003"
    - "T004"
    - "T005"
    - "DEC-001"
    - "DEC-002"
  related_artifacts:
    - "specs/014-one-line-agent-installer/commit-readiness.md"
    - "specs/014-one-line-agent-installer/validation.md"
  validation:
    - "Conventional Commit validator passed with required traceability"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-conventional-commit"
    - "commit-message"
    - "approved"
---

# Commit Message

````text
feat(install): add one-line agent installer

Spec: specs/014-one-line-agent-installer
Task: T001, T002, T003, T004, T005

Business context:
Make first-time harness installation one memorable command while preserving an
explicit agent boundary and the existing audited installation path.

Implementation details:
- Add a POSIX shell wrapper that pins Skills CLI, disables telemetry, and
  installs every harness skill project-scoped for one explicit agent.
- Add offline coverage for direct and stdin execution, alternate agents,
  overrides, invalid input, missing prerequisites, and delegated failures.
- Lead the README and install guide with the one-line command while retaining
  immutable revision and global-install guidance.

Mermaid diagram:
```mermaid
flowchart LR
    User["User names agent"] --> Script["install.sh"]
    Script --> CLI["Pinned Skills CLI"]
    CLI --> Project["Project-scoped harness skills"]
```

How to test:
1. Run the installer unittest and confirm all seven offline scenarios pass.
2. Run the documentation validator and documentation tests.
3. Verify the Feature 014 validation receipt and SDD gates are current.

Validation:
- python3 -m unittest tests/test_install_sh.py -> passed; 7 tests
- python3 docs/scripts/validate_docs.py -> passed; 186 pages and 44 skills
- python3 -m pytest -q docs/tests -> passed; 44 tests
- Feature 014 validation receipt -> current; 9 commands; 0 failures
- git diff --check -> passed
````
