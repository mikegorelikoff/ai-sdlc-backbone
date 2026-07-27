---
title: Supported versions
description: Release, harness API, compatibility, and migration support matrix.
---

# Supported versions

| Release | Harness API | Status | Migration |
| --- | --- | --- | --- |
| [`v3.0.0-rc.2`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v3.0.0-rc.2) | `3.0.0` | Current prerelease; role-guided flow, progressive skill steps, canonical runtime, OKF v0.2 bundles, and corrected protected CI | [Migrate to 3.0](../how-to/migrate-3.0.md); evaluate in a bounded pilot |
| [`v3.0.0-rc.1`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v3.0.0-rc.1) | `3.0.0` | Superseded prerelease; package smoke passes, but release CI used incomplete Git history and a stale remote-install contract | Update to `v3.0.0-rc.2` |
| [`v2.1.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v2.1.0) | `2.0.0` | Previous stable release; Apache-2.0 licensed; learning curriculum and community guides included | Remain pinned or review the 3.0 migration |
| [`v2.0.0-rc.1`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v2.0.0-rc.1) | `2.0.0` | Historical prerelease; superseded by `v2.1.0` | [Migrate to 2.0](../how-to/migrate-2.0.md) |
| [`v1.2.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.2.0) | `1.0.0` | Published Git tag; known installed consumer-root defect blocks complete SDD/commit use | Historical comparison only; wait for a corrected reviewed release |
| [`v1.1.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.1.0) | `1.0.0` | Compatible prior tag | Remain on an accepted pin or wait for a corrected reviewed release; do not upgrade to blocked `v1.2.0` |
| [`v1.0.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.0.0) | `1.0.0` | Historical compatible tag | Evaluate `v1.1.0` under local policy, or wait for the corrected release |

The repository version describes the tagged capability set. The Harness API
version protects public skill names, flags, routes, configuration, module
ranges, handoffs, artifact authority, and major data contracts. Release
`v3.0.0-rc.2` intentionally removes navigator and legacy artifact routes, so
consumers must complete the Harness API `3.0.0` migration before enabling its
modules.

The full compatibility helper requires a **harness source checkout**, including
`compatibility/`, `modules/`, `concepts/`, and `skills/ai-sdlc-shared-runtime`. Maintainers run:

```bash
python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_compatibility.py --skip-git-audit --format toon
```

Consumer repositories instead verify the installed inventory and portable
helper entry points described in [Update safely](../how-to/update.md). Pin and
verify the immutable commit behind a reviewed release; a movable tag alone is
not reproducible identity.
