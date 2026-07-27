---
title: Prerequisites
description: Check the tools, repository state, permissions, and review boundaries required before installing AI SDLC Harness.
---

# Prerequisites

Use this checklist before the first project-scoped installation.

- Git and a repository where project-local agent skills are acceptable.
- Node.js `>=22.20.0`, npm, and `npx`.
- Python `3.10+` for Harness helper scripts.
- An agent supported by the Skills CLI; the examples use `codex`.
- Permission to add project-scoped skill files and review their source.
- A clean or understood working tree so generated files are distinguishable.

Check the local tools:

```bash
git --version
node --version
npm --version
python3 --version
git status --short
```

Do not continue if you cannot identify pre-existing changes or if organization
policy forbids fetching and executing the installer. Use the
[pinned, reviewable installation path](../how-to/install.md#inspect-before-installing)
when you need an immutable source revision.

Next, [install the Harness](../how-to/install.md).
