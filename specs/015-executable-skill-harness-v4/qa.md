---
type: "ai-sdlc.qa-plan"
title: "QA Plan"
description: "Acceptance, regression, risk, and manual validation plan."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-30T10:01:32Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "015-executable-skill-harness-v4"
  artifact: "qa.md"
  path: "specs/015-executable-skill-harness-v4/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/015-executable-skill-harness-v4/_ai_sdlc/state.toon"
  decision_log: "specs/015-executable-skill-harness-v4/decision-log.md"
  status: "validated"
  owner: "QA and Repository Maintainers"
  created_at: "2026-07-30"
  updated_at: "2026-07-30"
  trace_ids:
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-011"
    - "TC-012"
    - "TC-013"
  related_artifacts:
    - "specs/015-executable-skill-harness-v4/branch-plan.md"
    - "specs/015-executable-skill-harness-v4/decision-log.md"
    - "specs/015-executable-skill-harness-v4/design.md"
    - "specs/015-executable-skill-harness-v4/index.md"
    - "specs/015-executable-skill-harness-v4/plan.md"
    - "specs/015-executable-skill-harness-v4/requirements.md"
    - "specs/015-executable-skill-harness-v4/research.md"
    - "specs/015-executable-skill-harness-v4/tasks.md"
    - "specs/015-executable-skill-harness-v4/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "validated"
    - "harness-v4"
---

# QA

## Change Summary
Replace coarse prose-only skill progression with executable semantic DAGs, per-step deterministic context, durable Apply journals, generated routers, and two-tier evaluations across the 44-skill product surface.

## Acceptance Scenarios
- QA-001: Actor: skill author. Setup: any repository skill. Action: run v4 manifest and generated-router checks. Expected: semantic DAG passes or an exact source and projection error is reported. Evidence: TC-001 and TC-002 automation. Risk: high because drift can route agents to incomplete instructions.
- QA-002: Actor: agent host. Setup: a ready step with relevant and irrelevant repository files. Action: compile context and StepCard. Expected: mandatory anchors are present with byte-stable fingerprint or direct reading blocks execution. Evidence: TC-003 and TC-004 automation. Risk: high because missing context can create confident but wrong mutations.
- QA-003: Actor: harness operator. Setup: approved Apply with an interruptible side-effect step. Action: execute, interrupt, and resume. Expected: every step follows planned, started, terminal, evidence, result order; completed work is reused; the side effect occurs once. Evidence: TC-005 and TC-006 automation. Risk: critical because duplicate or out-of-order effects can damage systems.
- QA-004: Actor: harness operator. Setup: an Explore card and mutable repository evidence. Action: Explore, then optionally change evidence and Apply. Expected: Explore writes nothing; stale Apply is rejected before run creation. Evidence: TC-007 and TC-008 automation. Risk: high because hidden state or stale intent weakens authorization.
- QA-005: Actor: release maintainer. Setup: complete repository and representative live scenarios. Action: run deterministic and live protocol suites. Expected: 44-skill offline receipt is clean and live routing, compliance, evidence, recovery, and context scores are recorded. Evidence: TC-011 automation plus TC-012 release receipt. Risk: medium because model compliance varies outside deterministic contracts.
- QA-006: Actor: repository maintainer. Setup: complete source tree and strict documentation output. Action: run TOON-only absence, decode, and canonicalization gates. Expected: no alternate machine-format artifact or identifier exists and every repository-owned TOON artifact has deterministic canonical bytes. Evidence: TC-013. Risk: critical because a second representation reintroduces parser drift and unstable fingerprints.

