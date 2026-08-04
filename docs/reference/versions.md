---
title: Supported versions
description: Release, harness API, compatibility, and migration support matrix.
---

# Supported versions

| Release | Harness API | Status | Migration |
| --- | --- | --- | --- |
| [`v4.2.2`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v4.2.2) | `4.1.0` | Current stable release; verifies and installs hash-locked Linux AST runtimes before the complete Python 3.10 and 3.13 CI matrix | No API migration; use this correction for every new or updated installation |
| [`v4.2.1`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v4.2.1) | `4.1.0` | Superseded corrective release; optional module installation works, but graph-required tests run without their pinned runtime in protected CI | Update immediately to `v4.2.2`; do not move or rewrite the original tag |
| [`v4.2.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v4.2.0) | `4.1.0` | Superseded feature release; optional module installation succeeds, but its installed record validator rejects the canonical module selection | Update immediately to `v4.2.1`; do not move or rewrite the original tag |
| [`v4.1.1`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v4.1.1) | `4.1.0` | Previous corrective release; aligns Pages publication with the native project installer | Update to `v4.2.0` for context-cache and AST graph capabilities |
| [`v4.1.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v4.1.0) | `4.1.0` | Superseded feature release; adds scheduling, effect drivers, provider evidence, and two project install profiles | Update to `v4.1.1` or later for the Pages correction |
| [`v4.0.1`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v4.0.1) | `4.0.0` | Previous stable release; adds native deterministic installation and a content-addressed TOON lock to the v4 execution harness | [Migrate to 4.0](../how-to/migrate-4.0.md), then update to the current release |
| [`v4.0.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v4.0.0) | `4.0.0` | Superseded initial release; execution harness is intact, but its external consumer installer creates a non-TOON lock | Update immediately to `v4.0.1`; do not move or rewrite the original tag |
| [`v3.0.0-rc.2`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v3.0.0-rc.2) | `3.0.0` | Previous published prerelease; role-guided flow, progressive skill steps, canonical runtime, and OKF v0.2 bundles | Complete the 4.0 migration before updating |
| [`v3.0.0-rc.1`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v3.0.0-rc.1) | `3.0.0` | Superseded prerelease; package smoke passes, but release CI used incomplete Git history and a stale remote-install contract | Update through `v3.0.0-rc.2`, then migrate to 4.0 |
| [`v2.1.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v2.1.0) | `2.0.0` | Historical stable release; Apache-2.0 licensed; learning curriculum and community guides included | Remain pinned or migrate through 3.0 and 4.0 |
| [`v2.0.0-rc.1`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v2.0.0-rc.1) | `2.0.0` | Historical prerelease; superseded by `v2.1.0` | [Migrate to 2.0](../how-to/migrate-2.0.md) |
| [`v1.2.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.2.0) | `1.0.0` | Published Git tag; known installed consumer-root defect blocks complete SDD/commit use | Historical comparison only |
| [`v1.1.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.1.0) | `1.0.0` | Compatible prior tag | Historical comparison only |
| [`v1.0.0`](https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.0.0) | `1.0.0` | Historical compatible tag | Historical comparison only |

The repository version describes the tagged capability set. The Harness API
version protects public skill names, flags, routes, configuration, module
ranges, handoffs, artifact authority, and major data contracts. The `v4.x`
family intentionally rejects pre-v4 machine contracts and removes alternate
parsers and serializers. Consumers must regenerate managed manifests,
configuration, fixtures, plans, state, journals, and receipts as canonical
TOON before enabling Harness API `4.x` modules or execution.

The full compatibility helper requires a **harness source checkout**, including
`compatibility/`, `modules/`, `concepts/`, and
`skills/ai-sdlc-shared-runtime`. Maintainers run:

```bash
python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_compatibility.py --skip-git-audit --format toon
```

Consumer repositories instead verify the installed inventory and portable
helper entry points described in [Update safely](../how-to/update.md). Pin and
verify the immutable commit behind a reviewed release; a movable tag alone is
not reproducible identity.
