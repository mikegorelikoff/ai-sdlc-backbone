---
title: AI SDLC Harness
description: Turn a software request into traceable delivery artifacts, implementation, evidence, and handoff.
hide:
  - navigation
---

<div class="product-hero" markdown>
<p class="product-hero__eyebrow">AI SDLC product family · Structure delivery</p>

# AI SDLC Harness

Turn a software request into traceable, reviewable delivery artifacts,
implementation, evidence, and handoff.

Use one guided entry point to understand a request, select the right rigor,
produce bounded artifacts, implement against an explicit plan, verify the
result, and hand off evidence without surrendering human authority.

<div class="product-hero__actions" markdown>
[Get started](start-here/index.md){ .md-button .md-button--primary }
[See how it works](how-it-works/index.md){ .md-button }
</div>
</div>

## The problem

- **Intent gets separated from code.** Requirements and decisions often remain
  in chat history while implementation moves into the repository.
- **AI work is difficult to resume.** A new session or reviewer must reconstruct
  scope, state, evidence, and unfinished work.
- **More automation can obscure authority.** Teams still need visible human
  decisions for scope, risk, exceptions, and release.

The Harness is for developers and cross-functional delivery teams that already
use Git and want AI-assisted changes to remain inspectable. It provides
workflow structure; it does not replace engineering or product judgment.

## How it works

<div class="workflow" aria-label="AI SDLC Harness workflow">
  <div class="workflow-step"><strong>1. Request</strong><span>State the outcome and constraints.</span></div>
  <div class="workflow-step"><strong>2. Explore</strong><span>Inspect evidence and select a route.</span></div>
  <div class="workflow-step"><strong>3. Specify</strong><span>Make requirements and acceptance explicit.</span></div>
  <div class="workflow-step"><strong>4. Plan</strong><span>Connect design, tests, tasks, and ownership.</span></div>
  <div class="workflow-step"><strong>5. Implement</strong><span>Change only the approved scope.</span></div>
  <div class="workflow-step"><strong>6. Verify and hand off</strong><span>Record evidence and the next owner.</span></div>
</div>

Each stage produces or updates repository artifacts that the next stage can
consume. [Explore the detailed workflow](how-it-works/workflow.md) or compare
the [quick, full, and expert paths](how-to/choose-flow.md).

## Five-minute first success

Install the skills into a project for Codex with one command. This path
requires Git and Python `3.10+`:

```bash
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-harness/v4.0.1/install.sh | sh -s -- codex
```

Then validate the resulting TOON provenance:

```bash
python3 .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py
```

The second command must validate all 44 installed skills and their locked
content digests. Then ask your agent to Explore a request without applying changes:

```text
Use ai-sdlc-flow to Explore this request. Show the route, evidence, rigor,
roles, blockers, planned writes, and next checkpoint. Do not Apply until I
approve the card.

Request: add a health endpoint to this service.
```

Success is a reviewable Explore card with a selected feature/workspace/stage,
evidence, rigor, blockers, planned writes, and next checkpoint. Continue with
[the full first-run guide](start-here/first-run.md) before approving Apply.

## What you get

<div class="path-cards" markdown>

- **Connected delivery artifacts**

  Requirements, design, test cases, tasks, decisions, evidence, and handoffs
  remain linkable in the repository.

- **Adaptive rigor**

  Quick flow keeps bounded work light; full flow adds questions, predecessor
  checks, traceability, and complete handoff evidence.

- **Exact skill contracts**

  Each skill is a validated semantic DAG with explicit operations, context,
  gates, side-effects, evidence, recovery, and handoff boundaries.

- **Minimum sufficient context**

  Every ready step gets authority-labeled exact ranges, mandatory-anchor
  recall, selected/skipped reasons, a token budget, and an exact direct-read
  fallback when packing would be unsafe.

- **Human-owned gates**

  People retain responsibility for product intent, risk acceptance, policy
  exceptions, merge, release, and deployment.

</div>

## Choose your path

<div class="path-cards" markdown>

- **New user**

  [Install and run a safe Explore request](start-here/index.md), then complete
  the first-feature tutorial.

- **Evaluator or team lead**

  [Plan a bounded pilot](adoption/index.md), understand the system model, and
  review limitations with explicit success criteria.

- **Advanced user or maintainer**

  [Open Reference](reference/index.md) for exact contracts or
  [Project](project/index.md) for compatibility, releases, audits, and
  contributor guidance.

</div>

## Scope and limitations

<div class="scope-panel" markdown>

Repository tests verify skill contracts, schemas, state transitions, generated
artifacts, compatibility, recovery, and documentation mechanics. They do not
prove faster delivery, improved quality, cost reduction, compliance, or ROI in
your environment. Human review remains required. See
[maturity and limitations](explanation/maturity-limitations.md).

</div>

## AI SDLC product family

<div class="product-family" markdown>

- <span class="status-badge">Current product</span> **AI SDLC Harness** —
  structure delivery from request through evidence and handoff.
- [Context Guard](https://github.com/mikegorelikoff/ai-sdlc-context) — control
  avoidable context growth and retain full evidence locally.
- [AI SDLC Metrics](https://github.com/mikegorelikoff/ai-sdlc-metrics) —
  measure local Codex CLI and Claude Code adoption from available evidence.

</div>

These products are complementary and independently installed. No built-in
technical integration is implied.