## Regression Targets
- Existing Agent Skills discovery and concise `SKILL.md` frontmatter remain valid.
- Existing skill-owned domain rules, artifact routing, state transitions, sandbox boundaries, and installation layouts remain represented after decomposition.
- Flow intent and role routing remain deterministic while Explore stays read-only.
- Runtime append-only per-task journaling, protocol order, replay, idempotency, and result projection remain portable and standard-library only.
- Context v3 behavior that is still semantically valid is re-expressed in v4 exact-range, authority, skipped-source, recall, and direct-read fields without hidden cache writes.
- Generated docs, module inventory, install smoke, and compatibility checks continue to cover exactly 44 skills.
- Every CLI and machine artifact continues to use the shared canonical TOON codec; no compatibility reader or alternate output mode returns.

## Risk Notes
- Critical: shallow mechanical steps could satisfy schema while weakening procedure quality; semantic lint and representative review are required.
- Critical: stale context or fingerprints could authorize the wrong work; insufficient context and drift fail before Apply writes.
- Critical: replay could duplicate or reorder side effects; stable idempotency keys, strict event phases, and receipt reuse are mandatory.
- Critical: a second machine representation could reintroduce dual-parser drift; source and strict-build absence gates fail closed.
- High: a hard cut could leave installed hosts on older schemas; installed-layout smoke and exact schema diagnostics are release gates.
- Medium: deterministic lexical retrieval may miss paraphrases; direct-read fallback and live scenarios cover the gap.
- Medium: live eval results are environment-sensitive; receipts must record host, provider, model, scenario version, and timestamp.

## Validation Commands
- Complete per-file suite: `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_test_suite.py --format toon`; current evidence is 95/95 files passed with receipt fingerprint `4d7881a8cdb44d4f8cbbb7e995d8384f8d07968a4bdf0d892bbfb30ef0e47d9f`.
- All semantic graphs and generated routers: `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_skill_graph.py --check --skills-root skills`; current inventory is 44 skills and 221 semantic nodes.
- Deterministic eval: `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_skill_eval.py --mode deterministic --skills-root skills --format toon` run twice and compared byte-for-byte; current receipt fingerprint is `1d47e6bbd5259b874ee9600040bf1aa716684fd0cdb2740b9bcaba910943f0d2`.
- Live protocol: `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_skill_eval.py --mode live-protocol --skills-root skills --format toon`; current offline protocol evidence is 6/6 scenarios with receipt fingerprint `39589f99fbc80b108649b07f02dbc43a2fe6dadc5744508af88aed1dd1541ac2`.
- Focused contracts: shared runtime, context compiler, flow, workflow, runtime, adapter, handoff, compatibility, modules, package, security, and install-smoke suites.
- Documentation and repository gates: catalog check, docs validator, docs unit suite, compatibility, installed-layout smoke, strict site build, rendered-link validation, repository TOON-only scan, and `git diff --check`.
- No command is marked passed until current output or a deterministic receipt exists; authorized provider execution remains release-owned.

## Manual Checks
- Review one simple utility skill, one artifact-profile skill, SDD, flow, runtime, approvals, workflow, and host adapter; confirm each semantic step has a distinct entry condition, action, gate, evidence, exit, and recovery boundary.
- Inspect generated `SKILL.md` routers for progressive disclosure and no duplicated canonical procedure prose.
- Inspect one sufficient and one direct-read context report; confirm selected and skipped sources, authority, recall, savings, and reasons are understandable without source-code knowledge.
- Interrupt and resume a disposable local run; compare strict journal order and idempotency receipt.
- Inspect strict documentation output for canonical TOON examples and absence of alternate machine representations.
- In release environment, execute the representative live protocol and record provider-neutral scores. Owner: Release maintainers. Expected: no missing evidence or skipped recovery explanation.

## Signoff
Deterministic implementation validation is complete: all 95 test files, all 44 semantic skill graphs, compatibility, native installed-layout, package, security, documentation, context-pack, replay, and TOON canonicality gates pass with current evidence. The provider-neutral live protocol passes 6/6 offline scenarios. Under DEC-008, publication may proceed with provider-executed TC-012 certification explicitly pending; no provider-certification claim is made until an authorized receipt meets the published threshold and records host, provider, model, scenario version, and timestamp.
