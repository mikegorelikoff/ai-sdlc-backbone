---
type: "ai-sdlc.design"
title: "Design"
description: "Technical design, interfaces, architecture, and migration decisions."
tags:
  - "ai-sdlc"
  - "sdd"
  - "design"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-17T11:55:09Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "design.md"
  path: "specs/022-ai-sdlc-loop/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-08-17"
  trace_ids:
    - "TC-001"
    - "TC-024"
  related_artifacts:
    - "specs/022-ai-sdlc-loop/branch-plan.md"
    - "specs/022-ai-sdlc-loop/decision-log.md"
    - "specs/022-ai-sdlc-loop/index.md"
    - "specs/022-ai-sdlc-loop/plan.md"
    - "specs/022-ai-sdlc-loop/qa.md"
    - "specs/022-ai-sdlc-loop/requirements.md"
    - "specs/022-ai-sdlc-loop/security-review.md"
    - "specs/022-ai-sdlc-loop/tasks.md"
    - "specs/022-ai-sdlc-loop/test-cases.md"
    - "specs/022-ai-sdlc-loop/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "approved"
    - "ai-sdlc-loop"
---

# Design

## Overview
AI SDLC Loop is a separate, public, Python-standard-library repository that installs five stage-oriented entrypoints, eleven focused delivery-control owners, and one internal shared runtime. `ai-sdlc-loop-orchestrate` routes Specify → Implement → Verify → Commit; stage skills invoke requirements review, approvals, branching, test-case, QA, validation, review, security, commit-quality, and release-readiness owners as needed while the runtime owns deterministic TOON state, fingerprints, approvals, evidence, commit gating, step selection, and Harness promotion. The parent Harness consumes a pinned gitlink at `products/ai-sdlc-loop`.

## Architecture
The repository has five layers: portable bootstrap (`install.py` and `install.sh`), five routed stage entrypoints, eleven delivery-control owners with canonical v2 step manifests, an internal shared Python runtime, versioned TOON contracts, and unittest/CI validation. Runtime authority is local: project state lives below `.ai-sdlc-loop/<feature>/`; Git remains source-change authority; explicit receipts authorize Implement eligibility and commit. Network access is absent at runtime.

## Components
- Installer: resolves `codex-project`, `claude-code-project`, or `agent-project --skills-root`, validates containment, copies the exact seventeen-member package transactionally, and writes a TOON digest record plus reusable verifier.
- Stage skills: `ai-sdlc-loop-orchestrate` routes the lifecycle; `ai-sdlc-loop-specify`, `ai-sdlc-loop-implement`, `ai-sdlc-loop-verify`, and `ai-sdlc-loop-commit` own the bounded stage flow.
- Delivery-control skills: approvals sandbox, branching, requirements review, test cases, QA planning, validation, code review, security testing, commit prep, Conventional Commit validation, and release readiness use bounded scripts, references, and v2 step graphs. Compact Loop-native reviewers emit typed TOON without the Harness refinement cascade.
- CLI: `specify`, `approve`, `implement-check`, `verify`, `commit`, `promote`, and `status`.
- Contracts: canonical TOON schema/version constants, fingerprints, approval receipts, evidence, install records, and promotion payloads.
- Tests/CI: isolated Git fixtures, path/security tests, install tests, workflow tests, promotion tests, docs/parser checks, and Linux/macOS/Windows jobs.

## Interfaces and Contracts
Install interfaces are `python3 install.py codex-project`, `python3 install.py claude-code-project`, and `python3 install.py agent-project --skills-root PATH`; verification is a separate `python3 install.py verify ...` action. Workflow commands accept explicit `--project-root` and `--feature`; Specify also accepts request and repeatable allowed paths. Approval commands require action, decision, reviewer, and current fingerprint. Verify accepts repeatable argv-safe command strings, records results, and produces a verified fingerprint. Commit requires a matching approved commit receipt and creates one traceable commit. Promote accepts valid `ai-sdlc-loop/v1` state and atomically emits a Harness-compatible artifact.

## Data Model
Canonical TOON uses UTF-8, sorted mapping keys, stable scalar quoting, and SHA-256 over canonical encoding. `spec.toon` contains schema, feature, normalized request, allowed paths, trace IDs, and fingerprint. `approvals/<action>.toon` contains schema, action, decision, reviewer, subject fingerprint, and timestamp. `evidence.toon` contains spec fingerprint, change fingerprint, ordered command records, redacted summaries, readiness, and verified fingerprint. `state.toon` references stage, current fingerprints, receipts, and evidence. Promoted `.toon` output preserves feature, request, paths, status, fingerprints, trace IDs, approvals, commands, and evidence under a Harness-consumable versioned envelope.

## Error Handling
Fail closed before mutation for invalid feature names, unsafe/escaping/symlink paths, malformed or unsupported TOON, missing/rejected/stale/mismatched approvals, dirty out-of-scope changes, failed/missing/timed-out commands, evidence drift, or incompatible promotion targets. Atomic temporary-file replacement prevents partial state. Commit denial must leave HEAD and index unchanged. Errors identify the failed contract and remediation without implying approval.

## Security Considerations
Resolve and contain every project/state/install path; reject absolute custom roots, traversal, metadata overlap, NUL, and symlink escape. Invoke subprocesses without a shell. Bound captured output and timeouts. Redact token, password, secret, authorization, and private-key-like values before persistence. Preserve unrelated tracked, staged, unstaged, and untracked work. Receipts are capability records scoped to an action and exact fingerprint, never reusable after drift.

## Observability
`status` reports feature, stage, current fingerprints, approval validity, command outcomes, and readiness as TOON. Every state transition writes deterministic TOON. Verify records command argv, cwd, exit/timeout status, redacted bounded output, and hashes. Commit messages include feature and verified fingerprint trailers. No telemetry or hosted dependency is used.

## Risks and Tradeoffs
A small fixed skill graph reduces support surface without collapsing ownership and does not promise fewer model calls. Generic agents may differ in skill discovery, so only the installation filesystem contract is claimed. Approval receipts prove explicit recorded authority, not reviewer identity cryptographically. Commands are intentionally explicit rather than inferred. Python stdlib maximizes portability but requires a small vendored TOON codec and schema validation. The parent submodule adds release coordination but gives exact immutable identity.

## Validation Strategy
Implement the accepted TC-001 through TC-024 suite. Locally run unittest discovery, compile checks, docs/parser checks, security scans, promotion fixtures, Git invariants, and shell syntax. CI repeats on Linux, macOS, and Windows. Before parent integration, validate public visibility and immutable commit identity. Then run the complete Harness AGENTS.md docs/build/render/diff sequence and SDD, security, code-review, and validation workflows.

## Migration Notes
This is additive. No existing Harness skill or public path moves. Consumers opt into the namespaced AI SDLC Loop package. Promotion writes new artifacts rather than rewriting existing Harness state. The parent adds one submodule and product-family documentation entry; removal is a normal gitlink/repository-reference rollback.
