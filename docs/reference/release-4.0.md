---
title: Release 4.0
description: Scope, compatibility, validation, limitations, and rollback for v4.0.0.
---

# Release `v4.0.0`

`v4.0.0` turns every installable skill into an explicit, deterministic
execution protocol. It combines semantic skill DAGs, just-in-time context
engineering, portable StepCards, durable per-step replay, cross-component
contract checks, and one canonical TOON machine boundary.

## Delivered scope

- All 44 skills use `ai-sdlc-skill-steps/v2` manifests with at least five
  semantic nodes; generated `SKILL.md` routers remain concise and drift-checked.
- The selector validates DAGs, resolves ready waves, compiles context-complete
  StepCards, and emits immutable run v2 plans with stable fingerprints.
- Context pack v4 records mandatory anchors, selected and skipped sources,
  authority, exact ranges, critical recall, token economics, sufficiency, and
  direct-read fallback.
- Flow Explore remains zero-write. Fingerprinted Apply creates a bounded run
  and rejects stale decisions before mutation.
- Runtime v2 journals planned, started, terminal, evidence, and result events;
  completion fingerprints bind result, evidence, and effect receipts across
  interruption and replay.
- Workflow v2, host adapter v2, handoff v2, deterministic evaluations, and the
  complete test-file runner preserve the same StepCard semantics.
- All structured machine contracts, fixtures, state, receipts, and generated
  outputs use canonical TOON; alternate runtime readers and serializers are
  absent.

## Validation evidence

The reviewed Feature 015 plan covers 94 skill-owned test files, 44 semantic
graphs with 221 nodes, 220 deterministic evaluation scenarios, six offline
provider-neutral protocol scenarios, source and installed-layout smoke checks,
compatibility, security boundaries, SDD traceability, canonical machine-data
checks, documentation tests, a strict site build, rendered-link validation,
and diff hygiene.

The final release commit is validated with the compatibility roadmap's pending
last-subject allowance. After the commit, compatibility runs again against the
exact history without that allowance. Protected CI, the remote tag, and a
fresh tagged installation are post-publication signals and are verified after
the tag exists.

## Compatibility and migration

Harness API `4.0.0` is a hard cut. Read [Migrate to
4.0](../how-to/migrate-4.0.md) before updating. Pre-v4 machine plans, state,
journals, receipts, manifests, and configuration are retained only as
historical evidence and must be regenerated from authoritative sources.
Human-authored specifications and product source remain consumer-owned.

## Known limitations

- The repository validates the provider-neutral live protocol offline.
  Provider-executed certification still requires a release-owner receipt that
  names provider, host, model, execution identity, scores, effect receipts, and
  recovery evidence. DEC-008 permits publication with that certification
  pending and forbids presenting offline evidence as provider execution.
- Filesystem journals are local durability, not a distributed transaction
  system. External effects still require idempotent host operations and
  accountable effect receipts.
- Installer recognition does not certify every agent host. Hosts not listed
  with evidence in the supported-environments matrix remain unverified.
- GitHub branch protection, organization policy, deployment authority, and
  production acceptance remain external controls.

## Rollback

Stop before tag publication if any required local gate fails. After
publication, restore the consumer's accepted pre-migration revision through a
new commit, reinstall its exact managed inventory, and preserve the v4 run and
validation artifacts. Publish corrections as new immutable history; never move
or rewrite a consumed release tag.
