---
name: ai-sdlc-project-context
description: AI SDLC evidence-backed project context and bounded task-pack workflow. Use when an AI assistant needs to onboard to a repository, detect stack and commands, map ownership and test topology, check context drift, conditionally select task sources, exclude secrets, or allocate a freshness-aware context pack within an explicit token budget. Supports `--quick-flow` for focused evidence and `--full-flow` for stricter repository coverage.
---

# ai-sdlc-project-context: Evidence-Backed Repository Memory

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Confirm the repository root and output location before durable writes.
> Do not read, reproduce, or summarize secrets.

## 0. Skill Card

- Skill name: `ai-sdlc-project-context`
- Primary audience: Dev
- Supporting audience: QA, BA, Delivery, AI assistants
- Audience tags: Dev, QA, BA, Delivery
- SDLC stage: Cross-feature repository context
- Purpose: Generate durable repository memory and task-specific, bounded,
  freshness-aware context from explained safe sources.
- Output: `_ai_sdlc/context/project-context.{md,toon}` and optional
  topology and task-pack records below `_ai_sdlc/context/`

## Step Selector

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `preflight` | `prepare` | none | `inspect-and-route` | [`steps/01-prepare.md`](steps/01-prepare.md) — `required` |
| `context` | `clarify`, `route` | `preflight` | `compile-context` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `execute` | `execute` | `context` | `execute-procedure` | [`steps/02-execute.md`](steps/02-execute.md) — `on-demand` |
| `validate` | `validate` | `execute` | `validate-evidence` | [`steps/03-validate-and-handoff.md`](steps/03-validate-and-handoff.md) — `before-completion` |
| `handoff` | `handoff`, `complete` | `validate` | `handoff-result` | [`steps/04-handoff.md`](steps/04-handoff.md) — `before-completion` |

## Progressive Disclosure Contract

- Resolve the phase entrypoint and dependency-ready set with
  `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.
- Read only the emitted StepCard and its selected context. Pass completed step
  IDs back to the selector before requesting the next ready node.
- Treat `direct_read` as an explicit context strategy. Block only when mandatory
  evidence or critical anchors are missing.
- Explore is read-only. After Apply, journal every selected owning-skill step,
  including analysis and validation nodes, before advancing the graph.
- In source use `skills/<skill>/...`; use `.agents/skills/<skill>/...` for
  Codex, `.claude/skills/<skill>/...` for Claude Code, or the project skills
  root recorded in `.ai-sdlc/harness-install.toon` for `agent-project`.
