---
name: ai-sdlc-requirements-discovery
description: Analyze raw feature or task requirements, compare business solution options using relevant precedents, and prepare prioritized stakeholder questions with evidence-gathering methods. Use before detailed specification when the request or business approach is still unclear. Supports --quick-flow and --full-flow.
---

# ai-sdlc-requirements-discovery: Requirements Discovery Assistant

Use this optional assistant for rough notes, feedback, tickets or an unclear
feature request. It can complete a useful discovery packet while answers are
still missing. Product choices remain proposals until the accountable owner
accepts them.

Read [the output contract](references/output-contract.md) when composing or
validating the packet. It includes a compact stakeholder-question example.

Use `scripts/requirements_discovery.py` for source preparation, draft scaffolding,
validation, finalization and freshness checks. Business reasoning remains draft
data; the helper owns canonical outputs. Read [the machine contract](references/discovery.schema.toon)
and [valid draft example](references/example-draft.toon) only when filling a draft.

## 0. Skill Card

- Skill name: `ai-sdlc-requirements-discovery`
- Primary audience: BA
- Supporting audience: PM, PO, Dev, QA
- Audience tags: BA, PM, PO, Dev, QA
- SDLC stage: Requirements discovery before specification
- Purpose: Turn raw feature or task inputs into a sourced problem analysis, business options, and an actionable stakeholder elicitation plan.
- Output: Source-bound context, validated TOON discovery packet, business options, stakeholder questions, and conditional handoff

## Step Selector

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `preflight` | `prepare` | none | `bound-discovery` | [`steps/01-prepare.md`](steps/01-prepare.md) — `required` |
| `context` | `clarify`, `route` | `preflight` | `collect-requirements-evidence` | [`steps/02-context.md`](steps/02-context.md) — `required` |
| `execute` | `execute` | `context` | `analyze-business-options` | [`steps/02-execute.md`](steps/02-execute.md) — `on-demand` |
| `validate` | `validate` | `execute` | `validate-discovery` | [`steps/03-validate-and-handoff.md`](steps/03-validate-and-handoff.md) — `before-completion` |
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
