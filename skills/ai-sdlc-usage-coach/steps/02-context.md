# Context

## Entry

Preflight validation completed and session discovery parameters are established.

## Procedure

Scan local append-only `.toon` session logs in `.ai-sdlc-loop/usage/sessions/`.
Read session metadata, monotonic sequence keys, and event records without loading raw prompts, model prose, or secrets.

## Exit

The factual event stream and active session context are loaded into memory.
