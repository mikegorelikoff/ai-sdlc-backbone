---
type: "ai-sdlc.decision-log"
title: "Decision Log"
description: "Auditable decisions, evidence, alternatives, and traceability."
tags:
  - "ai-sdlc"
  - "decision"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-27T19:27:56Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "014-one-line-agent-installer"
  artifact: "decision-log.md"
  path: "specs/014-one-line-agent-installer/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/014-one-line-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/014-one-line-agent-installer/decision-log.md"
  status: "review"
  owner: "Repository Maintainers"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "decision-log"
    - "review"
    - "installer"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-07-27 | accepted | Repository Maintainers | Add one project-scoped shell wrapper parameterized by explicit agent target | User feedback says installation should be one shell line for different agents; current docs expose multiple implementation flags | wrapper with explicit agent; automatic host detection; raw CLI only | install.sh; tests/test_install_sh.py; README.md; docs/how-to/install.md; specs/014-one-line-agent-installer/* | AC-001–AC-006; TC-001–TC-006 |
| DEC-002 | 2026-07-27 | accepted | Repository Maintainers | Use `feature/014-one-line-agent-installer` based on synchronized commit `32077c5` | The repository has no `dev` branch; `main` exactly matched `origin/main` before branching and all dirty paths belong to Feature 014 | block for a nonexistent dev branch; commit directly on main; create the aligned feature branch from synchronized main | branch-plan.md; specs/spec-registry.md; commit-readiness.md | git status --short --branch; git branch -vv; AC-001–AC-006 |
