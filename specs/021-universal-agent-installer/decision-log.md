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
  at: "2026-08-04T13:17:49Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "021-universal-agent-installer"
  artifact: "decision-log.md"
  path: "specs/021-universal-agent-installer/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/021-universal-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/021-universal-agent-installer/decision-log.md"
  status: "draft"
  owner: "Harness Maintainers"
  created_at: "2026-08-04"
  updated_at: "2026-08-04"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "decision-log"
    - "draft"
    - "universal-installer"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-08-04 | accepted | Harness Maintainers | Add one configurable `agent-project` profile requiring a safe repository-relative skills root | Existing fixed profiles exclude other compatible hosts; guessed vendor paths would create false conformance | Add many guessed named profiles; configurable compatible-host profile; global install | installer runtime; validator; docs; tests | FR-002; FR-005; AC-002; TC-002 |
| DEC-002 | 2026-08-04 | accepted | Harness Maintainers | Make Python 3.10+ the cross-platform bootstrap and retain `install.sh` for POSIX compatibility | Current shell bootstrap and unconditional `fcntl` import exclude native Windows | PowerShell-only bootstrap; duplicate installer; Python bootstrap delegating to native authority | install.py; install.sh; ai_sdlc_install.py | FR-003; FR-004; AC-005; TC-004 |
| DEC-003 | 2026-08-04 | accepted | Documentation and Release Maintainers | Claim Agent Skills package compatibility for the generic profile, not universal model-host certification | A configurable SKILL.md root proves package placement but not every proprietary discovery/runtime contract | Market as all agents; name only Codex/Claude; state portable package compatibility precisely | README; install guide; supported environments; release notes | NFR-006; AC-008; TC-007 |
