---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "decision-log.md"
  path: "specs/011-guided-explore-apply-flow/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-branching"
  flow_mode: "full"
  state_file: "specs/011-guided-explore-apply-flow/_ai_sdlc/state.toon"
  decision_log: "specs/011-guided-explore-apply-flow/decision-log.md"
  status: "draft"
  owner: "Repository Maintainers"
  created_at: "2026-07-26"
  updated_at: "2026-07-26"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-branching"
    - "decision-log"
    - "draft"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-013 | 2026-07-26 | accepted | Repository Maintainers | Base `feature/011-guided-explore-apply-flow` on refreshed `main` because no local or remote `dev` exists and `origin/HEAD` is `main`. | `git branch -r`, `git symbolic-ref refs/remotes/origin/HEAD`, and successful `git pull --ff-only` | Stop all work; invent dev; use canonical main | branch-plan.md, requirements.md | branch `feature/011-guided-explore-apply-flow` |
| DEC-001 | 2026-07-26 | accepted | Product | Adopt `ai-sdlc-flow` as recommended Explore→Apply entrypoint; keep direct skills advanced. | Upstream DEC-001 | Navigator only; public CLI | requirements.md, design.md | FR-001, FR-010, AC-001, AC-009 |
| DEC-002 | 2026-07-26 | accepted | Product | Explore is read-only and Apply performs one revalidated checkpoint. | Upstream DEC-002 | Implicit or multi-stage apply | requirements.md, test-cases.md | FR-002–FR-004, AC-002–AC-003 |
| DEC-003 | 2026-07-26 | accepted | Repository Maintainers | Preserve tool-owned roots; reject overrides, escapes, symlinks, and divergence. | Upstream DEC-003 | Collapse roots; links | design.md, test-cases.md | FR-005, AC-004 |
| DEC-004 | 2026-07-26 | accepted | Product | Activate cross-functional roles only from documented evidence. | Upstream DEC-004 | All roles always | design.md | FR-006, AC-005 |
| DEC-005 | 2026-07-26 | accepted | Repository Maintainers | Accept packs only at 100% anchor recall and at least 15% net savings including rereads. | Upstream DEC-005 | Always pack; raw-only threshold | design.md, test-cases.md | FR-008, AC-007 |
| DEC-006 | 2026-07-26 | accepted | Engineering | Record spec-first independent findings before rationale or prior verdicts. | Upstream DEC-006 | Rationale-first review | design.md, qa.md | FR-009, AC-008 |
| DEC-007 | 2026-07-26 | accepted | Product | Exclude global install, public CLI, remote service, and publication. | Upstream DEC-007 | Expand operations scope | requirements.md, tasks.md | Out of Scope, AC-009 |
| DEC-008 | 2026-07-26 | accepted | Repository Maintainers | Implement a pure decision core plus allow-listed action adapter in `ai-sdlc-flow`; reuse navigator/runtime contracts. | Repository skill architecture | Embed writes in routing; duplicate skills | design.md, tasks.md | FR-001–FR-004, T001–T004 |
| DEC-009 | 2026-07-26 | accepted | Repository Maintainers | Canonicalize DecisionCard fingerprint inputs and hash with SHA-256; the hash grants no authority. | Determinism requirement | Timestamp or session token | design.md, test-cases.md | FR-003, AC-003 |
| DEC-010 | 2026-07-26 | accepted | Repository Maintainers | Put workspace and symlink validation in canonical shared runtime; callers cannot choose output roots. | Two-root safety | Caller paths; symlink compatibility | design.md, test-cases.md | FR-005, AC-004 |
| DEC-011 | 2026-07-26 | accepted | QA | Use checked-in fixtures for routing, roles, rigor, economics, review, and compatibility. | Fixture-only boundary | Live telemetry | test-cases.md, qa.md | NFR-008, AC-001–AC-010 |
| DEC-012 | 2026-07-26 | accepted | Engineering | Make spec-first evidence capture an explicit phase before comparison context. | Anchoring feedback | Single rationale-first prompt | design.md, qa.md | FR-009, AC-008 |
