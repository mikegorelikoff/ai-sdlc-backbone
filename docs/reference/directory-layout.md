---
title: Directory layout
description: Repository surfaces and the kind of delivery contract each one owns.
---

```text
ai-sdlc-harness/
├── skills/                 # Portable workflow packages
│   ├── ai-sdlc-shared-runtime/ # Single installable deterministic runtime
│   └── ai-sdlc-*/          # SKILL.md router, steps manifest/files, scripts, tests, references
├── modules/                # Versioned capability manifests
├── guides/                 # Internal legacy authoring notes; non-canonical
├── concepts/               # Internal design notes; non-canonical
├── docs/                   # Canonical public docs and generated catalogs
├── specs-refiniment/       # PM/BA/QA/Delivery refinement workspaces
├── specs/                  # Developer implementation SDD workspaces
├── compatibility/          # Release compatibility baseline
└── .github/workflows/      # CI and Pages automation
```

The historical `specs-refiniment` spelling is a compatibility-preserved canonical route. Migration helpers, rather than ad hoc renames, own any future transition.

Every installable skill contains `steps/manifest.toon`. `SKILL.md` selects a
phase rather than embedding the full procedure; the agent then loads only the
declared prepare, execute, validation, handoff, or domain-specific step. Step
paths remain inside their owning skill package and therefore install in both
`skills/` and `.agents/skills/` layouts without repository-only links.

Root `concepts/` and `guides/` are retained for repository history and internal
design context. Every file carries a canonical-public-docs marker and must point
readers to `docs/`; public onboarding never depends on those folders.
