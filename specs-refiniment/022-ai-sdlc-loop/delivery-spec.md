---
type: "ai-sdlc.delivery-spec"
title: "Delivery Specification"
description: "Structured implementation and cross-functional delivery contract."
tags:
  - "ai-sdlc"
  - "requirements"
  - "delivery"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-17T10:57:37Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "delivery-spec.md"
  path: "specs-refiniment/022-ai-sdlc-loop/delivery-spec.md"
  workspace: "refinement"
  skill: "ai-sdlc-delivery-spec-synthesis"
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
    - "BR-002"
    - "BR-003"
    - "BR-004"
    - "BR-005"
    - "BR-006"
    - "BR-007"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "REQ-001"
    - "REQ-002"
    - "REQ-003"
    - "REQ-004"
    - "REQ-005"
    - "REQ-006"
    - "REQ-007"
    - "REQ-008"
    - "REQ-009"
    - "TASK-001"
    - "TASK-004"
    - "TASK-005"
    - "TASK-006"
    - "TASK-007"
    - "TASK-008"
    - "TASK-009"
    - "WF-001"
    - "WF-002"
    - "WF-003"
    - "WF-004"
    - "WF-005"
  related_artifacts:
    - "specs-refiniment/022-ai-sdlc-loop/backlog-gap-review.md"
    - "specs-refiniment/022-ai-sdlc-loop/backlog.md"
    - "specs-refiniment/022-ai-sdlc-loop/business-context.md"
    - "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
    - "specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md"
    - "specs-refiniment/022-ai-sdlc-loop/discovery.md"
    - "specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md"
    - "specs-refiniment/022-ai-sdlc-loop/index.md"
    - "specs-refiniment/022-ai-sdlc-loop/prfaq.md"
    - "specs-refiniment/022-ai-sdlc-loop/release-slicing.md"
    - "specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md"
    - "specs-refiniment/022-ai-sdlc-loop/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-delivery-spec-synthesis"
    - "delivery-spec"
    - "approved"
---

# delivery-spec.md

## Feature Summary
AI SDLC Loop is a public Apache-2.0 repository and minimal AI SDLC product exposing one ai-sdlc skill. The deliverable supports a bounded change through Specify, approval-bound Implement, deterministic Verify, and approval-bound commit, while producing artifacts that can be promoted into AI SDLC Harness and pinned in Harness as products/ai-sdlc-loop.

## Actors and Stakeholders
Contributors operate the workflow; reviewers grant exact-fingerprint authority; Loop maintainers own code, package, documentation, CI, compatibility inventory, and releases; Harness maintainers own promotion and submodule integration; QA and security reviewers own positive, negative, drift, recovery, path, secret, and approval-boundary evidence. Approval cannot be inferred from any non-reviewer action or repository state.

## Scope and Boundaries
MVP includes STORY-001 through STORY-009. Supported profiles are source-verified as codex-project, claude-code-project, and agent-project with a required safe relative --skills-root. Fixed destinations are .agents/skills/ai-sdlc and .claude/skills/ai-sdlc; the custom profile installs under its supplied root. Out of scope are other Harness skills, full refinement orchestration, telemetry, deployment, implicit approval, and unapproved commits.

## Workflows and Failure Paths
Install resolves a supported profile, validates containment and collision rules, writes exactly one skill, records provenance, and verifies the result. Specify persists the request contract and fingerprint. Implement accepts only a matching current approval and mutates only approved scope. Verify runs relevant deterministic checks and persists evidence and a change fingerprint. Commit accepts only matching passing evidence approval. Drift, interruption, unsafe paths, overlap, failed checks, incompatibility, or release mismatch fail closed.

## Requirements and Business Rules
REQ-001 through REQ-009 and BR-001 through BR-007 are mandatory P0 launch contracts. Approval receipts bind action, feature, artifact fingerprint, decision, and timestamp; any content change invalidates downstream authority. Install and workflow operations preserve unrelated files. Verification evidence records command, working directory, exit status, and stable output summary. Promotion accepts only the supported Loop subset and rejects unknown incompatible versions without partial conversion.

## Data, Integrations, and Non-Functional Requirements
Canonical Loop state is local Markdown plus TOON under a feature workspace, with deterministic SHA-256 fingerprints over normalized approved content and relevant Git state. Records cover specification, lifecycle stage, approvals, validation evidence, and promotion provenance. Integrations are Python 3 standard library, POSIX or PowerShell bootstrap, local filesystem, Git, user-approved test commands, GitHub, and Harness fixtures. No runtime network, telemetry, secret collection, or dependency install is required by the skill.

