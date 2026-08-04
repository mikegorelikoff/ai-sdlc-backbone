---
name: ai-sdlc-research
description: Optional AI SDLC research workflow. Use when an AI assistant needs to investigate a customer, market, domain, technology, regulation, competitor, operational question, or implementation uncertainty and produce a routed source inventory plus synthesized findings with confidence, limitations, open questions, and delivery trace targets. Supports `--quick-flow` for focused evidence and `--full-flow` for multi-source and source-diversity gates.
---

# ai-sdlc-research: Sourced Delivery Evidence

> Optional domain skill, not required by the core module.
> Every rule below is important to follow. None of it can be skipped.
> Research informs decisions; it does not silently become a requirement or approval.

## 0. Skill Card

- Skill name: `ai-sdlc-research`
- Primary audience: Research, PM, BA, Architecture
- Supporting audience: Dev, QA, Security, Delivery
- Audience tags: Research, PM, BA, Architecture, Dev
- SDLC stage: Discovery, refinement, and design evidence
- Purpose: Preserve questions, sources, findings, confidence, and limitations.
- Output: `research.md` and `_ai_sdlc/research.toon`

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
