---
name: ai-sdlc-flow
description: Guided AI SDLC Explore then Apply workflow. Use when a contributor needs one readable entrypoint that classifies intent before feature selection, explains context, rigor, roles, workspaces, blockers, and planned writes, then revalidates and starts exactly one lifecycle checkpoint.
---

# ai-sdlc-flow: Guided Explore and Apply

> Internal AI SDLC skill and the recommended repository workflow entrypoint.
> Explore is always read-only. Apply never broadens user, sandbox, policy, or
> owning-skill authority.

## 0. Skill Card

- Skill name: `ai-sdlc-flow`
- Primary audience: Contributor, Dev
- Supporting audience: Product, BA, QA, Engineering, Security, Operations
- Audience tags: Contributor, Dev, Product, BA, QA, Security, Operations
- SDLC stage: Cross-lifecycle guided entry
- Purpose: Replace skill-order guesswork with one auditable Explore decision card and one fingerprinted Apply checkpoint.
- Output: `ai-sdlc-flow/v3` canonical TOON or human Markdown decision card and one bounded Apply result

## Step Selector

This table is generated from `steps/manifest.toon`. The manifest and linked
step documents are canonical; regenerate this projection after graph changes.

| Step | Ready when | Depends on | Operation | Load |
| --- | --- | --- | --- | --- |
| `clarify` | `clarify`, `prepare` | none | `inspect-and-route` | [`steps/clarify.md`](steps/clarify.md) — `required` |
| `route` | `route` | `clarify` | `inspect-and-route` | [`steps/route.md`](steps/route.md) — `required` |
| `execute` | `execute` | `route` | `execute-procedure` | [`steps/execute.md`](steps/execute.md) — `on-demand` |
| `validate` | `validate` | `execute` | `validate-evidence` | [`steps/validate.md`](steps/validate.md) — `before-completion` |
| `handoff` | `handoff` | `validate` | `handoff-result` | [`steps/handoff.md`](steps/handoff.md) — `on-demand` |
| `complete` | `complete` | `handoff` | `handoff-result` | [`steps/complete.md`](steps/complete.md) — `before-completion` |

## Progressive Disclosure Contract

- Resolve the phase entrypoint and dependency-ready set with
  `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.
- Read only the emitted StepCard and its selected context. Pass completed step
  IDs back to the selector before requesting the next ready node.
- Treat `direct_read` as an explicit context strategy. Block only when mandatory
  evidence or critical anchors are missing.
- Explore is read-only. After Apply, journal every selected owning-skill step,
  including analysis and validation nodes, before advancing the graph.
- In a source checkout use `skills/<skill>/...`; in a project-scoped install
  use `.agents/skills/<skill>/...`.
