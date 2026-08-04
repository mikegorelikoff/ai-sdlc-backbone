---
title: Start here
description: Install AI SDLC Harness, run a safe first Explore request, verify the result, and choose a next path.
---

# Start here

Use this path if you are installing AI SDLC Harness for the first time. The
recommended default is a project-scoped install followed by a read-only
`ai-sdlc-flow` Explore request.

## Recommended path

1. Check the [prerequisites](prerequisites.md).
2. [Run the one-line installer](../how-to/install.md) in one evaluation project.
3. [Run your first request](first-run.md) without applying changes.
4. Verify the installed skills and the Explore card.
5. Continue to the [first-feature tutorial](../tutorials/first-feature.md).

You do not need to understand every skill before starting. The flow entry point
selects the owning path and shows the planned writes before Apply.

From the project you want to evaluate, run the primary Codex install action:

```bash
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-harness/v4.4.0/install.sh | sh -s -- codex-project
```

Keep verification as the next separate step in the [install guide](../how-to/install.md).
That guide also provides native Windows, Claude Code, and configurable
Agent Skills-compatible host commands.

## Choose a next path

- New to AI-assisted delivery: follow the [learning path](../start.md).
- Working in an existing repository: use the
  [existing-project tutorial](../tutorials/existing-project.md).
- Evaluating team adoption: run a [bounded pilot](../adoption/pilot.md).
- Already know the owning skill: use the
  [skills overview](../reference/skills-overview.md).

If installation or state checks fail, use
[troubleshooting and recovery](../operations/troubleshooting.md).