## Dependencies, Risks, and Constraints
Installer behavior depends on current Harness profile contracts in install.py and related fixtures. The artifact subset depends on Harness-compatible metadata and trace identifiers. Git mutation depends on a repository and explicit user approval. Public repository creation and push are external writes authorized by the user, while each product workflow commit remains separately gated. Risks are host drift, approval replay, path escape, dirty-work damage, nondeterministic evidence, remote bootstrap compromise, and promotion loss.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-005 are accepted. Source inspection resolved the supported profile set to codex-project, claude-code-project, and agent-project --skills-root. Owner: maintainer. Impact: installer interface and fixtures. Resolution: encode this exact inventory and fail CI on drift. The compatible schema version and first v0.x tag remain implementation and release choices; they must be explicit, versioned, fixture-backed, and cannot alter accepted scope. No delivery-spec blocker remains.

## Success Measures
All three profiles install and verify exactly one skill. Every approval negative case leaves protected state unchanged. Approved implementation changes only declared paths and retains unrelated work. Verification evidence is repeatable and blocks commit on failure. Promotion round trips every supported field. The public repository exposes license, README, security guidance, tests, and passing CI, and Harness resolves the pinned submodule commit. Documentation commands are tested fixtures, not prose-only claims.

## Source Coverage
Consumed specs-refiniment/022-ai-sdlc-loop/index.md, specs-refiniment/022-ai-sdlc-loop/discovery.md, specs-refiniment/022-ai-sdlc-loop/prfaq.md, specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md, specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md, specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md, specs-refiniment/022-ai-sdlc-loop/backlog-gap-review.md, specs-refiniment/022-ai-sdlc-loop/backlog.md, specs-refiniment/022-ai-sdlc-loop/user-stories.md, specs-refiniment/022-ai-sdlc-loop/release-slicing.md, specs-refiniment/022-ai-sdlc-loop/business-context.md, specs-refiniment/022-ai-sdlc-loop/decision-log.md, specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon, install.py, docs/reference/supported-environments.md, and docs/reference/compatibility.md.

## Requirement Detail
| Requirement ID | Actor/System | Requirement | Source | Priority | Acceptance Ref |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | Installer | Install exactly one public ai-sdlc skill | STORY-001, STORY-002, BR-001 | P0 | AC-001, SAC-001 through SAC-003 |
| REQ-002 | ai-sdlc skill | Implement Specify, Implement, and Verify as one bounded workflow | STORY-003 through STORY-006, BR-002 | P0 | AC-002, AC-004 |
| REQ-003 | Reviewer and runtime | Require current fingerprint approval before code mutation | STORY-004, BR-003 | P0 | AC-003, SAC-005, SAC-006 |
| REQ-004 | Runtime | Restrict mutation to approved paths and preserve unrelated work | STORY-005, BR-007 | P0 | SAC-007 |
| REQ-005 | Runtime and reviewer | Persist relevant check evidence and require current approval before commit | STORY-006, STORY-007, BR-004, BR-005 | P0 | AC-004, AC-005 |
| REQ-006 | Installer | Support codex-project, claude-code-project, and safe agent-project roots | STORY-001, STORY-002, DEC-003 | P0 | AC-001 |
| REQ-007 | Loop and Harness | Promote supported artifact content without information loss | STORY-008, BR-006 | P0 | AC-006, SAC-011 |
| REQ-008 | Repository | Publish under Apache-2.0 with CI, docs, security, and version evidence | STORY-009, TASK-006, TASK-007, TASK-009 | P0 | SAC-012 |
| REQ-009 | Harness | Pin the validated public repository at products/ai-sdlc-loop | STORY-009, DEC-001 | P0 | SAC-012 |

