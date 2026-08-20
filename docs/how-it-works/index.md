# How it works

This page is the canonical mental model for AI SDLC Backbone.

```text
Request → Explore → Specify → Plan → Implement → Verify → Handoff
```

The Backbone structures work through skills, repository artifacts, explicit
state, deterministic helpers, evidence, and human-controlled gates. A request
is routed to the smallest useful flow. Higher-risk or ambiguous work uses more
predecessor checks, traceability, and approval points.

## Authority model

- People own intent, trade-offs, consequential approvals, and release.
- Repository artifacts preserve requirements, decisions, plans, and evidence.
- Agent output is a proposal until the applicable gate or owner accepts it.
- Generated state supports continuity but does not replace source evidence.

## Licensed distribution boundary

The public installer sends the license key to the licensing API. After an
entitlement check, the service returns a short-lived, one-time download grant
and an expected SHA-256. The installer downloads from that service, verifies
the checksum, safely extracts the allowlisted product artifact, and performs
an idempotent installation. Only the backend holds private GitHub credentials.

Exact licensing behavior is in [Reference](../reference/licensing.md).
