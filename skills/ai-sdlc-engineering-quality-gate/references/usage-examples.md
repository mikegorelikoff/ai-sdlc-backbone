# Engineering Quality Gate Usage Examples

## Contents

1. [TypeScript service correction](#example-1-typescript-service-correction)
2. [Go transaction regression](#example-2-go-transaction-regression)
3. [Review-only Loop invocation](#example-3-review-only-loop-invocation)

These examples illustrate invocation and evidence shape. They are never
substitutes for the active repository's instructions, patterns, or commands.
Resolve `skills/` to the installed skill root when not running from a Harness
source checkout.

## Example 1: TypeScript service correction

Request: add an optional order discount update to an existing TypeScript
service. The diff is in the working tree. The repository uses thin controllers,
service validation, Vitest, and a shared `Result<T>` error pattern.

Generate bounded context:

```bash
python3 skills/ai-sdlc-engineering-quality-gate/scripts/engineering_quality_gate.py context \
  --root . \
  --request "Allow an order discount to be set explicitly to zero" \
  --base HEAD \
  --output specs/order-discount/_ai_sdlc/quality-gate-context.toon \
  --quick-flow
```

Inspect the ranked candidates, then select 2–5 useful comparisons such as the
neighboring invoice and customer update services plus their tests. Record a
Medium correctness finding before editing: the new `value || existing` fallback
discards an explicit zero. Run the focused service test, apply the localized
nullish check and negative test in the repository's existing style, then rerun
the focused test and required typecheck.

Write an exact `ai-sdlc-engineering-quality-gate-draft/v1` TOON draft and
finalize it only against a freshly regenerated post-fix context:

```bash
python3 skills/ai-sdlc-engineering-quality-gate/scripts/engineering_quality_gate.py finalize \
  --root . \
  --context specs/order-discount/_ai_sdlc/quality-gate-post-fix-context.toon \
  --draft specs/order-discount/_ai_sdlc/quality-gate-draft.toon \
  --output specs/order-discount/_ai_sdlc/quality-gate.toon
python3 skills/ai-sdlc-engineering-quality-gate/scripts/engineering_quality_gate.py verify \
  --root . \
  --report specs/order-discount/_ai_sdlc/quality-gate.toon
```

Expected decision: `PASS` when no finding or optional gap remains;
`PASS_WITH_FINDINGS` when only a documented non-blocking item remains.

## Example 2: Go transaction regression

Request: review a completed Go branch that adds retryable payment capture. The
accepted design requires one transaction boundary and idempotent provider
calls. Compare the branch to `main` and use full flow:

```bash
python3 skills/ai-sdlc-engineering-quality-gate/scripts/engineering_quality_gate.py context \
  --root . \
  --request "Add idempotent retryable payment capture" \
  --base main \
  --max-candidates 5 \
  --output specs/payment-capture/_ai_sdlc/quality-gate-context.toon \
  --full-flow
```

Inspect comparable command handlers, transaction helpers, provider adapters,
and service tests. Record a High correctness finding before mutation if the
provider call can repeat after a database commit without the repository's
idempotency key. Run the focused package test and seeded retry test. Apply only
the supported transaction/idempotency correction inside the authorized
payment package, regenerate context, and rerun those tests plus the repository-
required broader Go suite. Do not create a generic retry framework or refactor
neighboring providers.

Finalize and verify with the same two commands shown in Example 1, using the
payment-capture artifact paths. Expected decision: `PASS` only after the High
finding is fixed and all current required checks pass. If the accepted design
does not define the external idempotency contract, retain the finding and
return `FAIL` rather than guessing.

## Example 3: Review-only Loop invocation

Request: independently review a completed Python import CLI, but do not edit
code. Loop feature `safe-import-paths` already has a current specification and
matching Implement approval. Generate a Loop-compatible context fingerprint:

```bash
python3 skills/ai-sdlc-engineering-quality-gate/scripts/engineering_quality_gate.py context \
  --root . \
  --request "Reject import paths that escape the configured workspace" \
  --feature safe-import-paths \
  --output .ai-sdlc-loop/safe-import-paths/quality-gate-context.toon \
  --full-flow
```

Inspect existing path-containment helpers, adjacent CLI subcommands, negative
tests, and package verification commands. If the implementation normalizes a
path only after opening it, record a High security finding with exact source
and test evidence before any potential fix. Because this invocation is
review-only, leave `resolution: remaining`, keep `fix` empty, explain the
authority blocker in `reason_not_fixed`, record applicable checks truthfully,
and finalize to `.ai-sdlc-loop/safe-import-paths/quality-gate.toon`.

Expected decision: `FAIL`, `ready_for_next_stage: false`, with the unresolved
High finding and missing mutation authority named as blocking reasons. A later
authorized invocation must regenerate context, apply the contained fix, rerun
checks, finalize a new report, and invalidate the old fingerprint.
