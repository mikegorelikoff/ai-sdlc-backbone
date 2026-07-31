---
type: "ai-sdlc.commit-message"
title: "Commit Message"
description: "Validated Conventional Commit message for the executable harness v4 release."
tags:
  - "ai-sdlc"
  - "commit"
  - "traceability"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-30"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "015-executable-skill-harness-v4"
  artifact: "commit-message.md"
  path: "specs/015-executable-skill-harness-v4/commit-message.md"
  workspace: "implementation"
  skill: "ai-sdlc-conventional-commit"
  flow_mode: "full"
  state_file: "specs/015-executable-skill-harness-v4/_ai_sdlc/state.toon"
  decision_log: "specs/015-executable-skill-harness-v4/decision-log.md"
  status: "approved"
  owner: "Repository Maintainers"
  created_at: "2026-07-30"
  updated_at: "2026-07-30"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "AC-009"
    - "AC-010"
    - "AC-011"
    - "AC-012"
    - "AC-013"
    - "DEC-007"
    - "DEC-008"
    - "DEC-009"
    - "T001"
    - "T002"
    - "T003"
    - "T004"
    - "T005"
    - "T006"
    - "T007"
    - "T008"
    - "T009"
    - "T010"
    - "T011"
  related_artifacts:
    - "specs/015-executable-skill-harness-v4/commit-readiness.md"
    - "specs/015-executable-skill-harness-v4/validation.md"
  validation:
    - "conventional commit validator passed with full traceability"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-conventional-commit"
    - "commit-message"
    - "approved"
    - "harness-v4"
---

# Commit Message

````text
fix(install): enforce TOON-only native installation

Spec: specs/015-executable-skill-harness-v4
Task: T011
Decision: DEC-009

Business context:
The first tagged v4 installation proved that the external installer generated a non-TOON lock, violating the release's hard machine-boundary requirement.

Implementation details:
- Replace the external consumer path with a Harness-owned installer that binds a clean Git revision, validates the managed inventory, rejects links and non-TOON artifacts, stages and rehashes every skill, and rolls back caught partial-application failures.
- Add portable install-record v2 plus a deterministic content-addressed TOON lock and an installed validator that recomputes every managed digest.
- Narrow validated installation to project-scoped Codex, pin the primary command to immutable v4.0.1, and document v4.0.0 as superseded without moving its tag.
- Add native installer unit and installed-layout smoke coverage, update CI and generated catalogs, and keep every repository machine boundary TOON-only.

Mermaid diagram:
```mermaid
flowchart LR
    Tag["Immutable v4.0.1"] --> Stage["Stage and hash 44 skills"]
    Stage --> Install["Serialized project install"]
    Install --> Lock["TOON record and digest lock"]
    Lock --> Verify["Recompute installed bytes"]
```

How to test:
1. Verify the current Feature 015 receipt and inspect the 17 command results.
2. Run the complete 95-file suite and native installed-layout smoke.
3. Build documentation strictly and validate all rendered local targets.
4. Run exact compatibility and a fresh tagged native installation.

Validation:
- python3 skills/ai-sdlc-validation/scripts/run_validation.py --root . --plan specs/015-executable-skill-harness-v4/_ai_sdlc/validation-plan.toon --output specs/015-executable-skill-harness-v4/_ai_sdlc/validation-receipt.toon --verify --quick-flow -> current; 17/17 commands passed
- python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_test_suite.py --format toon -> passed; 95/95 files
- python3 skills/ai-sdlc-shared-runtime/tests/install_smoke.py --mode native --source . --agent codex --quick-flow -> passed
- python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_compatibility.py --git-executable /usr/bin/git --format toon -> compatible
- mkdocs build --strict and python3 docs/scripts/validate_rendered.py site -> passed; 201 HTML pages and 5,423 local targets
- git diff --check -> passed
````
