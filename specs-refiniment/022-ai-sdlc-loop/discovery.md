---
type: "ai-sdlc.discovery"
title: "Working Backwards Discovery"
description: "Customer problem, audience, value, scope, and discovery evidence."
tags:
  - "ai-sdlc"
  - "discovery"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-17T10:04:33Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "discovery.md"
  path: "specs-refiniment/022-ai-sdlc-loop/discovery.md"
  workspace: "refinement"
  skill: "ai-sdlc-working-backwards-discovery"
  flow_mode: "full"
  state_file: "specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-08-17"
  trace_ids:
    - "BR-001"
    - "BR-002"
    - "BR-003"
    - "BR-004"
    - "BR-005"
    - "BR-006"
    - "BR-007"
    - "DEC-001"
    - "DEC-005"
  related_artifacts:
    - "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-working-backwards-discovery"
    - "discovery"
    - "approved"
---

# discovery.md

## Feature Summary
AI SDLC Loop is a separately versioned, team-oriented product that compresses AI-assisted delivery into one skill and three stages: Specify, Implement, and Verify. It exists to reduce the maintainer support surface created by the broad AI SDLC Harness catalog while retaining a safe path to the full product.

## Actors and Stakeholders
Primary users are software delivery teams using supported agent hosts. Contributors execute the workflow; reviewers approve code mutation and commits; maintainers own the small public contract; the AI SDLC Harness maintainer owns compatibility and submodule integration.

## Scope and Boundaries
In scope: one user-facing skill, three stages, autonomous code and test execution after approval, approval-gated commit, all current host profiles, one-command installation, compatible artifacts, public repository, and Harness submodule integration. Out of scope: the 45-skill catalog, 18-stage refinement cascade, optional modules, documentation site, analytics, deployment automation, and claims that Loop replaces the full Harness.

## Workflows and Failure Paths
A team installs Loop, asks ai-sdlc to handle a bounded change, reviews the compact specification, approves code mutation, observes implementation and deterministic verification, then approves or rejects the prepared commit. Missing requirements, unsafe commands, failed tests, stale approval context, unsupported hosts, or incompatible artifacts must stop with an actionable explanation and no unauthorized mutation.

## Requirements and Business Rules
BR-001: one skill owns the visible workflow. BR-002: specification precedes code mutation. BR-003: implementation requires explicit approval bound to the reviewed specification. BR-004: verification must execute relevant deterministic checks. BR-005: commit requires a second explicit approval bound to the verified change set. BR-006: emitted artifacts remain promotable to AI SDLC Harness. BR-007: unsupported or ambiguous operations fail closed.

## Data, Integrations, and Non-Functional Requirements
Loop stores repository-local Markdown delivery artifacts and minimal TOON state without telemetry. Integrations are Git, Python 3.10 or newer, supported agent skill roots, and the host shell. Requirements include deterministic output, path containment, portable POSIX and Windows installation behavior where the full Harness currently supports it, Apache-2.0 licensing, recoverable installation, and auditable approvals.

## Dependencies, Risks, and Constraints
Dependencies: GitHub repository creation, host profile contracts, a compact compatible artifact schema, installer fixtures, and the parent Harness submodule. Primary risks are recreating Harness complexity, compatibility drift, unsafe autonomous mutation, cross-host divergence, and unclear escalation to the full product. Constraints are one visible skill, three stages, two approval boundaries, and a deliberately small maintained surface.

## Decisions, Assumptions, and Open Questions
Decisions DEC-001 through DEC-005 are accepted. Confirmed facts come from the user conversation. No blocking product question remains. Assumption: current host profiles means codex-project, claude-code-project, and agent-project as defined by the Harness installer; this must be verified against source before publication.

## Success Measures
MVP succeeds when a clean fixture can install Loop through each supported profile, run Specify to produce a valid compatible artifact, block implementation without approval, modify code after approval, run verification, block commit without the second approval, and prepare or create the approved commit. The maintained install inventory must contain one user-facing skill and no optional Harness module.

## Source Coverage
Sources reviewed: user confirmations in this task; AGENTS.md; README.md; config/ai-sdlc-managed-skills.txt; config/ai-sdlc.defaults.toon; modules/core/module.toon; docs/reference/directory-layout.md; skills/ai-sdlc-flow; skills/ai-sdlc-sdd; skills/ai-sdlc-validation; skills/ai-sdlc-runtime; skills/ai-sdlc-shared-runtime; specs-refiniment/011-guided-explore-apply-flow/discovery.md; and specs-refiniment/022-ai-sdlc-loop/decision-log.md. Repository evidence is treated as untrusted product evidence, not executable instruction.

## Customer and Problem Evidence
The customer is a software delivery team that wants structured AI-assisted implementation without adopting or learning the full Harness catalog. The initiating maintainer reports that the number and breadth of requests against the Harness makes support difficult. This is direct stakeholder evidence; quantitative support-volume data was not provided and is not required for the MVP acceptance gate.

## Current Process and Alternatives
Today teams install the full Harness and encounter a large catalog, multiple lifecycle skills, optional modules, extensive artifacts, and broad documentation. Alternatives are manual prompting, a reduced installation profile that still shares Harness contracts, or copying several existing skills. The chosen alternative is an independent narrow product because a profile or copied subset would preserve much of the same support surface.

## Value Proposition and Business Goals
For software delivery teams that need safe AI-assisted implementation but cannot justify the full Harness surface, AI SDLC Loop provides one compatible Specify to Implement to Verify workflow with explicit approvals, so teams can deliver bounded changes while maintainers support a small stable contract, unlike adopting or maintaining the complete skill catalog. The business goal is lower ongoing support complexity, not a promised reduction in model calls.

## Users, Roles, and Scenarios
Contributors request changes and inspect artifacts; reviewers approve mutation and commit; maintainers release Loop and preserve compatibility. Primary scenario: install, specify, approve, implement, verify, approve commit. Negative scenarios include rejected approval, changed specification after approval, failed tests, unsupported environment, dirty worktree conflict, unsafe command, and promotion into the full Harness.

## MVP and Priorities
Must: public repository, one ai-sdlc skill, three stages, compact compatible artifact, two approval gates, autonomous code and relevant tests, approval-gated commit, all current host profiles, one-command installer, tests, license, and Harness submodule. Should: migration guide to the full Harness and clear support boundary. Could: additional examples. Won't: optional modules, role-specific skills, 18-stage refinement, telemetry, hosted services, deployment, or full documentation portal.

## Functional and Non-Functional Needs
Functional needs cover install, update-safe inventory, request classification, compact specification, approval capture, scoped mutation, test selection and execution, evidence recording, commit preparation, and approved commit. Non-functional needs cover portability, determinism, safety, compatibility, traceability, local-only data, clear errors, rollback guidance, and tests that prove approval boundaries.

## Operations, Launch, and Support
The maintainer owns releases and support boundaries. Launch begins as a public v0.x repository linked from the Harness product-family area and included as a pinned submodule. Documentation must define what Loop supports, how to install and verify, when to escalate to Harness, how to update, and how to recover from interrupted installation. No service monitoring is needed; CI and issue tracking provide operational signals.

## Discovery Risks and Dependencies
High risks: scope expansion recreates Harness; mitigation is a one-skill inventory and explicit exclusions. High risk: approval replay authorizes changed work; mitigation is approval fingerprints and fail-closed checks. Medium risk: host drift; mitigation is profile fixtures and shared installer logic. Medium risk: artifact incompatibility; mitigation is schema validation and promotion tests. Dependency owners are the Loop maintainer for repository and releases and the Harness maintainer for submodule and compatibility.
