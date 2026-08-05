---
type: "ai-sdlc.branch-plan"
title: "Branch Plan"
description: "Branch alignment, delivery boundary, and handoff plan."
tags:
  - "ai-sdlc"
  - "git"
  - "planning"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-04T13:18:19Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "021-universal-agent-installer"
  artifact: "branch-plan.md"
  path: "specs/021-universal-agent-installer/branch-plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-branching"
  flow_mode: "quick"
  state_file: "specs/021-universal-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/021-universal-agent-installer/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-04"
  updated_at: "2026-08-05"
  trace_ids: []
  related_artifacts:
    - "specs/021-universal-agent-installer/decision-log.md"
    - "specs/021-universal-agent-installer/design.md"
    - "specs/021-universal-agent-installer/index.md"
    - "specs/021-universal-agent-installer/qa.md"
    - "specs/021-universal-agent-installer/requirements.md"
    - "specs/021-universal-agent-installer/tasks.md"
    - "specs/021-universal-agent-installer/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-branching"
    - "branch-plan"
    - "approved"
    - "universal-installer"
---

# branch-plan.md

## Implementation
- Use branch `feature/021-universal-agent-installer` from refreshed `main`.
- Implement the portable bootstrap, dynamic profile, path guards, record validation, and OS locking without changing existing named-profile targets.
- Use follow-up branch `feature/021-universal-agent-update-command` from the
  validated installer commit for the pre-release update interface.
- Recover update profile and selection only from verified installed provenance.

## Testing
- Add focused unit/integration tests for named and configurable profiles, unsafe targets, modules, bootstraps, and portable locking.
- Add Python and shell install-to-update coverage plus local-drift refusal.
- Run native OS matrix plus repository SDD/docs gates before release.

## Documentation
- Update canonical install and environment references, then link from entry pages without duplicating the contract.
- Record material documentation and release decisions in project logs and changelog.
