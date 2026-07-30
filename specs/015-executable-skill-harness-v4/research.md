---
type: "ai-sdlc.research"
title: "Research"
description: "Evidence-backed technical or product research."
tags:
  - "ai-sdlc"
  - "research"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-30T09:31:58Z"
artifact_metadata:
  schema: "ai-sdlc-research-metadata/v1"
  feature: "015-executable-skill-harness-v4"
  artifact: "research.md"
  path: "specs/015-executable-skill-harness-v4/research.md"
  workspace: "implementation"
  skill: "ai-sdlc-research"
  flow_mode: "full"
  state_file: "specs/015-executable-skill-harness-v4/_ai_sdlc/state.toon"
  status: "review"
  updated_at: "2026-07-30"
  trace_ids:
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "FR-001"
    - "FR-002"
    - "FR-003"
    - "FR-004"
    - "FR-005"
    - "FR-006"
    - "FR-007"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
  metatags:
    - "ai-sdlc"
    - "research"
    - "evidence"
    - "traceable"
---

# Research

## Topic

Deterministic executable skill harness and context engineering for AI SDLC Harness v4

## Questions

- id: RQ-001; question: Which skill structure makes multi-step agent work explicit without loading every instruction eagerly?; trace_targets: FR-001/FR-002/NFR-001/DEC-002
- id: RQ-002; question: Which durable-execution invariants are required for safe resume;  retry;  and side effects?; trace_targets: FR-004/FR-005/NFR-002/DEC-003
- id: RQ-003; question: How should context be selected and measured for long-running skill steps?; trace_targets: FR-003/NFR-003/NFR-004/DEC-004
- id: RQ-004; question: Which repository and evaluation feedback loops make an agent harness maintainable?; trace_targets: FR-006/FR-007/NFR-005/DEC-005

## Sources

- accessed_at: 2026-07-30; credibility: Canonical Agent Skills format specification.; id: SRC-001; locator: https://agentskills.io/specification; notes: Defines progressive disclosure;  skill directory structure;  validation;  and concise SKILL.md guidance.; title: Agent Skills specification; type: open-specification
- accessed_at: 2026-07-30; credibility: Official Agent Skills authoring guidance.; id: SRC-002; locator: https://agentskills.io/skill-creation/best-practices; notes: Recommends explicit checklists;  dependency and validation gates;  moderate detail;  and on-demand references.; title: Best practices for skill creators; type: official-guidance
- accessed_at: 2026-07-30; credibility: Primary engineering publication from an agent platform provider.; id: SRC-003; locator: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents; notes: Treats context as a finite attention budget and recommends high-signal just-in-time retrieval;  compaction;  and structured memory.; title: Effective context engineering for AI agents; type: engineering-research
- accessed_at: 2026-07-30; credibility: Primary report describing a tested long-running coding harness.; id: SRC-004; locator: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents; notes: Reports better continuity from incremental work;  explicit progress artifacts;  clean handoffs;  and feature-by-feature execution.; title: Effective harnesses for long-running agents; type: engineering-experiment
- accessed_at: 2026-07-30; credibility: Primary OpenAI engineering case study.; id: SRC-005; locator: https://openai.com/index/harness-engineering/; notes: Uses repository knowledge as the system of record and emphasizes legibility;  executable feedback loops;  and architecture enforcement.; title: Harness engineering: leveraging Codex in an agent-first world; type: engineering-case-study
- accessed_at: 2026-07-30; credibility: Official durable workflow runtime documentation.; id: SRC-006; locator: https://docs.langchain.com/oss/javascript/langgraph/functional-api; notes: Specifies checkpointed task results;  TOON-serializable state;  deterministic replay order;  idempotency;  and encapsulated side effects.; title: LangGraph functional API: durable execution; type: runtime-documentation
- accessed_at: 2026-07-30; credibility: Direct source-code inspection and baseline test execution in this repository.; id: SRC-007; locator: skills/ai-sdlc-shared-runtime; notes: Shows v1 three-step manifests;  v3 context packs;  plan-only workflow graphs;  durable run primitives;  and contract drift.; title: Current AI SDLC Harness runtime;  step;  context;  flow;  and skill contracts; type: internal-evidence

## Findings

- confidence: high; id: RF-001; limitations: The Agent Skills specification does not define an executable DAG;  so the v4 manifest remains an AI SDLC extension.; source_ids: SRC-001/SRC-002/SRC-003/SRC-007; statement: The canonical skill router should stay concise while a machine-readable DAG selects focused step documents and references just in time.; trace_targets: FR-001/FR-002/NFR-001/DEC-002
- confidence: high; id: RF-002; limitations: Filesystem journaling is suitable for the portable local harness but does not replace a transactional distributed scheduler.; source_ids: SRC-004/SRC-006/SRC-007; statement: Resume safety requires stable task identity;  persisted results;  deterministic dependency order;  TOON-serializable state;  idempotency keys;  and explicit side-effect boundaries.; trace_targets: FR-004/FR-005/NFR-002/DEC-003
- confidence: high; id: RF-003; limitations: Lexical retrieval trades semantic recall for offline determinism; live evals must guard representative cases where wording differs.; source_ids: SRC-003/SRC-004/SRC-007; statement: Context should be compiled per step from mandatory anchors plus deterministic lexical topology and trace signals;  with sufficiency and recall gates before execution.; trace_targets: FR-003/NFR-003/NFR-004/DEC-004
- confidence: high; id: RF-004; limitations: Live-agent quality varies by host and provider; the repository can define a neutral protocol but cannot certify every external runtime offline.; source_ids: SRC-002/SRC-005/SRC-007; statement: A maintainable harness needs repository-native contracts;  generated projections;  drift checks;  deterministic evals for every skill;  and a separate live-agent evaluation tier.; trace_targets: FR-006/FR-007/NFR-005/DEC-005
- confidence: high; id: RF-005; limitations: This is an AI SDLC policy choice derived from the repository safety model rather than a universal external requirement.; source_ids: SRC-004/SRC-005/SRC-006/SRC-007; statement: Explore must remain read-only and durable run creation must begin only at Apply so planning probes cannot leave hidden execution state.; trace_targets: FR-005/NFR-006/DEC-006

## Open Questions

- id: OQ-001; next_action: Run the provider-neutral live eval protocol on the release candidate and record provider-specific receipts without changing deterministic core behavior.; owner: Release maintainers; question: Which provider and model matrix should be required for the first live v4 release certification?