## Workflow Detail
| Workflow ID | Trigger | Actor | Steps | End State | Exceptions | Requirement Ref |
| --- | --- | --- | --- | --- | --- | --- |
| WF-001 | Install request | Contributor | Resolve profile; validate safe target; install one skill; record provenance; verify | Verified one-skill installation | Unsupported profile, unsafe root, collision, interruption, or drift stops safely | REQ-001, REQ-006 |
| WF-002 | Bounded change request | Contributor and reviewer | Normalize request; persist spec; fingerprint; review; approve or reject | Approved current specification or stopped workflow | Missing or stale approval blocks mutation | REQ-002, REQ-003 |
| WF-003 | Current specification approved | Contributor and runtime | Validate receipt; snapshot scope; apply approved change; preserve unrelated state | Scoped implemented change | Path escape, overlap, drift, or command denial stops mutation | REQ-004 |
| WF-004 | Scoped change exists | Runtime and reviewer | Select relevant checks; request command approval if needed; execute; record evidence; fingerprint; approve or reject commit | Approved verified change or failed evidence | Failed/unavailable check or stale approval blocks commit | REQ-005 |
| WF-005 | Passing release candidate | Maintainers | Run promotion fixture; publish repository and release; add and pin Harness submodule | Reproducible public product integration | Schema loss, CI failure, missing license, or pin mismatch blocks launch | REQ-007 through REQ-009 |

## Business Rule Detail
| Rule ID | Rule | Applies To | Source | Failure Behavior | Decision Ref |
| --- | --- | --- | --- | --- | --- |
| BR-001 | Exactly one ai-sdlc skill is public and installed | Package and installer | REQ-001 | Verification fails on missing or extra skill | DEC-002 |
| BR-002 | A persisted fingerprinted specification precedes mutation | Specify and Implement | REQ-002 | Implement remains unavailable | DEC-002 |
| BR-003 | Mutation requires explicit approval matching current spec fingerprint | Implement | REQ-003 | No code mutation occurs | DEC-004 |
| BR-004 | Relevant deterministic checks and evidence precede commit readiness | Verify | REQ-005 | Readiness is denied | DEC-004 |
| BR-005 | Commit requires explicit approval matching current verified fingerprint | Commit | REQ-005 | Index and history remain unchanged | DEC-004 |
| BR-006 | Promotion preserves every supported field and version | Promotion | REQ-007 | No partial output is written | DEC-005 |
| BR-007 | All invalid, unsafe, stale, interrupted, and failed states stop closed | Entire product | REQ-001 through REQ-009 | Preserve unrelated state and provide recovery | DEC-003, DEC-004 |

## User Story Traceability
EPIC-001 maps STORY-001 and STORY-002 to REQ-001 and REQ-006. EPIC-002 maps STORY-003 through STORY-007 to REQ-002 through REQ-005. EPIC-003 maps STORY-008 and STORY-009 to REQ-007 through REQ-009. TASK-001 through TASK-004 provide core implementation, TASK-005 provides QA fixtures, TASK-006 documentation, TASK-007 security review, TASK-008 promotion and submodule integration, and TASK-009 public release evidence. All stories remain P0 and MVP.

## Acceptance Traceability
AC-001 covers profile inventory, one-skill install, drift, interruption, and recovery through SAC-001 to SAC-003. AC-002 covers spec schema and fingerprint through SAC-004. AC-003 covers missing, rejected, stale, mismatched, and matching mutation approvals through SAC-005 and SAC-006. AC-004 covers scoped preservation and deterministic checks through SAC-007 and SAC-008. AC-005 covers commit denial and approval through SAC-009 and SAC-010. AC-006 covers valid and invalid promotion plus release pinning through SAC-011 and SAC-012.

## QA and Operational Notes
QA must use isolated repositories and profile roots; compare filesystem, Git index, and history before and after denied actions; freeze time and normalize output where needed; cover POSIX and Windows bootstrap logic; and validate recovery after interruption. Security tests cover traversal, symlinks, malicious names, approval replay, changed fingerprints, command injection, secret-like output, unsafe Git state, remote-source pinning, and partial writes. Operators need install verification, doctor-style diagnostics, update/recovery guidance, compatibility version, and escalation to Harness.

## Handoff Risks
No scope or permission blocker remains. HR-001: schema design could become either too weak for promotion or too broad for minimal support; owner developer and Harness maintainer; mitigation is a versioned minimum subset plus round-trip fixtures. HR-002: generic command execution could exceed approval intent; owner security and developer; mitigation is explicit command preview and host approval. HR-003: remote one-line installation increases supply-chain exposure; owner maintainer; mitigation is version-pinned URLs, transparent source, CI, and documented local alternative. HR-004: submodule integration can drift; owner Harness maintainer; mitigation is pinned commit verification.
