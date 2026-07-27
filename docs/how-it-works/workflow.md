---
title: Delivery workflow
description: Follow the verified AI SDLC Harness path from request through exploration, specification, implementation, evidence, and handoff.
---

# Delivery workflow

The primary workflow connects seven outcomes. Exact skill ownership varies by
request, role, and rigor; `ai-sdlc-flow` is the recommended entry point when
you do not already know the owning skill.

<div class="workflow" aria-label="Request to handoff workflow">
  <div class="workflow-step"><strong>Request</strong><span>State the intended outcome and constraints.</span></div>
  <div class="workflow-step"><strong>Explore</strong><span>Inspect repository evidence, risks, roles, and route.</span></div>
  <div class="workflow-step"><strong>Specify</strong><span>Record requirements, acceptance, and boundaries.</span></div>
  <div class="workflow-step"><strong>Plan</strong><span>Connect design, tests, tasks, decisions, and order.</span></div>
  <div class="workflow-step"><strong>Implement</strong><span>Execute only approved, bounded tasks.</span></div>
  <div class="workflow-step"><strong>Verify</strong><span>Run focused checks and record exact evidence.</span></div>
  <div class="workflow-step"><strong>Handoff</strong><span>Transfer state, findings, authority, and next action.</span></div>
</div>

## What moves between stages

Markdown provides reviewable requirements, designs, test cases, plans, tasks,
decisions, and validation reports. Compact TOON state helps agents resume and
route work. Deterministic helpers scaffold, validate, index, and migrate these
records. The [artifact authority model](../explanation/artifact-authority.md)
defines which source controls when representations disagree.

## Human and agent responsibilities

An agent may inspect evidence, draft artifacts, execute approved tasks, and run
validation within its granted scope. People remain accountable for product
intent, material scope, trade-offs, exceptions, security and privacy
acceptance, merge, release, and deployment.

## Choose rigor

Use quick flow for low-risk, bounded work and full flow when missing context,
dependencies, traceability, or handoffs require stronger checks. Direct expert
skill invocation is supported when you already understand the exact contract.
See [Choose a flow mode](../how-to/choose-flow.md).

Next, follow the [first-feature tutorial](../tutorials/first-feature.md) or open
the [workflow reference](../reference/workflow-map.md).
