---
title: Compatibility contract
description: Public surfaces protected across additive harness releases and the checks that enforce them.
---

## Protected surfaces

Release candidate `3.0.0-rc.2` implements Harness API `3.0.0` and protects the
public surface established after `v2.1.0`. The flow v2, canonical runtime, and
OKF path changes are the intentional major migration; the resulting skill
inventory, flags, routes, and operating gates remain mechanically protected.

- Installed skill names and package identity.
- Stable `--quick-flow` and `--full-flow` support.
- Canonical refinement and implementation artifact routes.
- Feature state and machine plan locations.
- Configuration schema and protected gate semantics.
- Module manifest schema and harness API range behavior.
- Required compatibility baseline inventory.

## Additive evolution

New skills, optional modules, fields, and documentation may be added when old consumers continue to work. Renames, removals, authority changes, or required new fields are breaking unless a migration and version contract explicitly handles them.

## Mechanical gate

```bash
command -v git
python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_compatibility.py \
  --git-executable /absolute/reviewed/path/to/git --format toon
```

A compatible result reports the release, harness API version, complete protected
skill, flag, and route inventories, skill/module counts, and
`result: compatible`. The gate also audits the exact reviewed release sequence
from `v2.1.0`; an extra, missing, or reordered planned commit fails. Release
notes must still explain meaningful behavior; passing structure alone does not
replace human review.

The Git history audit has no implicit executable lookup. Review the path printed
by `command -v git` and pass that absolute system path. Use
`--skip-git-audit` for structure-only checks that intentionally do not inspect
release history.
