---
title: Flow
description: Human-facing operating guide for ai-sdlc-flow, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-flow`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Cross-lifecycle guided entry | Contributor, Dev | Product, BA, QA, Engineering, Security, Operations | `core` | `ai-sdlc-flow/v2` Markdown, TOON, or JSON decision card and one bounded Apply result |

## Why it exists

Replace skill-order guesswork with one auditable Explore decision card and one fingerprinted Apply checkpoint.

## Use it when

Guided AI SDLC Explore then Apply workflow. Use when a contributor needs one readable entrypoint that classifies intent before feature selection, explains context, rigor, roles, workspaces, blockers, and planned writes, then revalidates and starts exactly one lifecycle checkpoint.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use it to Apply before a matching Explore card exists. Use `ai-sdlc-flow` Explore instead for read-only routing.
- Do not use it to bypass lifecycle prerequisites. Use `ai-sdlc-sdd` or the selected owning skill instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Repository root and natural-language intent.
- Canonical `NNN-kebab-case` feature when durable feature work is expected.
- Optional explicit quick/full rigor.
- Optional `--role` and `--action` overrides plus bounded `--team` and `--user`
  configuration layers.

## Tell your agent

```text
Use ai-sdlc-flow for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `ai-sdlc-flow/v2` Markdown, TOON, or JSON decision card and one bounded Apply result, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Repository root and natural-language intent.
- Canonical `NNN-kebab-case` feature when durable feature work is expected.
- Optional explicit quick/full rigor.
- Optional `--role` and `--action` overrides plus bounded `--team` and `--user`
  configuration layers.

## What it may write

- Explore writes no artifact.
- Apply routes refinement only to `specs-refiniment/<feature>` and
  implementation only to `specs/<feature>`.
- The selected owning skill creates artifacts, metadata, decision logs, state,
  and indexes.

## Human checkpoints



Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- `--quick-flow` requests quick rigor when risk and policy permit it.
- `--full-flow` requests full rigor and takes precedence.
- Explore explains every automatic choice or override.

## Procedural step selectors

The router loads these skill-owned procedures just in time. Read only the selector matching the current phase, active role, and action; a selected step is normative and an unselected step stays out of context.

| Selector | Phases | Roles | Load rule | Step | Reason |
| --- | --- | --- | --- | --- | --- |
| `clarify` | `clarify` | `business-analyst`, `product-manager`, `software-architect`, `software-engineer`, `qa-engineer` | `required` | [`steps/clarify.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-flow/steps/clarify.md) | guided flow clarify phase with explicit evidence and exit criteria |
| `route` | `route` | `business-analyst`, `product-manager`, `software-architect`, `software-engineer`, `qa-engineer` | `required` | [`steps/route.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-flow/steps/route.md) | guided flow route phase with explicit evidence and exit criteria |
| `execute` | `execute` | `business-analyst`, `product-manager`, `software-architect`, `software-engineer`, `qa-engineer` | `on-demand` | [`steps/execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-flow/steps/execute.md) | guided flow execute phase with explicit evidence and exit criteria |
| `handoff` | `handoff` | `business-analyst`, `product-manager`, `software-architect`, `software-engineer`, `qa-engineer` | `on-demand` | [`steps/handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-flow/steps/handoff.md) | guided flow handoff phase with explicit evidence and exit criteria |
| `validate` | `validate` | `business-analyst`, `product-manager`, `software-architect`, `software-engineer`, `qa-engineer` | `before-completion` | [`steps/validate.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-flow/steps/validate.md) | guided flow validate phase with explicit evidence and exit criteria |
| `complete` | `complete` | `business-analyst`, `product-manager`, `software-architect`, `software-engineer`, `qa-engineer` | `before-completion` | [`steps/complete.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-flow/steps/complete.md) | guided flow complete phase with explicit evidence and exit criteria |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`flow.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-flow/scripts/flow.py) | Explore an AI SDLC route and optionally apply one revalidated checkpoint. | `python3 skills/ai-sdlc-flow/scripts/flow.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-flow/scripts/flow.py explore \
  --intent "<request>" --feature NNN-feature \
  [--role software-engineer] [--action implementation] --format markdown
```

After the contributor explicitly accepts the displayed JSON card, pass that
same saved card to the separate mutation command:

```bash
python3 skills/ai-sdlc-flow/scripts/flow.py apply \
  --card <accepted-card.json> --execute
```

Use `.agents/skills/` instead of `skills/` in a project-scoped installation.
Without `--execute`, Apply performs verification and reports the single action
it would start. `--execute` is an explicit mutation boundary.

## Success criteria

A successful result produces `ai-sdlc-flow/v2` Markdown, TOON, or JSON decision card and one bounded Apply result and satisfies every output rule and blocker check below.

## Blockers and recovery



On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Return the decision card, blockers, action result, and evidence directly in
  the Codex response.
- Return progress, blockers, and completion directly in the active agent response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; each action includes reason, command, and expected artifact.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    Explore reads `_ai_sdlc/state.toon` but never changes it. Apply may start one
    allow-listed state transition only after fingerprint verification. It cannot
    complete a task, stage, validation, or approval on behalf of an owning skill.

??? info "Artifact metadata"

    Decision cards are ephemeral and do not carry `artifact_metadata` or
    `metatags`. Any artifact created after Apply is owned and formatted by the
    selected downstream skill.

??? info "Specs index"

    Explore reads `_ai_sdlc/specs-index.toon` before broad feature scans and may
    show feature-local OKF `index.md` paths as evidence. It never rebuilds them.
    Apply delegates index updates to the one selected owning skill.

## Example

```bash
python3 skills/ai-sdlc-flow/scripts/flow.py explore \
  --intent "<request>" --feature NNN-feature \
  [--role software-engineer] [--action implementation] --format markdown
```

After the contributor explicitly accepts the displayed JSON card, pass that
same saved card to the separate mutation command:

```bash
python3 skills/ai-sdlc-flow/scripts/flow.py apply \
  --card <accepted-card.json> --execute
```

Use `.agents/skills/` instead of `skills/` in a project-scoped installation.
Without `--execute`, Apply performs verification and reports the single action
it would start. `--execute` is an explicit mutation boundary.

## Source contract

This page is generated from [`skills/ai-sdlc-flow/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-flow/SKILL.md) plus its linked `steps/manifest.json` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
