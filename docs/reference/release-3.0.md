---
title: Release 3.0 candidate
description: Scope, compatibility, validation, migration, and rollback for v3.0.0-rc.2.
---

# Release `v3.0.0-rc.2`

`v3.0.0-rc.2` packages the guided Explore→Apply workflow, role-aware
progressive disclosure, one installable runtime, and native OKF v0.2 artifact
bundles accumulated after `v2.1.0`.

This candidate supersedes `v3.0.0-rc.1`. It keeps the same Harness API and
feature scope while correcting protected CI: compatibility checks now receive
the complete tagged history, and remote installation smoke targets the
published v3 package contract.

## Delivered scope

- `ai-sdlc-flow/v3` selects exactly one active role and action, exposes
  prerequisites and handoffs, loads only the selected steps/references, and
  rejects stale Apply fingerprints.
- All 44 skills use validated skill-owned step manifests while keeping concise
  `SKILL.md` routers and direct skill invocation.
- The shared runtime, tests, install smoke, schemas, and deterministic helpers
  are packaged under `ai-sdlc-shared-runtime`.
- Durable lifecycle, change, context, evidence, and workflow writers use the
  shared OKF v0.2 profiles, provenance, bundle indexes, and conformance checks.
- Feature bundles use local `index.md`; project context lives under
  `_ai_sdlc/context/`; legacy runtime fallbacks are removed.
- Harness API and bundled module compatibility move to `3.0.0`.

## Validation evidence

Feature 013 passed its reviewed 11-command full-flow validation plan: flow
tests, the complete shared-runtime suite, OKF bundle conformance, all step
manifest checks, full/selective/global installation smoke, generated
documentation, compatibility, SDD validation, and diff hygiene. Release
publication additionally runs module discovery, commit-history compatibility,
documentation tests, strict MkDocs build, rendered-link checks, and a clean
source installation smoke.

Protected GitHub Actions and the remote tagged installation are verified after
publication because those signals do not exist before the tag and remote
revision are available.

## Compatibility and migration

This is a major release candidate. Read [Migrate to 3.0](../how-to/migrate-3.0.md)
before updating. The removal of navigator, flow v1, `_shared`, root project
context, and workspace human indexes is intentional.

The previous stable `v2.1.0` release remains the rollback target during the
candidate period.

## Known limitations

- Codex-oriented project/global installation and deterministic source checks
  are validated locally; other agent hosts remain candidate environments until
  their complete workflow is recorded.
- GitHub branch protection and organization policy remain external controls.
- OKF verification is not inferred from lifecycle status; independent
  verification evidence must be supplied and refreshed explicitly.

## Rollback

Stop publication before tag/push if any release gate fails. After publication,
reinstall the immutable `v2.1.0` revision, restore only consumer-owned
artifacts from the migration backup, and preserve the failed candidate evidence
for a corrected release.
