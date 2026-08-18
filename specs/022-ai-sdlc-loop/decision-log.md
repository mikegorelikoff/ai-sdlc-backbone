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
  at: "2026-08-17T11:08:28Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "decision-log.md"
  path: "specs/022-ai-sdlc-loop/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-branching"
  flow_mode: "full"
  state_file: "specs/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs/022-ai-sdlc-loop/decision-log.md"
  status: "draft"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-08-17"
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
| DEC-001 | 2026-08-17 | accepted | maintainer | Use feature/022-ai-sdlc-loop from refreshed main for the complete user-visible task | main matched origin/main; all dirty paths were related refinement and implementation planning artifacts | Continue on main; split repositories into separate parent tasks; one aligned task branch | branch-plan.md; implementation SDD; parent integration | git fetch origin main; git rev-list --left-right --count main...origin/main; user-approved scope |
| DEC-002 | 2026-08-17 | accepted | maintainer | Replace the premature one-skill JSON design with five stage-oriented skills, one shared runtime, canonical step manifests, and TOON-only durable contracts | User explicitly corrected that Loop requires several skills and that the AI SDLC product family always uses TOON | One monolithic skill with JSON; copied full Harness catalog; fixed minimal skill graph with TOON | requirements.md; design.md; test-cases.md; tasks.md; Loop runtime and installer | FR-001; FR-002; FR-003; FR-006; FR-008; FR-010; AC-001; AC-002; AC-004; AC-006; AC-008 |
| DEC-003 | 2026-08-17 | accepted | maintainer | Strengthen Loop with eight self-contained Harness delivery-control skills while excluding the full discovery/refinement dependency chain | User requested a stronger skill package; dependency audit showed full Harness SDD would require absent upstream product artifacts and skills | Keep only five stage skills; copy the complete Harness catalog; add the autonomous delivery-control core | requirements.md; design.md; test-cases.md; tasks.md; installer; skills; tests | FR-001; FR-002; FR-010; FR-011; AC-001; AC-009; TC-026 |
| DEC-004 | 2026-08-18 | accepted | maintainer | Add a compact autonomous QA owner before release | User requested one more valuable capability; the Harness QA skill depended on an 18-stage refinement cascade, so Loop needs a smaller support boundary | Copy the cascade-dependent QA skill; omit QA; create a focused TOON-native QA plan and signoff workflow | requirements.md; design.md; test-cases.md; tasks.md; installer; ai-sdlc-loop-qa; tests | FR-001; FR-011; FR-012; AC-001; AC-010; TC-027 |
| DEC-005 | 2026-08-18 | accepted | maintainer | Complete the focused package with requirements-gap and release-readiness owners | User requested two final skills; these close pre-Specify ambiguity and pre-tag evidence gaps without importing the Harness refinement cascade | Copy full refinement skills; add arbitrary helpers; create two compact Harness-v2-compatible TOON reviewers | requirements.md; design.md; test-cases.md; tasks.md; installer; ai-sdlc-loop-requirements-review; ai-sdlc-loop-release-readiness; tests | FR-001; FR-011; FR-013; FR-014; AC-001; AC-011; AC-012; TC-028; TC-029 |
| DEC-006 | 2026-08-18 | accepted | maintainer | Namespace every distributed skill as `ai-sdlc-loop-{slug}` and name the router `ai-sdlc-loop-orchestrate` | User required a product-owned namespace before release so installed skills are visibly attributable to Loop and cannot be confused with Harness skills | Retain Harness names; prefix only lifecycle skills; namespace the complete installed inventory | requirements.md; design.md; test-cases.md; tasks.md; installer; all Loop skill directories and manifests; README; tests | FR-001; FR-015; AC-001; AC-013; TC-030 |
| DEC-007 | 2026-08-18 | accepted | maintainer | Publish Loop through a standalone MkDocs Material site with the six-section product navigation | User required MkDocs for the public Loop product after its first release; a source-backed compact site avoids copying the large Harness catalog | README only; copy Harness docs wholesale; compact Loop-owned site with strict build and Pages workflow | mkdocs.yml; docs; requirements-docs.txt; README; CONTRIBUTING.md; GitHub workflows; tests | FR-016; AC-014; TC-031; T010 |
