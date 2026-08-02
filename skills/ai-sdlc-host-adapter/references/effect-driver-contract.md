# Effect driver contract

Negotiation proves compatibility but does not execute. An effect request binds
the negotiation, StepCard and context fingerprints, exact native operation,
capabilities, side-effect class, approval reference, bounded arguments, and a
stable idempotency key. Any mismatch fails before the driver runs.

Only registered drivers execute. `workspace.write-text` uses a repository-
relative path and an expected-content precondition. `external.toon-post` sends
canonical TOON to an explicitly allowlisted credential-free HTTPS endpoint and
passes the idempotency key as a transport header. There is no generic command
or shell driver.

The first successful execution atomically persists one TOON receipt. Replays
with the same request return it without repeating the effect. Secret-bearing
argument keys, traversal, links, unapproved external effects, changed payloads,
and foreign receipts fail closed.
