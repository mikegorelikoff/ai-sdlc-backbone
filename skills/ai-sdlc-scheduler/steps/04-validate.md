# Validate — AI SDLC Scheduler

## Entry

A create, claim, recovery, or terminal mutation completed.

## Procedure

Replay the event fingerprint chain, validate the state fingerprint, verify ready
ordering and lease uniqueness, and inspect any external-effect receipt before
accepting the transition.

Compare the scheduler task with the isolated runtime task: IDs, context and
step fingerprints, worker lease, terminal outcome, result identity, and effect
receipt must agree. Exercise stale revisions, expired nonces, interrupted
runtime completion, and identical replay. A passing unit test without the
cross-component identity check is insufficient evidence.

## Output Spec

- Success includes a valid event chain, current state fingerprint, unique live
  lease per task, byte-stable replay, and matching runtime/effect evidence.
- Failure names the first stale revision, context, lease, journal, runtime, or
  receipt invariant and leaves prior durable evidence intact.

## Exit

The projection is replay-valid and acceptance evidence is recorded.
