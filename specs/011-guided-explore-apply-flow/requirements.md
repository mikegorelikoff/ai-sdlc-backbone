---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "requirements.md"
  path: "specs/011-guided-explore-apply-flow/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/011-guided-explore-apply-flow/_ai_sdlc/state.toon"
  decision_log: "specs/011-guided-explore-apply-flow/decision-log.md"
  status: "approved"
  owner: "Repository Maintainers"
  created_at: "2026-07-26"
  updated_at: "2026-07-26"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "AC-009"
    - "AC-010"
    - "DEC-001"
    - "DEC-007"
    - "DEC-008"
    - "DEC-013"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
    - "NFR-008"
  related_artifacts:
    - "specs/011-guided-explore-apply-flow/branch-plan.md"
    - "specs/011-guided-explore-apply-flow/decision-log.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "approved"
---

# Requirements

## Goal
Implement `ai-sdlc-flow` as the recommended guided entrypoint: deterministic read-only Explore explains intent, feature, workspace, stage, rigor, roles, context evidence, planned writes, and blockers; explicit Apply revalidates and executes exactly one checkpoint. Existing direct skills remain an expert-compatible path.

## Problem Statement
Skill purpose and order are difficult to infer. Navigator can select recent state before recognizing new-refinement feedback; compressed context is hard to audit and can cost more after rereads; unsafe directory behavior can create unintended structures; rationale-first review can anchor humans and hide bugs or unreadable code.

## Scope
Create `skills/ai-sdlc-flow/` with contract, helper, reference, and tests; make navigator intent-first; add canonical shared-runtime DecisionCard, fingerprint, workspace, role/rigor, and context-economics logic and synchronize installed mirrors; enforce spec-first review ordering; update module and managed-skill inventories, generated catalogs, onboarding/reference docs, install/compatibility checks, and deterministic fixtures.

## Actors
Contributor explores, verifies, and explicitly applies. Expert contributor may invoke a direct skill. Maintainers own routes, schemas, guards, fixtures, catalogs, and compatibility. Engineering reviewers and QA record independent findings before comparison context. Product, BA, security, operations, and other roles activate only from documented request evidence.

## Inputs
Natural-language intent; optional explicit feature; repository root and branch; refinement and implementation state/index files; project-context freshness metadata; policy and rigor configuration; source hashes; context benchmark results; and checked-in fixtures. Binding upstream sources are `specs-refiniment/011-guided-explore-apply-flow/delivery-spec.md`, `qa-readiness.md`, `delivery-handoff-review.md`, and `decision-log.md`.

## Outputs
Explore emits deterministic Markdown and TOON DecisionCards with classification, confidence/reason, feature/workspace/stage/skill, context freshness, evidence hashes, rigor, activated roles, token/anchor economics, blockers, planned writes, next checkpoint, and route fingerprint. Apply emits one action result, validation evidence, authorized state changes, and the next Explore checkpoint.

## Functional Requirements
- **FR-001:** Classify intent before feature state. New/refinement/feedback cannot fall back to the latest completed feature; material ambiguity blocks.
- **FR-002:** Explore performs zero durable writes and emits a complete DecisionCard in Markdown and TOON.
- **FR-003:** SHA-256 fingerprint covers repository identity, normalized intent, feature, workspace, stage, skill, rigor, role evidence, config/policy version, state hash, and selected source hashes.
- **FR-004:** Apply requires and recomputes the fingerprint, rejects drift, and invokes at most one allow-listed stage or task.
- **FR-005:** Refinement routes only to `specs-refiniment/<feature>` and implementation only to `specs/<feature>`; reject overrides, escapes, symlinks, and divergent roots.
- **FR-006:** Activate minimum stage roles and add cross-functional roles only from documented evidence; expose triggers and avoid unrelated process questions.
- **FR-007:** Recommend quick/full from size, risk, ambiguity, and stage; explain it; honor safe overrides and transparently upgrade or block unsafe ones.
- **FR-008:** Use packed context only with 100% critical-anchor recall and at least 15% net savings including rereads; otherwise use direct reading and show the calculation.
- **FR-009:** Review requirements, tests, and diff and record independent findings before exposing AI rationale or prior verdicts.
- **FR-010:** Preserve direct skill invocations, flags, state/index formats, and installed-runtime behavior; docs recommend flow and describe direct skills as advanced.

