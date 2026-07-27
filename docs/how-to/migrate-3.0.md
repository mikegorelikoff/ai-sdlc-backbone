---
title: Migrate to 3.0
description: Move from Harness API 2.0 to the role-guided flow, canonical runtime, progressive skill steps, and OKF artifact routes.
---

# Migrate to 3.0

Release `v3.0.0-rc.1` introduces Harness API `3.0.0`. Use a disposable branch
and preserve consumer-owned specifications, decisions, evidence, and policy
before changing harness-managed files.

## Breaking changes

- `ai-sdlc-navigator` is removed. Start with `ai-sdlc-flow` Explore or invoke a
  known owning skill directly.
- Flow v1 decision cards are rejected. Run Explore again and apply only the
  resulting `ai-sdlc-flow/v2` fingerprint.
- The installable runtime exists only at
  `.agents/skills/ai-sdlc-shared-runtime`; `_shared` is no longer a runtime
  authority.
- Durable feature artifacts use OKF v0.2 and feature-local `index.md` bundle
  navigation. Workspace `specs-index.md` files are removed.
- Project context moves from root `project-context.md` to
  `_ai_sdlc/context/project-context.md`; runtime fallback to the old path is
  intentionally absent.
- Bundled modules require Harness API `>=3.0.0,<4.0.0`.

## Migration procedure

1. Record the accepted `v2.1.0` revision, installed inventory, and clean Git
   state.
2. Back up consumer-owned `specs/`, `specs-refiniment/`, `_ai_sdlc/`, and
   policy/evidence files.
3. Install `v3.0.0-rc.1` project-scoped from its resolved immutable commit.
4. Remove only harness-managed files reported obsolete by the reviewed install
   diff; do not recursively delete consumer artifact trees.
5. Run the explicit OKF migration check before apply:

   ```bash
   python3 .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_okf.py \
     --migrate specs specs-refiniment --check
   ```

6. Resolve every divergent legacy/canonical path manually. Then run the
   reviewed migration in apply mode.
7. Run flow Explore, validate both affected OKF bundles, and execute the
   project’s focused regression and installation smoke checks.
8. Commit the migration separately from product work.

## Rollback

Restore the accepted `v2.1.0` harness-managed inventory and module range, then
restore consumer artifacts from the pre-migration backup. Preserve failed
migration evidence and do not rewrite or discard feature history.
