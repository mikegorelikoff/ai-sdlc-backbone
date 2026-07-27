---
name: ai-sdlc-security-testing
description: AI SDLC security testing workflow. Use when an AI assistant is asked for OWASP review, security testing, abuse-case analysis, authz/authn review, input validation review, secret exposure review, or security-focused validation of a diff, endpoint, workflow, or subsystem. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.
---

# ai-sdlc-security-testing: Security Testing

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-security-testing`
- Primary audience: Dev
- Supporting audience: QA, Security, BA
- Audience tags: Dev, QA, BA
- SDLC stage: Security review / abuse-case validation
- Purpose: Review AI SDLC diffs, endpoints, workflows, provider integrations, and configs for concrete security findings, abuse paths, trust-boundary failures, and missing security validation. When the output makes OWASP- or standards-based claims, verify them against current primary sources before presenting them as authoritative guidance.
- Output: Security findings, trust-boundary analysis, standards-backed notes, validation gaps, and fixes

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
