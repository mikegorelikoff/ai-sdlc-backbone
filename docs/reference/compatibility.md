---
title: Compatibility contract
description: Public surfaces protected across additive harness releases and the checks that enforce them.
---

## Protected surfaces

The published `v4.2.2` source implements Harness API `4.1.0`. It preserves the
hard contract cut from the `3.0.0-rc.2` line: all 46 skills use executable
`ai-sdlc-skill-steps/v2` graphs, and canonical TOON is the sole structured
machine-data representation.

- Installed skill names and package identity.
- Stable `--quick-flow` and `--full-flow` support.
- Canonical refinement and implementation artifact routes.
- Feature state and machine plan locations.
- Configuration schema and protected gate semantics.
- Module manifest schema and the `>=4.0.0,<5.0.0` harness API range.
- Exactly 46 semantic graphs with at least five nodes each, including additive
  scheduler and optional context-cache capabilities introduced after v4.0.1.
- Canonical TOON codec path and `.toon` extension.
- StepCard, per-step context, run, workflow, adapter, and evaluation contract
  identities and canonical bytes.
- Required compatibility baseline inventory.

## Additive evolution

New skills, optional modules, fields, and documentation may be added inside a
compatible major version when existing consumers continue to work. Renames,
removals, authority changes, or required new fields are breaking. They require
a new major version, an explicit decision, source-regeneration guidance, and
failure fixtures. Runtime does not silently coerce older schemas.

## Mechanical gate

```bash
command -v git
python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_compatibility.py \
  --git-executable /absolute/reviewed/path/to/git --format toon
```

A compatible result reports the release, Harness API, machine extension,
protected contract count, semantic graph schema, complete protected skill,
flag, and route inventories, skill/module counts, and `result: compatible`.
The gate decodes and canonicalizes protected contracts, validates module API
ranges, loads every skill graph, and enforces the semantic-node floor.

The optional history gate still audits the exact reviewed published release
sequence from `v2.1.0`; an extra, missing, or reordered planned commit fails.
Release notes must explain meaningful behavior; passing structure alone does
not replace human review or the provider-neutral live evaluation gate.

The Git history audit has no implicit executable lookup. Review the path printed
by `command -v git` and pass that absolute system path. Use
`--skip-git-audit` for structure-only checks that intentionally do not inspect
release history.
