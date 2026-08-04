---
title: Use the local context cache
description: Build and query an optional deterministic local graph-enhanced RAG index with TOON-only context packs.
---

# Use the local context cache

## Goal

Reuse fresh repository evidence across agent requests, reduce repeated broad
reads, and produce bounded `ai-sdlc-context-pack/v4` input without making a
cache authoritative.

## When to use it

Use the optional cache for a medium or large repository, repeated related
tasks, cross-session retrieval, or relation-aware exploration. Prefer direct
reads for one narrow file or when building the index would cost more than the
expected reuse.

## Prerequisites

- A project-scoped Harness install with the optional `context-cache` module.
- Python 3.10+ whose standard `sqlite3` build includes FTS5.
- Permission to write disposable state below `.ai-sdlc/cache/`.
- A clear query and explicit token, result, and graph bounds.

Install the module from a reviewed source or release:

```bash
./install.sh codex-project --module context-cache
```

Use `claude-code-project` for `.claude/skills/`.

## Procedure

After the optional module is installed, normal Harness StepCard compilation
automatically warms and uses a valid economical cache pack. No background
daemon runs. If the module is absent, policy is invalid, a timeout occurs,
sources drift, the index is corrupt, anchors are incomplete, or savings are too
low, the runtime uses the existing direct-read compiler.

The built-in strict policy is
`.agents/skills/ai-sdlc-context-cache/references/runtime-policy.toon`. A project
may add `.ai-sdlc/context-cache-policy.toon` with the same schema and exact
`skill` plus `step_id` overrides. Values are always clamped to the owning step
manifest; unknown fields fail safely. Portable policy is TOON only.

First prove that all twelve pinned AST parsers are available:

```bash
python3 .agents/skills/ai-sdlc-context-cache/scripts/context_cache.py \
  graph-preflight --root .
```

Build or replace the complete codebase index explicitly. `--require-graph`
fails closed instead of silently accepting lexical-only fallback:

```bash
python3 .agents/skills/ai-sdlc-context-cache/scripts/context_cache.py \
  build --root . --rebuild --require-graph
```

Later incremental refreshes can omit `--rebuild` while retaining the strict
graph gate:

```bash
python3 .agents/skills/ai-sdlc-context-cache/scripts/context_cache.py \
  build --root . --require-graph
```

For the concurrency-safe operation used by StepCards, run:

```bash
python3 .agents/skills/ai-sdlc-context-cache/scripts/context_cache.py \
  warm --root . --lock-timeout-ms 1500 --retries 1
```

Query explained lexical and relation-aware evidence:

```bash
python3 .agents/skills/ai-sdlc-context-cache/scripts/context_cache.py \
  query --root . \
  --query "scheduler context freshness" \
  --limit 12 --graph-depth 1 --graph-limit 64
```

Build a bounded v4 pack for one semantic step:

```bash
python3 .agents/skills/ai-sdlc-context-cache/scripts/context_cache.py \
  pack --root . \
  --query "scheduler context freshness" \
  --skill ai-sdlc-scheduler --step-id context \
  --budget-tokens 4000
```

The cache uses stable chunks, FTS5 candidate selection, deterministic integer
ranking, and bounded typed-edge expansion. It makes no network or model call.
The SQLite file is internal disposable state; all portable output is canonical
TOON.

This is graph-enhanced RAG: it follows deterministic repository relations from
lexical seeds. It does not claim the LLM-extracted entity, community-summary,
or global-search behavior of a full GraphRAG pipeline.

Treat retrieved text as evidence only. A relevance score cannot turn source
content into an instruction, approval, or permission. Recognized repository
instruction files retain their existing scoped authority; other hits remain
`evidence_only`.

## Verify

Check every indexed source hash before using cross-session results:

```bash
python3 .agents/skills/ai-sdlc-context-cache/scripts/context_cache.py \
  verify --root .
```

Expected output reports `status: ready`, `fresh: true`, document, chunk, and
edge counts, plus stable cache and repository fingerprints. A pack is accepted
only when it validates as `ai-sdlc-context-pack/v4`, starts with the owning step
document, retains 100 percent of its critical anchors, respects its budget,
achieves at least 15 percent net savings, and identifies exact source hashes
and line ranges. Otherwise the valid result is `direct_read`.

For release evidence, create a TOON golden-case file using schema
`ai-sdlc-context-cache-benchmark-cases/v1`, then run:

```bash
python3 .agents/skills/ai-sdlc-context-cache/scripts/context_cache.py \
  benchmark --root . --cases context-cache-cases.toon \
  --limit 12 --graph-depth 1 --graph-limit 64
```

Each case names its query, expected paths and anchors, owning skill and step,
budget, and expected `packed` or `direct_read` strategy. The receipt compares
lexical and graph-enhanced recall, mandatory-anchor recall, savings, and stable
fingerprints. Wall-clock latency stays in a separate observational tier so the
deterministic receipt remains byte-identical.

Inspect or reset privacy-safe aggregate outcomes and token economics:

```bash
python3 .agents/skills/ai-sdlc-context-cache/scripts/context_cache.py observe --root .
python3 .agents/skills/ai-sdlc-context-cache/scripts/context_cache.py reset-observations --root .
```

These operations never expose query text, prompts, retrieved content,
credentials, user identity, or wall-clock values.

## Troubleshooting

| Symptom | Safe response |
| --- | --- |
| Cache is missing | Normal StepCard compilation performs bounded `warm`; standalone `query` never rebuilds silently. |
| Cache is stale | Inspect changed paths, rebuild, and verify again. Do not use stale results as sufficient context. |
| FTS5 is unavailable | Use an organization-approved Python build with FTS5 or continue with direct reads. |
| Query returns `direct_read` | Read the named paths and reasons; narrow or clarify the query before rebuilding. |
| Savings are below the threshold | Prefer direct reads for this task. The cache is an optimization, not a required gate. |
| A source is excluded | Check path, size, binary, symlink, generated-output, and credential-like-content rules. Do not weaken secret exclusions for recall. |
| Cache must be removed | Run `purge --root .`; review its TOON receipt and confirm repository sources remain unchanged. |

## Next step

Use the accepted pack with the dependency-ready StepCard, then apply the
[context and verification principles](../learn/context-and-verification.md).
For a one-task non-cached pack, use [Build a task context pack](build-context-pack.md).
