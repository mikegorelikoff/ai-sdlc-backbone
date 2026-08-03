# Validate cache evidence

## Entry

A build, query, or pack receipt exists and its claimed source set is known.

## Procedure

1. Run `verify` against current repository bytes.
2. Recompute or validate cache, repository, query, and pack fingerprints.
3. Confirm every selected source path, hash, line range, authority, score, and
   graph bound.
4. Validate `ai-sdlc-context-pack/v4` through the shared runtime validator.
5. Confirm the owning step document is present, critical-anchor recall is 100
   percent, packed tokens fit the budget, and net savings are at least 15
   percent whenever strategy is `packed`.
6. Run the TOON golden benchmark when validating release claims; compare
   lexical-only, graph-enhanced, and packed or direct-read outcomes twice.
7. Reject stale, corrupt, incomplete, unsafe, non-deterministic, or uneconomic
   evidence.

## Exit

Return validation status, acceptance evidence, savings, and residual risk.
