---
title: Certify provider execution
description: Pin the live protocol, collect an attested provider observation, and reject offline evidence as certification.
---

# Certify provider execution

## Goal

Produce a provider-executed TC-012 receipt tied to one harness revision,
scenario version, provider, host, model, execution identity, and evidence set.

## Procedure

First generate the offline protocol. This validates scenario construction and
per-step context packs, but its portable template remains `pending`:

```bash
python3 .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_skill_eval.py \
  --mode live-protocol --skills-root .agents/skills \
  --output tc-012-live-protocol.toon --full-flow
```

In an authorized provider session, execute every pinned scenario and create an
`ai-sdlc-provider-execution/v1` observation. Record provider, host, model,
execution ID, RFC 3339 time, scenario version, attestation, per-scenario score
and evidence, effect receipt references, and recovery evidence. Do not copy an
offline fixture into this record or infer a provider identity.

Validate it against the exact protocol:

```bash
python3 .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_provider_eval.py \
  --protocol tc-012-live-protocol.toon \
  --observations tc-012-provider-observation.toon \
  --output tc-012-provider-receipt.toon --root . --full-flow
```

## Verify

A passing receipt covers the complete scenario set, agrees with every
criterion threshold, and preserves protocol, context, effect, and recovery
evidence. Missing identity, missing attestation, incomplete scenarios,
contradictory scores, stale fingerprints, or offline execution cannot produce
a passing provider verdict. Certification applies only to the identity and
evidence in that receipt; it is not a claim about other hosts or models.
