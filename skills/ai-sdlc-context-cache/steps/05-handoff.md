# Handoff cache-backed context

## Entry

Validation is complete and the result or fallback has a stable fingerprint.

## Procedure

1. State whether the result is cached or direct-read and whether it is fresh.
2. Preserve exact source paths, hashes, line ranges, query and graph bounds,
   token economics, cache fingerprint, and validation evidence.
3. Remind the next owner that repository files remain authoritative.
4. Name the explicit rebuild or purge command only when needed and authorized.
5. Do not persist conversation history, secrets, or unstated user attributes.

## Exit

Return a bounded handoff with owner, next action, freshness, fingerprint, and
recovery path.
