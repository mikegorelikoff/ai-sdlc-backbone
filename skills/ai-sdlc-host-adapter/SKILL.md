---
name: ai-sdlc-host-adapter
description: AI SDLC host adapter and capability negotiation workflow. Use when an AI assistant needs to validate a host adapter manifest, map portable workflow operations to host-native operations, negotiate capabilities and limits, select deterministic semantic-preserving fallbacks, or explain why a host cannot run a plan. Supports `--quick-flow` and `--full-flow`.
---

# ai-sdlc-host-adapter: Portable Host Negotiation

> Internal AI SDLC skill, not client-facing by default.
> Negotiation describes host behavior; it never invokes the host.

## 0. Skill Card

- Skill name: `ai-sdlc-host-adapter`
- Primary audience: Dev, Delivery, Architecture
- Supporting audience: Security, QA
- Audience tags: Dev, Delivery, Architecture, Security
- SDLC stage: Portable execution handoff
- Purpose: Preserve workflow semantics across hosts with explicit mappings and safe fallbacks.
- Output: `_ai_sdlc/adapters/<adapter-id>/negotiation.toon` and its
  `negotiation.md` human projection

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
- In a source checkout use `skills/<skill>/...`; in a project-scoped install
  use `.agents/skills/<skill>/...`.
