# Context

## Entry

Preflight validation has completed successfully and session discovery parameters are established deterministically. The execution environment is verified, and repository roots and working paths are confirmed.

## Procedure

1. Scan local append-only `.toon` session logs in the usage directory (`.ai-sdlc-loop/usage/sessions/` or `.ai-sdlc/usage/sessions/`).
2. Read session metadata, monotonic sequence keys, and event records without loading raw prompts, model prose, or secrets.
3. Validate that each parsed event contains well-formed event types, timestamps, and duration fields.
4. Filter historical sessions by the specified scan window or feature identifier.

## Exit

The factual event stream and active session context are loaded into memory and ready for analytical processing without data minimization violations.
