---
name: ai-sdlc-conventional-commit
description: AI SDLC Conventional Commit workflow. Use when an AI assistant drafts, validates, reviews, or fixes commit messages in this repository, especially when commits must include SDD spec references, validation summaries, or safe conventional commit subjects. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.
---

# ai-sdlc-conventional-commit: Conventional Commit Message

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-conventional-commit`
- Primary audience: Dev
- Supporting audience: PM, BA, QA
- Audience tags: Dev, PM, BA, QA
- SDLC stage: Commit message drafting
- Purpose: Draft, validate, or repair an AI SDLC commit message that uses Conventional Commit syntax and includes SDD, business, implementation, testing, and validation traceability when the change is medium or large.
- Output: Conventional Commit subject/body with traceability and validation summary

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
- In a source checkout use `skills/<skill>/...`; in a Codex project install
  use `.agents/skills/<skill>/...`, and in a Claude Code project install use
  `.claude/skills/<skill>/...`.
