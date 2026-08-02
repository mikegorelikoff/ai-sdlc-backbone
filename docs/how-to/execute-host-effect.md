---
title: Execute a host effect safely
description: Execute one negotiated allowlisted effect with approval, context binding, and replay-safe evidence.
---

# Execute a host effect safely

## Goal

Turn a compatible host negotiation into one bounded effect and a durable
`ai-sdlc-effect-receipt/v1` without exposing a generic shell boundary.

## Procedure

Create a canonical TOON request from `effect-request.schema.toon`. Bind the
adapter ID, negotiation fingerprint, StepCard fingerprint, context fingerprint,
operation, complete capability set, side-effect class, approval reference,
bounded arguments, and the digest of the semantic request as its idempotency
key. Then execute:

```bash
python3 .agents/skills/ai-sdlc-host-adapter/scripts/effect_driver.py . \
  --request effect-request.toon --negotiation negotiation.toon --full-flow
```

Use `workspace.write-text` only for a repository-relative regular-file path
with an expected prior SHA-256 when replacement is possible. Use
`external.toon-post` only for a credential-free HTTPS URL whose exact host is
in the request allowlist; external writes require an approval reference.

## Verify

The first successful call writes one receipt below `_ai_sdlc/effects/`. Repeat
the identical request and confirm it returns the same receipt without invoking
the effect again. Changed arguments cannot reuse the idempotency key. Traversal,
symlinks, secret-bearing argument keys, missing approval, foreign receipts, or
negotiation/context drift must fail before execution.

There is intentionally no command or shell driver. Add a new driver only with
a versioned schema, explicit argument validator, bounded side effect, approval
rules, deterministic tests, security review, and compatibility registration.
