---
name: ai-sdlc-policy
description: AI SDLC versioned policy-as-code workflow. Use when an AI assistant needs to resolve layered delivery policy, evaluate an action with explainable rules and gates, protect organization minimums from weaker overrides, apply or reject an expiring waiver, or select a reusable assurance profile. Supports `--quick-flow` for deterministic evaluation and `--full-flow` for strict owner and exception review.
---

# ai-sdlc-policy: Explainable Delivery Controls

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Unknown or invalid policy inputs fail closed when they could weaken protection.

## 0. Skill Card

- Skill name: `ai-sdlc-policy`
- Primary audience: Delivery, Security, Architecture, Release
- Supporting audience: Dev, QA, PM, BA
- Audience tags: Delivery, Security, Architecture, Release, Dev
- SDLC stage: Governance and control evaluation
- Purpose: Resolve policy layers with provenance and evaluate actions against
  protected, versioned, waiver-aware rules.
- Output: `_ai_sdlc/policy-resolution.toon` or fingerprint-addressed TOON records
  below `_ai_sdlc/policy-decisions/` when `--write` is requested

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
