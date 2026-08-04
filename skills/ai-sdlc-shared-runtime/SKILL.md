---
name: ai-sdlc-shared-runtime
description: Portable AI SDLC shared-helper runtime. Use when an AI assistant installs, verifies, diagnoses, or repairs project-scoped AI SDLC skills whose deterministic scripts depend on shared state, artifact, context, path, canonical TOON, semantic graph, StepCard, evaluation, or index modules. This is an installation dependency, not a lifecycle entry point.
---

# ai-sdlc-shared-runtime: Portable Helper Dependency

> Internal AI SDLC dependency, not a client-facing lifecycle skill.
> Do not select it instead of the guided flow or an owning workflow.
> Every installed capability that imports shared helpers must resolve this
> sibling package before it executes.

## 0. Skill Card

- Skill name: `ai-sdlc-shared-runtime`
- Primary audience: agent runners, platform engineers, harness maintainers
- Supporting audience: AI assistants and repository owners diagnosing install failures
- Audience tags: Platform, Maintainer, Dev
- SDLC stage: Installation and cross-lifecycle runtime support
- Purpose: Provide the single deterministic Python runtime used by source checkouts and installed skill sets.
- Output: Read-only runtime verification or an explicit installation blocker

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
