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
  at: "2026-08-03T10:03:50Z"
artifact_metadata:
  schema: "ai-sdlc-research-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "research.md"
  path: "specs-refiniment/017-local-context-cache/research.md"
  workspace: "refinement"
  skill: "ai-sdlc-research"
  flow_mode: "full"
  state_file: "specs-refiniment/017-local-context-cache/_ai_sdlc/state.toon"
  status: "review"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-006"
    - "AC-008"
    - "AC-010"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "FR-001"
    - "FR-002"
    - "FR-003"
    - "FR-004"
    - "FR-005"
    - "FR-006"
    - "FR-007"
    - "FR-008"
    - "FR-009"
    - "FR-010"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
    - "OQ-001"
    - "OQ-003"
  metatags:
    - "ai-sdlc"
    - "research"
    - "evidence"
    - "traceable"
---

# Research

## Topic

Deterministic local graph-enhanced retrieval and context engineering for AI SDLC Harness

## Questions

- id: RQ-001; question: Which local storage and lexical retrieval primitives are portable and deterministic enough for the harness?; trace_targets: FR-001/FR-002/NFR-001/DEC-001
- id: RQ-002; question: Which graph semantics add useful repository topology without an LLM indexing dependency?; trace_targets: FR-005/NFR-003/DEC-003
- id: RQ-003; question: How must retrieval integrate with the existing context-pack v4 contract?; trace_targets: FR-006/FR-007/AC-006/DEC-004
- id: RQ-004; question: Which context-engineering measurements prove that the cache saves tokens without dropping critical instructions?; trace_targets: FR-010/NFR-004/NFR-007/DEC-007
- id: RQ-005; question: Which security boundaries apply to locally retrieved repository content?; trace_targets: FR-008/NFR-005/AC-008/DEC-005
- id: RQ-006; question: How should incremental indexing detect changes and recover from stale or corrupt state?; trace_targets: FR-003/FR-009/NFR-002/DEC-006
- id: RQ-007; question: Which GraphRAG capabilities belong in the first local release and which must be deferred?; trace_targets: FR-005/DEC-003/OQ-003

## Sources

- accessed_at: 2026-08-03; credibility: Canonical SQLite documentation.; id: SRC-001; locator: https://www.sqlite.org/fts5.html; notes: Defines FTS5 full-text queries;  ranking;  and index consistency considerations.; title: SQLite FTS5 Extension; type: official-documentation
- accessed_at: 2026-08-03; credibility: Canonical SQLite transaction documentation.; id: SRC-002; locator: https://www.sqlite.org/lang_transaction.html; notes: Defines explicit transactions and atomic commit behavior needed for synchronized index updates.; title: SQLite Transactions; type: official-documentation
- accessed_at: 2026-08-03; credibility: Primary research publication.; id: SRC-003; locator: https://arxiv.org/abs/2404.16130; notes: Defines GraphRAG as an LLM-extracted entity graph with community summaries for global questions.; title: From Local to Global GraphRAG research paper; type: research-paper
- accessed_at: 2026-08-03; credibility: Official Microsoft GraphRAG documentation.; id: SRC-004; locator: https://microsoft.github.io/graphrag/query/overview/; notes: Distinguishes local graph plus text search from resource-intensive global community-report search.; title: GraphRAG Query Engine Overview; type: official-documentation
- accessed_at: 2026-08-03; credibility: Official Microsoft GraphRAG documentation.; id: SRC-005; locator: https://microsoft.github.io/graphrag/index/methods/; notes: Documents standard and fast graph indexing tradeoffs and LLM-dependent extraction costs.; title: GraphRAG Indexing Methods; type: official-documentation
- accessed_at: 2026-08-03; credibility: Primary engineering guidance from an agent platform provider.; id: SRC-006; locator: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents; notes: Treats context as a finite attention budget and recommends selecting the smallest high-signal token set.; title: Effective context engineering for AI agents; type: engineering-research
- accessed_at: 2026-08-03; credibility: Primary engineering evaluation from an agent platform provider.; id: SRC-007; locator: https://www.anthropic.com/engineering/contextual-retrieval; notes: Shows exact-term value from BM25 and retrieval gains from attaching document-specific context to chunks.; title: Introducing Contextual Retrieval; type: engineering-experiment
- accessed_at: 2026-08-03; credibility: Industry security standard.; id: SRC-008; locator: https://genai.owasp.org/llmrisk/llm01-prompt-injection/; notes: States that RAG does not fully mitigate indirect prompt injection from external content.; title: OWASP Prompt Injection Risk; type: security-standard
- accessed_at: 2026-08-03; credibility: Primary security engineering guidance.; id: SRC-009; locator: https://openai.com/index/designing-agents-to-resist-prompt-injection/; notes: Recommends constraining capability impact and preserving authority boundaries when agents consume untrusted content.; title: Designing AI agents to resist prompt injection; type: engineering-security
- accessed_at: 2026-08-03; credibility: Canonical Git documentation.; id: SRC-010; locator: https://git-scm.com/docs/gitdatamodel.html; notes: Defines immutable content-addressed objects suitable as tracked-content change evidence.; title: Git Data Model; type: official-documentation
- accessed_at: 2026-08-03; credibility: Direct repository inspection and deterministic prototype tests.; id: SRC-011; locator: skills/ai-sdlc-context-cache; notes: Shows the current SQLite schema;  discovery filters;  chunking;  relation edges;  retrieval;  context packing;  and known mandatory-anchor gap.; title: Current local context cache prototype; type: internal-evidence
- accessed_at: 2026-08-03; credibility: Canonical Git documentation.; id: SRC-012; locator: https://git-scm.com/docs/git-diff.html; notes: Defines path status and object identifiers useful for incremental changed-file detection.; title: Git diff documentation; type: official-documentation

