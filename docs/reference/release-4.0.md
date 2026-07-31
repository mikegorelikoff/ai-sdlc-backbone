---
title: Release 4.0.1
description: Scope, corrective installation contract, validation, limitations, and rollback for v4.0.1.
---

# Release `v4.0.1`

`v4.0.1` is the accepted v4 patch release. It preserves Harness API `4.0.0`
and the `v4.0.0` executable skill system, then replaces the incompatible
external consumer installation path with a Harness-owned, deterministic,
TOON-only installer.

The original `v4.0.0` tag remains immutable. A post-publication fresh-install
smoke found that its external installer generated a non-TOON lock despite the
repository's TOON-only contract. The release was not rewritten: `v4.0.1`
records the correction as new history.

## Delivered execution scope

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

## Corrective installation scope

- `install.sh` fetches an exact tag or commit and runs the source-owned Python
  installer without npm, a package registry, or a third-party skill CLI.
- The installer requires a clean source revision, reads the canonical managed
  inventory, rejects symlinks and non-TOON machine artifacts, and supports only
  the validated project-scoped Codex target.
- Every skill is staged, hashed, copied, and rehashed before acceptance.
  Existing differing managed directories fail closed unless a human has
  explicitly reviewed replacement.
- `.ai-sdlc/harness-install.toon` records portable installation identity.
  `.ai-sdlc/harness-install-lock.toon` binds every managed path to a SHA-256
  tree digest over relative paths, permission modes, lengths, and bytes without
  timestamps or absolute paths.
- The installed validator recomputes every digest and rejects record, lock,
  inventory, path, or byte drift.

## Validation evidence

The Feature 015 suite passes all 95 skill-owned test files with receipt
fingerprint
`4d7881a8cdb44d4f8cbbb7e995d8384f8d07968a4bdf0d892bbfb30ef0e47d9f`.
It covers 44 semantic graphs with 221 nodes, 220 deterministic evaluation
scenarios, six offline provider-neutral protocol scenarios, native source and
installed-layout smoke checks, compatibility, security boundaries, SDD
traceability, canonical machine-data checks, 46 documentation tests, a strict
site build, rendered-link validation, and diff hygiene.

Exact compatibility passes for Harness API `4.0.0`, 12 protected contracts, 44
skills, and five modules. Protected CI, the remote tag, and a fresh tagged
native installation remain post-publication signals and are recorded after the
tag exists.

## Compatibility and migration

Harness API `4.0.0` remains a hard cut. Read [Migrate to
4.0](../how-to/migrate-4.0.md) before updating. Pre-v4 machine plans, state,
journals, receipts, manifests, and configuration are retained only as
historical evidence and must be regenerated from authoritative sources.
Human-authored specifications and product source remain consumer-owned.

Consumers of `v4.0.0` should update to `v4.0.1`. Confirm any root legacy lock
is installer-owned before removing that exact file, then run the native
installer and commit the new TOON record, lock, and managed inventory.

## Known limitations

- Provider-executed certification still requires a release-owner receipt that
  names provider, host, model, execution identity, scores, effect receipts, and
  recovery evidence. DEC-008 permits publication with that certification
  pending and forbids presenting offline evidence as provider execution.
- Filesystem journals are local durability, not a distributed transaction
  system. External effects still require idempotent host operations and
  accountable effect receipts.
- Native installation is validated only for project-scoped Codex. Other hosts
  and global scope remain separate conformance work.
- GitHub branch protection, organization policy, deployment authority, and
  production acceptance remain external controls.

## Rollback

Restore the consumer's previously accepted installation commit, validate its
exact managed inventory and provenance, and preserve failed v4 run and
validation artifacts. Publish corrections as new immutable history; never move
or rewrite a consumed release tag.
