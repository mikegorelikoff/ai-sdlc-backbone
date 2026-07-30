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
  at: "2026-07-29T22:13:40Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "015-executable-skill-harness-v4"
  artifact: "decision-log.md"
  path: "specs/015-executable-skill-harness-v4/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-branching"
  flow_mode: "quick"
  state_file: "specs/015-executable-skill-harness-v4/_ai_sdlc/state.toon"
  decision_log: "specs/015-executable-skill-harness-v4/decision-log.md"
  status: "draft"
  owner: "Repository Maintainers"
  created_at: "2026-07-30"
  updated_at: "2026-07-30"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-branching"
    - "decision-log"
    - "draft"
    - "harness-v4"
---
# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-07-30 | accepted | Repository Maintainers | Use SDD quick-flow because the user-approved v4 plan is decision-complete | User plan plus research.md and branch-plan.md | Repeat the full 18-stage discovery cascade; use traceable quick-flow | requirements.md; design.md; tasks.md | RF-001 through RF-005; AC-001 through AC-012 |
| DEC-002 | 2026-07-30 | accepted | Harness Maintainers | Treat v2 manifests and semantic step documents as canonical and generate concise SKILL routers | Agent Skills progressive disclosure guidance and current router drift | Keep routers canonical; keep three coarse steps; canonical manifest plus generated router | skill manifests; step docs; SKILL.md; generator | FR-001; FR-002; AC-001; AC-002 |
| DEC-003 | 2026-07-30 | accepted | Runtime Maintainers | Journal every selected owning-skill step after Apply and require idempotency around side effects | Durable execution research and current runtime replay primitives | Journal writes only; journal terminal nodes only; journal every step | runtime contracts; workflow compiler; journals | FR-004; FR-005; AC-005; AC-006 |
| DEC-004 | 2026-07-30 | accepted | Context Maintainers | Compile context per step with deterministic lexical ranges, mandatory anchors, 100 percent critical recall, and 15 percent savings fallback | Context engineering research and existing context v3 benchmark | Embeddings; preload all sources; deterministic JIT with direct read | context pack v4; StepCard; context tests | FR-003; AC-003; AC-004; RF-003 |
| DEC-005 | 2026-07-30 | accepted | QA and Release Maintainers | Require deterministic evals for all 44 skills and a provider-neutral live representative suite before release | Harness engineering evidence and provider variability | Offline tests only; provider-specific tests; two-tier neutral protocol | eval CLI; scenario catalog; release receipt | FR-008; AC-011; AC-012; TC-011; TC-012 |
| DEC-006 | 2026-07-30 | accepted | Flow and Security Maintainers | Preserve Explore as strict zero-write and create durable run state only after fingerprinted Apply | Repository safety model and durable execution boundaries | Create draft runs during Explore; cache hidden state; Apply-only run creation | flow v3; runtime v2; zero-write tests | FR-006; AC-007; AC-008; RF-005 |
| DEC-007 | 2026-07-30 | accepted | Harness and Documentation Maintainers | Use canonical TOON as the only structured machine-data representation and enforce a repository-wide absence plus canonicalization gate | User hard-cut requirement, context-engineering determinism, and mixed-format drift risk | Retain alternate readers and emitters; allow legacy conversion inside runtime; strict TOON-only source and build outputs | shared codec; contracts; fixtures; CLIs; docs build; repository gate | FR-011; NFR-008; AC-010; AC-013 |
| DEC-008 | 2026-07-30 | accepted | Release Owner | Publish v4.0.0 from current deterministic evidence while provider-executed TC-012 certification remains pending and no provider-certification claim is made | Explicit instruction to complete, push, and create the 4.0.0 release; deterministic suite passed; offline provider-neutral protocol passed 6/6 | Block publication pending external execution; misrepresent offline execution as provider certification; publish with the limitation disclosed | validation.md; security-review.md; docs/reference/release-4.0.md | TC-012; AC-012; release verification |