## Findings

- confidence: high; id: RF-001; limitations: FTS5 behavior still depends on the SQLite build shipped by the host; capability verification is required before use.; source_ids: SRC-001/SRC-002/SRC-011; statement: The portable baseline should use SQLite FTS5 with the content tables and full-text index updated atomically in the same transaction and verified for consistency.; trace_targets: FR-001/FR-003/NFR-002/DEC-001
- confidence: medium; id: RF-002; limitations: Embedding and reranking gains are corpus-dependent and are not proven for this repository until the golden-query evaluation is executed.; source_ids: SRC-001/SRC-007/SRC-011; statement: Lexical retrieval is the deterministic offline baseline because it handles exact identifiers well; document and heading context should be attached to chunks while embeddings remain a future optional adapter.; trace_targets: FR-002/FR-004/NFR-001/DEC-002
- confidence: high; id: RF-003; limitations: A typed repository-relation graph cannot answer corpus-wide thematic questions in the same way as an LLM-extracted entity and community graph.; source_ids: SRC-003/SRC-004/SRC-005/SRC-011; statement: The first release is graph-enhanced RAG with deterministic bounded relation expansion and must not claim parity with Microsoft GraphRAG; provider-backed entity extraction and community summaries are deferred.; trace_targets: FR-005/NFR-003/DEC-003/OQ-003
- confidence: high; id: RF-004; limitations: The 15 percent savings threshold is a harness policy and must be validated on representative repository tasks.; source_ids: SRC-006/SRC-007/SRC-010; statement: Context engineering requires the smallest high-signal context that preserves the owning StepCard;  mandatory evidence;  critical anchors;  authority labels;  source hashes;  and a stable fingerprint; insufficient packs must fall back to direct reading.; trace_targets: FR-006/FR-007/NFR-004/AC-006/DEC-004
- confidence: high; id: RF-005; limitations: Deterministic filtering and authority labels reduce impact but cannot perfectly detect every malicious instruction embedded in repository content.; source_ids: SRC-008/SRC-009/SRC-011; statement: Retrieved repository text is untrusted evidence rather than executable instruction; the cache must preserve instruction hierarchy and cannot authorize tools;  writes;  or external actions.; trace_targets: FR-008/NFR-005/AC-008/DEC-005
- confidence: high; id: RF-006; limitations: Git object identity covers tracked content; untracked files require direct content hashes and explicit discovery rules.; source_ids: SRC-010/SRC-012/SRC-011; statement: Incremental indexing should use repository-relative paths and content fingerprints;  replace changed chunks and edges transactionally;  remove stale entries;  and reject symlinks;  binary files;  secrets;  generated output;  and oversized files.; trace_targets: FR-003/FR-009/NFR-006/DEC-006
- confidence: medium; id: RF-007; limitations: Token savings are estimates and do not guarantee answer quality; live-agent evaluation remains a separate optional tier.; source_ids: SRC-005/SRC-006/SRC-007/SRC-011; statement: Release claims require a deterministic evaluation harness comparing direct read;  lexical retrieval;  and graph expansion on golden queries using mandatory-anchor recall;  recall at k;  estimated token savings;  latency;  and stable receipt fingerprints.; trace_targets: FR-010/NFR-007/AC-010/DEC-007/OQ-001

## Open Questions

- id: OQ-001; next_action: Approve deterministic release thresholds in DEC-007 and encode them in the benchmark command and QA readiness gate.; owner: Maintainers and QA; question: Which mandatory-anchor recall and token-savings thresholds gate the first release?
- id: OQ-002; next_action: Define a provider-neutral embedding adapter only after lexical and graph-enhanced baselines are measured.; owner: Architecture; question: Which optional local embedding runtime should be supported first?
- id: OQ-003; next_action: Assess an opt-in provider-backed entity and community pipeline after the portable local release.; owner: Product and Architecture; question: Should a later module implement full GraphRAG global search?
