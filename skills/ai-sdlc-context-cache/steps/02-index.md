# Build or refresh local index

## Entry

The preflight boundary is accepted and a durable cache write is authorized.

## Procedure

1. Run `build`; use `--rebuild` only when an incompatible or corrupt disposable
   projection must be replaced.
2. Verify discovery exclusions before content reads.
3. Check the TOON receipt for indexed, unchanged, removed, and excluded counts.
4. Preserve the cache and repository logical fingerprints for later freshness
   checks.
5. If FTS5 is unavailable or the build fails, stop and use direct reads.

## Exit

Return one complete build receipt and the accepted cache fingerprint, or an
explained direct-read fallback. Never claim readiness from a partial database.
