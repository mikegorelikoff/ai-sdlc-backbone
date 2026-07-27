---
title: Run your first request
description: Produce and verify a read-only AI SDLC Harness Explore card before approving repository writes.
---

# Run your first request

This guide helps a first-time user produce one reviewable Explore result
without applying repository changes.

## Goal

Route a small request and inspect the proposed rigor, owners, evidence, writes,
and checkpoint.

## When to use it

Use it immediately after a project-scoped installation or when evaluating the
Harness in an unfamiliar repository.

## Prerequisites

- Complete the [prerequisites](prerequisites.md).
- Install the Harness with the [installation guide](../how-to/install.md).
- Open the project in your supported agent host.

## Procedure

Send this prompt:

```text
Use ai-sdlc-flow to Explore this request. Show the intent, selected
feature/workspace/stage, evidence, rigor, roles, context economics, blockers,
planned writes, next checkpoint, and fingerprint. Do not Apply until I
explicitly approve that card.

Request: add a health endpoint to this service.
```

Review the card. Confirm that the selected scope matches the request and that
every planned write belongs in the evaluation project.

## Verify

The result must identify the feature, workspace and stage, evidence, selected
rigor, roles, blockers, planned writes, and next checkpoint. It must stop
before Apply. Missing fields or immediate writes are not a successful result.

## Troubleshooting

If the agent cannot find `ai-sdlc-flow`, rerun the skill inventory command in
the [installation guide](../how-to/install.md). If state or predecessor checks
fail, use [troubleshooting and recovery](../operations/troubleshooting.md).

## Next step

Complete [Ship a first feature](../tutorials/first-feature.md), or read
[quick, full, and expert paths](../how-to/choose-flow.md) before approving
Apply.
