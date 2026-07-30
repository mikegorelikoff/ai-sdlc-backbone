---
title: TOON-only agent artifacts
description: Why one canonical machine representation keeps execution, context, replay, and evaluation deterministic.
---

# TOON-only agent artifacts

The harness uses TOON as its only structured machine-data representation.
Contracts, fixtures, configuration, manifests, context packs, plans, journal
events, state projections, and evaluation receipts all use `.toon`. Human
guidance and review artifacts remain Markdown.

This follows the [TOON specification 3.3](https://toonformat.dev/reference/spec)
for nested objects, primitive arrays, tabular uniform-object arrays, expanded
non-uniform arrays, scalar values, and quoting. One shared deterministic encoder
and decoder keep output consistent across capabilities.

## Why one representation matters

The machine boundary is intentionally narrow:

- one parser means one scalar and table interpretation;
- one canonical encoder means byte-stable fingerprints and golden fixtures;
- one extension makes repository-wide conformance easy to audit;
- one context representation prevents format conversion from consuming or
  distorting the prompt budget;
- one journal representation makes replay and recovery use the same validation
  path as plans and state.

CLI commands expose `--format toon` for machine output and may expose Markdown
for human review. A machine record never gains a second serialization merely
because a human projection exists.

## Canonical invariants

Repository-owned TOON is deterministic, newline-terminated, and preserves the
complete logical record. Mapping order, scalar encoding, tables, nested
evidence, gates, source anchors, budgets, and task state are canonical.
Fingerprints are calculated from canonical logical data. Decode and encode of a
generated artifact must reproduce the same bytes.

Malformed input, an unexpected schema, or a non-canonical generated artifact
fails closed. Runtime does not carry an alternate parser or an in-place legacy
conversion mode.

## Context-engineering impact

Step context is compiled into `ai-sdlc-context-pack/v4`. It records exact source
ranges, instruction authority, selected and skipped evidence, mandatory-anchor
recall, token estimates, savings, sufficiency, and a direct-read fallback.
Because the pack and StepCard use the same canonical representation, the
selection fingerprint describes exactly what the executor receives.

Packed context is allowed only when every critical anchor is retained and the
pack saves enough tokens. Otherwise the StepCard names exact direct-read paths
instead of pretending a lossy summary is sufficient.

## Durable runtime paths

Each run stores an immutable `plan.toon`, one hash-chained event per
`journal/<sequence>.toon`, and a replay-derived `state.toon`. The event order is
strict: planned, started, terminal, evidence, result. Replay validates
identities, attempts, sequence continuity, the hash chain, and protocol order
before replacing the state projection.
