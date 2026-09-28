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
  at: "2026-09-28T10:00:00Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "026-usage-coach"
  artifact: "decision-log.md"
  path: "specs/026-usage-coach/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/026-usage-coach/_ai_sdlc/state.toon"
  decision_log: "specs/026-usage-coach/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-09-28"
  updated_at: "2026-09-28"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "decision-log"
    - "draft"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-09-28 | accepted | Engineering | Adopt local append-only event-sourced TOON session journal and on-demand interactive usage coach | Multi-session behavioral feedback needed without external telemetry, scoring, or SQLite/JSON analytics databases | Global mutable SQLite DB; remote telemetry pipeline; append-only local TOON journals | design.md; usage_journal.py; coach.py; Loop skills | AC-001 through AC-008; TC-001 through TC-016 |
