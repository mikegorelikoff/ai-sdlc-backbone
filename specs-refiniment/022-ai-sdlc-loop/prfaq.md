---
type: "ai-sdlc.prfaq"
title: "PRFAQ Package"
description: "Working-backwards press release, FAQ, and business requirements."
tags:
  - "ai-sdlc"
  - "discovery"
  - "requirements"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-17T10:05:41Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "prfaq.md"
  path: "specs-refiniment/022-ai-sdlc-loop/prfaq.md"
  workspace: "refinement"
  skill: "ai-sdlc-prfaq-package-synthesis"
  flow_mode: "full"
  state_file: "specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-08-17"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "BR-001"
    - "BR-007"
    - "DEC-001"
    - "DEC-005"
    - "REQ-001"
    - "REQ-002"
    - "REQ-003"
    - "REQ-004"
    - "REQ-005"
    - "REQ-006"
    - "REQ-007"
    - "REQ-008"
    - "REQ-009"
  related_artifacts:
    - "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
    - "specs-refiniment/022-ai-sdlc-loop/discovery.md"
    - "specs-refiniment/022-ai-sdlc-loop/index.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-prfaq-package-synthesis"
    - "prfaq"
    - "approved"
---

# prfaq.md

## Feature Summary
AI SDLC Loop is a public, separately versioned product for teams that need safe AI-assisted implementation without the full AI SDLC Harness surface. One ai-sdlc skill owns Specify, Implement, and Verify; two fingerprinted approvals guard code mutation and commit.

## Actors and Stakeholders
Team contributors request and inspect work; reviewers approve mutation and commit; maintainers support Loop releases and compatibility; the AI SDLC Harness maintainer owns the pinned submodule and promotion path.

## Scope and Boundaries
MVP includes all current host profiles, one-command install, one skill, compact Harness-compatible artifacts, autonomous scoped code changes, deterministic verification, approval-gated commit, public CI, and submodule integration. It excludes role catalogs, optional modules, 18-stage refinement, telemetry, hosted services, deployment, and a full documentation portal.

## Workflows and Failure Paths
Install, Specify, approve mutation, Implement, Verify, review evidence, approve commit. Invalid or stale approval fingerprints, unsafe paths or commands, dirty-worktree overlap, incompatible artifacts, failed tests, and unsupported hosts stop without unauthorized mutation and return recovery guidance.

## Requirements and Business Rules
BR-001 through BR-007 apply. AC-001: every supported profile installs and verifies one skill. AC-002: Specify produces a schema-valid compatible artifact. AC-003: implementation is blocked before approval and proceeds after a matching approval. AC-004: relevant checks run and evidence is recorded. AC-005: commit is blocked before a second approval and succeeds only for the verified fingerprint. AC-006: a Loop artifact can be promoted into Harness without information loss in the supported subset.

## Data, Integrations, and Non-Functional Requirements
Repository-local Markdown and TOON are authoritative; no telemetry or service dependency is introduced. Integrations are Git, Python 3.10 or newer, POSIX and Windows host entrypoints already supported by Harness, and host-specific project skill roots. Output and ordering must be deterministic, paths contained, installation recoverable, and approvals auditable.

## Dependencies, Risks, and Constraints
Dependencies are a new GitHub repository, installer/profile fixtures, artifact schema validation, approval fingerprints, and parent-repository submodule support. The main risk is scope creep recreating Harness; additional risks are host drift, compatibility drift, approval replay, and unclear escalation. The fixed constraints are one visible skill, three stages, and two approval boundaries.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-005 are accepted. Open item OQ-001: verify that current host profiles are codex-project, claude-code-project, and agent-project. Owner: maintainer. Impact: advertised installation compatibility and related fixtures. Resolution: inspect the current installer profile parser and tests before publishing commands; block launch if the inventory differs. No other blocking product question remains.

## Success Measures
A clean fixture must install each profile, verify exactly one visible skill, produce a compatible spec, prove both negative and positive approval paths, execute a code change and relevant tests, record evidence, and create only an explicitly approved commit. The v0.x release and pinned Harness submodule must be reproducible from published commands.

## Source Coverage
Consumed sources: specs-refiniment/022-ai-sdlc-loop/discovery.md; specs-refiniment/022-ai-sdlc-loop/decision-log.md; specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon; specs-refiniment/022-ai-sdlc-loop/index.md; AGENTS.md; README.md; current installer profiles; and the referenced Loop-related skill contracts.

## Press Release
AI SDLC Loop gives software delivery teams a small, approval-controlled path from a request to verified code. Teams install one skill, review a compact specification, approve implementation, inspect deterministic verification evidence, and approve the resulting commit. Loop keeps its artifacts compatible with AI SDLC Harness, so teams can escalate complex work without starting over. The first release supports every current Harness project host profile while deliberately excluding the broad skill catalog and optional modules.

## Customer FAQ
Who is it for? Teams wanting structured AI-assisted coding with a small maintained surface. What changes on day one? One install and one ai-sdlc entrypoint replace choosing among many skills. Does it change code? Yes, only after specification approval. Does it commit? Only after verification and a second explicit approval. Can work move to Harness? Yes, the compact artifact preserves the supported compatibility fields. What is missing? Advanced refinement, role-specific workflows, optional modules, deployment, and hosted services.

## Internal FAQ
Why invest? To separate the simple team workflow from the support burden of the full Harness. What is MVP? One skill, three stages, two approvals, all current hosts, compatible artifacts, installer, tests, public repository, and pinned submodule. Who owns support? The Loop maintainer owns its narrow contract; Harness owns only compatibility and submodule integration. How is release readiness proven? Cross-profile install fixtures, approval-boundary tests, artifact promotion tests, and deterministic end-to-end validation. When should users move to Harness? When work needs multi-role discovery, extensive governance, security or QA specialization, optional modules, or deeper lifecycle orchestration.

## Business Requirements
REQ-001 provide one public ai-sdlc skill. REQ-002 implement Specify, Implement, and Verify in one bounded workflow. REQ-003 require approval tied to the current specification before mutation. REQ-004 independently select and run relevant deterministic checks. REQ-005 require approval tied to the verified change set before commit. REQ-006 install and verify through codex-project, claude-code-project, and agent-project profiles. REQ-007 emit a compact artifact accepted by the defined Harness promotion path. REQ-008 publish as Apache-2.0 with local-only data behavior and no telemetry. REQ-009 integrate at products/ai-sdlc-loop as a pinned Git submodule.

## Launch Risks
Scope creep is the go/no-go risk: fail launch if the installed inventory exceeds one user-facing skill or imports optional Harness modules. Fail launch on any approval bypass, approval replay after fingerprint drift, unsupported advertised host, non-reproducible installer, artifact promotion loss, failing tests, undocumented recovery path, or unpinned submodule. Quantitative support-volume improvement is not claimed in v0.x; issue categories and change frequency provide later operational evidence.
