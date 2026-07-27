---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "branch-plan.md"
  path: "specs/011-guided-explore-apply-flow/branch-plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-branching"
  flow_mode: "full"
  state_file: "specs/011-guided-explore-apply-flow/_ai_sdlc/state.toon"
  decision_log: "specs/011-guided-explore-apply-flow/decision-log.md"
  status: "approved"
  owner: "Repository Maintainers"
  created_at: "2026-07-26"
  updated_at: "2026-07-26"
  trace_ids:
    - "DEC-013"
  related_artifacts:
    - "specs/011-guided-explore-apply-flow/decision-log.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-branching"
    - "branch-plan"
    - "approved"
---

# branch-plan.md

## Implementation
Change size is large and the canonical SDD is `specs/011-guided-explore-apply-flow`. The repository has no local or remote `dev`; `origin/HEAD` points to `main`, which was refreshed with `git pull --ff-only` and reported up to date. The active branch is `feature/011-guided-explore-apply-flow`. Existing dirty paths are the directly related refinement package and its indexes; no unrelated changes were carried.

## Testing
Before SDD or code writes, verify `git branch --show-current` equals `feature/011-guided-explore-apply-flow`, the upstream refinement full gate remains 18/18, and the implementation state records branching complete. Later validation and commit-prep must confirm branch/spec alignment and keep all task changes on this single feature branch.

## Documentation
Record the `main` base exception in implementation DEC-013 because the required `dev` branch does not exist and the remote default is `main`. Do not publish or push the branch without explicit user authorization. The next phase is SDD artifact creation, not product-code mutation.
