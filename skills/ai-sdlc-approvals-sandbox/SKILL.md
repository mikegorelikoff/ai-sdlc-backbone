---
name: ai-sdlc-approvals-sandbox
description: AI SDLC approvals, sandbox, and command rule workflow. Use when an AI assistant needs to decide whether to request escalated permissions, explain sandbox failures, propose prefix_rule approvals, avoid unsafe command patterns, or document why a command was or was not rerun outside the sandbox. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.
---

# ai-sdlc-approvals-sandbox: Approvals And Sandbox

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-approvals-sandbox`
- Primary audience: Dev
- Supporting audience: QA
- Audience tags: Dev, QA
- SDLC stage: Sandbox escalation decision
- Purpose: Decide, request, and report sandbox escalation for AI SDLC commands only when the sandbox blocks a required action or the task explicitly requires approved external access.
- Output: Sandbox escalation decision record with prefix_rule guidance and residual risk

## Step Selector

Read `steps/manifest.json` and load only the step selected for the current phase, active role, and action. Treat every selected step as normative.

| Selector | Read when | Step | Load rule |
| --- | --- | --- | --- |
| `prepare` | `prepare`, `clarify`, `route` | [`steps/01-prepare.md`](steps/01-prepare.md) | `required` |
| `execute` | `execute` | [`steps/02-execute.md`](steps/02-execute.md) | `on-demand` |
| `validate-and-handoff` | `validate`, `handoff`, `complete` | [`steps/03-validate-and-handoff.md`](steps/03-validate-and-handoff.md) | `before-completion` |

## Progressive Disclosure Contract

- Read the manifest's required entry selector (`prepare`, or `clarify`/`route` for guided flow) before any command, durable write, or lifecycle transition.
- Read an `execute` selector only when performing the selected skill work.
- Read a `validate`, `handoff`, or `complete` selector before reporting completion.
- Do not broad-load unselected steps. If selectors return no match or a validation error, stop and report the blocker.
- Resolve selectors with the canonical `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.
- In a source checkout use `skills/<skill>/...`; in a consumer install use `.agents/skills/<skill>/...`.
