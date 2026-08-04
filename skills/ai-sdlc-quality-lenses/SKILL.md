---
name: ai-sdlc-quality-lenses
description: AI SDLC reusable quality-lens workflow. Use when an AI assistant needs to challenge a requirement, design, plan, test strategy, change, or delivery artifact through pre-mortem, adversarial, edge-case, stakeholder-conflict, reversibility, abuse-case, operational-failure, or assumption lenses and finalize evidence-backed findings with ownership and traceability. Supports `--quick-flow` for selected high-value lenses and `--full-flow` for the complete applicable registry.
---

# ai-sdlc-quality-lenses: Traceable Cross-Artifact Review

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Findings are proposals for review, not authority to change source artifacts.

## 0. Skill Card

- Skill name: `ai-sdlc-quality-lenses`
- Primary audience: BA, QA, Dev, Delivery
- Supporting audience: PM, Architecture, Security
- Audience tags: BA, QA, Dev, Delivery, PM
- SDLC stage: Cross-lifecycle quality review
- Purpose: Apply reusable challenge lenses and finalize evidence-backed findings.
- Output: `quality-lens-report.md` and `_ai_sdlc/quality-lens-report.toon`

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