## Non-Functional Requirements
- **NFR-001 Determinism:** identical fixtures produce semantically stable cards and fingerprints.
- **NFR-002 Safety:** Explore writes nothing; Apply fails before mutation on ambiguity, drift, unsafe roots, symlinks, policy conflict, or unsupported action.
- **NFR-003 Explainability:** routing, role, rigor, and context choices cite evidence and rejected alternatives.
- **NFR-004 Integrity:** accepted packs retain 100% configured critical anchors.
- **NFR-005 Efficiency:** accepted packs save at least 15% including rereads.
- **NFR-006 Compatibility:** existing focused, runtime, install-smoke, catalog, and docs checks remain green.
- **NFR-007 Readability:** cards and findings are understandable without compressed-source decoding.
- **NFR-008 Locality:** acceptance uses checked-in fixtures without network, secrets, customer data, or live telemetry.

## Constraints
Preserve the physical `specs-refiniment` name. Do not add a public CLI, global-install fix, compatibility symlinks, remote service, or automatic multi-stage Apply. Shared source remains canonical in `skills/_shared/` where installed mirrors exist. Explore never implies Apply approval, and flow cannot broaden user, sandbox, policy, or owning-skill authority.

## Acceptance Criteria
- **AC-001:** The original feedback as new work selects feature 011 and the correct refinement/SDD checkpoint, never completed feature 010 because of recency.
- **AC-002:** Before/after filesystem snapshots prove Explore makes zero durable changes; Markdown and TOON contain the complete field set and equivalent meaning.
- **AC-003:** Unchanged accepted Apply executes one action; drift in intent, state, config, sources, workspace, stage, roles, or rigor rejects with zero mutation.
- **AC-004:** Canonical refinement/implementation fixtures route correctly; overrides, `..`, symlink roots, and divergent roots fail with actionable diagnostics.
- **AC-005:** Code-only intent adds no customer-feedback questions; auth, migration, release, or product-policy signals activate only matching roles and cite evidence.
- **AC-006:** Bounded low-risk work recommends quick; cross-cutting/ambiguous work recommends full; safe overrides work and policy upgrades are explicit.
- **AC-007:** 100% anchors plus ≥15% net savings selects packed; anchor loss, 14.99%, or negative reread economics selects direct and reports all values.
- **AC-008:** A blind pass detects one seeded P0/P1 behavior bug and one readability violation before rationale, while a clean fixture has no unexpected P0/P1.
- **AC-009:** Direct skill, navigator, runtime, and project-scoped install smoke remain compatible; no global-install or symlink migration appears.
- **AC-010:** Flow, navigator, path, context, review, compatibility, docs, catalog, full SDD, and refinement gates pass; generated entrypoint surfaces list flow appropriately.

## Out of Scope
Global installation repair; public standalone CLI; remote services; live telemetry or feedback collection; multi-stage Apply; root collapse/rename; sandbox changes; publication/release; and unrelated product-role workflows.

## Assumptions
Repository-local Python and existing shared helpers remain the runtime. SHA-256 detects drift but provides no authority. Existing Markdown/TOON and metadata stay compatible. Fixture-only evidence is accepted. `main` is the remote base because no `dev` exists; DEC-013 records the exception.

## Open Questions
No product or delivery question blocks implementation planning. T001/T002 must confirm exact helper boundaries and generated-doc commands from repository conventions; these engineering choices cannot change FR-001–FR-010 or AC-001–AC-010.

## Decision Status
Approved for implementation planning. All blocking decisions are resolved: upstream DEC-001–DEC-007 are binding, and DEC-008–DEC-013 select implementation boundaries, fingerprinting, workspace guards, fixture evaluation, review ordering, and the canonical branch base. Contract changes require a new accepted decision before code.
