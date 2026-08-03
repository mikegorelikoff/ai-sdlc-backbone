# Build or refresh local index

## Entry

The preflight boundary is accepted and a durable cache write is authorized.

## Procedure

1. Run `graph-preflight`, then `build --require-graph`; use `--rebuild` only when an incompatible or corrupt disposable
   projection must be replaced.
2. Verify discovery exclusions before content reads.
3. Check the TOON receipt for indexed, unchanged, removed, excluded, parsed
   language, symbol, occurrence, graph-node, and graph-edge counts.
4. Preserve the cache and repository logical fingerprints for later freshness
   checks.
5. Run `graph-stats` and require complete observed-language coverage, bounded
   relation fan-out, fresh hashes, and stable fingerprints.
6. If FTS5, any required grammar, isolated parsing, AST completeness, source
   recheck, or graph bounds fail, stop and use direct reads.

## Exit

Return one complete build receipt and the accepted cache fingerprint, or an
explained direct-read fallback. Never claim readiness from a partial database.
