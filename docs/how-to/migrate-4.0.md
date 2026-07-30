---
title: Migrate to 4.0
description: Move to executable semantic skill graphs, deterministic per-step context, durable runtime v2, and canonical TOON-only machine contracts.
---

# Migrate to 4.0

Release `v4.0.0` introduces Harness API `4.0.0` as a deliberate hard cut.
Preserve human-authored requirements, decisions, source code, and evidence,
but regenerate harness-managed machine artifacts from their authoritative
sources. The v4 runtime does not include an alternate parser, compatibility
reader, or in-place conversion mode.

## Breaking changes

- Every installable skill now owns an `ai-sdlc-skill-steps/v2` semantic DAG
  with typed nodes, gates, dependencies, side-effect classes, recovery policy,
  and generated concise routing.
- Ready work is exchanged as `ai-sdlc-step-card/v1`; workflow, runtime, host
  adapter, and handoff contracts reject older schemas explicitly.
- Context compiles per step as `ai-sdlc-context-pack/v4` with mandatory
  anchors, authority, exact ranges, critical recall, savings, and direct-read
  fallback.
- Apply execution uses immutable run v2 plans and append-only event journals.
  Existing pre-v4 plans, state projections, journals, and result receipts are
  historical evidence, not resumable v4 state.
- Machine contracts, schemas, fixtures, configuration, manifests, receipts,
  CLI output, and generated catalogs use canonical TOON only.
- Bundled modules require Harness API `>=4.0.0,<5.0.0`.

## Migration procedure

1. Record the accepted current revision, install record, managed skill
   inventory, module ranges, and clean Git state.
2. Create a migration branch and back up consumer-owned `specs/`,
   `specs-refiniment/`, `_ai_sdlc/`, policy, and evidence paths.
3. Fetch annotated tag `v4.0.0`, resolve it to an immutable commit, review the
   release notes and install diff, then install project-scoped skills from that
   detached checkout.
4. Replace only files named by the harness-managed inventory. Preserve
   unrelated skills and every consumer-owned Markdown artifact.
5. Archive pre-v4 machine plans, state, journals, configuration, module
   manifests, and receipts as read-only migration evidence. Do not feed them to
   v4 entry points.
6. Regenerate current configuration, module manifests, feature indexes,
   validation plans, and other required machine artifacts from their
   authoritative source material using installed v4 writers.
7. Run `ai-sdlc-flow` Explore again for any unfinished work. Review its v3
   decision fingerprint and authorize a fresh Apply instead of resuming an old
   run.
8. Validate installed layout, all affected specifications, focused product
   regressions, compatibility, and the canonical TOON gate. Commit the harness
   migration separately from product changes.

## Verification

The migration is complete when all 44 managed skills have v2 manifests, every
required helper starts from the installed layout, no pre-v4 machine artifact
is presented to a v4 entry point, and one Explore produces a context-sufficient
StepCard without durable writes. A reviewed Apply must then create a new
repository-bounded run with ordered journal evidence.

## Rollback

Reset neither shared history nor consumer artifacts. Restore the accepted
pre-migration install revision and managed inventory in a new rollback commit,
restore only files replaced during migration, and keep the v4 attempt plus its
validation evidence for diagnosis. Pre-v4 runtime state may be resumed only by
the matching pre-v4 installation.
