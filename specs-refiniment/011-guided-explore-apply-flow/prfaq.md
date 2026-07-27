---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "prfaq.md"
  path: "specs-refiniment/011-guided-explore-apply-flow/prfaq.md"
  workspace: "refinement"
  skill: "ai-sdlc-prfaq-package-synthesis"
  flow_mode: "full"
  state_file: "specs-refiniment/011-guided-explore-apply-flow/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/011-guided-explore-apply-flow/decision-log.md"
  status: "approved"
  owner: "Product and Repository Maintainers"
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
    - "BR-001"
    - "BR-002"
    - "BR-003"
    - "DEC-001"
    - "DEC-007"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
  related_artifacts:
    - "specs-refiniment/011-guided-explore-apply-flow/decision-log.md"
    - "specs-refiniment/011-guided-explore-apply-flow/discovery.md"
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
`ai-sdlc-flow` is the recommended guided entrypoint over existing lifecycle skills. A read-only, intent-first Explore emits a verifiable decision card; Apply revalidates its fingerprint and executes exactly one bounded checkpoint. Direct skills remain supported for expert use.

## Actors and Stakeholders
Contributors explore and accept routes; repository maintainers own policy, paths, fixtures, docs, and compatibility; reviewers and QA independently validate outcomes. Product, BA, security, operations, and other roles participate only when explicit request evidence activates their concerns.

## Scope and Boundaries
Scope includes the meta-skill contract, intent-first routing, decision cards, single-step Apply, two-root safety, adaptive roles and rigor, context economics, spec-first review, docs, catalogs, and deterministic fixtures. Global installation, publication, live telemetry, external services, and product-code implementation are excluded.

## Workflows and Failure Paths
Explore classifies intent before feature, validates project context, selects workspace and stage, and exposes evidence, token/coverage economics, roles, writes, blockers, and next checkpoint. Apply recomputes the route fingerprint and performs one action. Ambiguity, drift, unsafe paths, missing anchors, or unsafe rigor overrides block with no mutation.

## Requirements and Business Rules
FR-001 intent-first selection; FR-002 complete read-only card; FR-003 fingerprint revalidation; FR-004 one action; FR-005 tool-owned roots; FR-006 evidence-driven roles; FR-007 adaptive rigor; FR-008 visible context economics; FR-009 blind spec-first review; FR-010 direct-skill compatibility. BR-001 fail closed, BR-002 zero Explore writes, and BR-003 preserve auditable evidence.

## Data, Integrations, and Non-Functional Requirements
Inputs are lifecycle state, specs indexes, project-context metadata, policy, source hashes, and local fixtures. NFR-001 deterministic output, NFR-002 no Explore mutation, NFR-003 explainability, NFR-004 100% critical-anchor recall, NFR-005 at least 15% net pack savings including rereads, NFR-006 compatibility, and NFR-007 readability apply.

## Dependencies, Risks, and Constraints
Shared navigator, state/index/path helpers, context freshness and benchmark tools, policy, and review/test skills are dependencies. Wrong routing, hidden context loss, role creep, reviewer anchoring, unreadable code, and compatibility drift are controlled by fail-closed fixtures and independent gates. The historical `specs-refiniment` physical root is preserved.

## Decisions, Assumptions, and Open Questions
DEC-001–DEC-007 establish the meta-skill, Explore/Apply boundary, separate roots, adaptive roles, context threshold, spec-first review, and global-install exclusion. The stakeholder-confirmed product choices close all blocking refinement questions. Later SDD decisions may select mechanisms only if these contracts remain intact.

## Success Measures
AC-001 correct feedback routing; AC-002 complete no-write Explore; AC-003 drift-safe single-step Apply; AC-004 safe roots; AC-005 evidence-backed roles; AC-006 explained rigor and safe override; AC-007 context recall/economics; AC-008 blind seeded-defect detection; AC-009 compatibility; AC-010 all local gates pass.

## Source Coverage
Authoritative evidence reviewed: `specs-refiniment/011-guided-explore-apply-flow/discovery.md`; `specs-refiniment/011-guided-explore-apply-flow/decision-log.md`; `specs-refiniment/011-guided-explore-apply-flow/prfaq.md`; `specs/009-operational-feedback-hardening/requirements.md`; `specs/007-context-and-prompt-engineering/requirements.md`; `docs/reference/workflow-map.md`; `docs/reference/directory-layout.md`; and `concepts/context-and-quality.md`. Stakeholder feedback and DEC-001–DEC-007 supply the confirmed problem, value, and scope decisions.

## Press Release
Contributors can now start AI SDLC work with one readable Explore request, see exactly where the work will go and why, then Apply one safe checkpoint. The flow removes skill-order guesswork without taking expert controls away.

## Customer FAQ
**Why this flow?** To replace blind skill selection with an auditable route. **Does Explore write?** No. **Can experts invoke skills directly?** Yes. **Why two roots?** Refinement evidence and implementation contracts have distinct lifecycles. **How is context trusted?** Critical anchors and net cost are measured.

## Internal FAQ
**Why this flow?** To replace blind skill selection with an auditable route. **Does Explore write?** No. **Can experts invoke skills directly?** Yes. **Why two roots?** Refinement evidence and implementation contracts have distinct lifecycles. **How is context trusted?** Critical anchors and net cost are measured.

## Business Requirements
| ID | Contract | Acceptance |
|---|---|---|
| FR-001/002 | Resolve intent and show the complete no-write card | AC-001/002 |
| FR-003/004 | Revalidate and execute one checkpoint | AC-003 |
| FR-005–007 | Protect roots and adapt roles/rigor | AC-004–006 |
| FR-008–010 | Prove context, review independently, preserve compatibility | AC-007–010 |

## Launch Risks
Primary risks are wrong feature selection, hidden context loss, unreadable output, review anchoring, and compatibility drift. Controls are fail-closed routing, anchor/economics fixtures, blind review order, human readability checks, and direct-skill regression.
