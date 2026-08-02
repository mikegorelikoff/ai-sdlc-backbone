---
title: Policy
description: Human-facing operating guide for ai-sdlc-policy, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-policy`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Governance and control evaluation | Delivery, Security, Architecture, Release | Dev, QA, PM, BA | `core` | `_ai_sdlc/policy-resolution.toon` or fingerprint-addressed TOON records below `_ai_sdlc/policy-decisions/` when `--write` is requested |

## Why it exists

Resolve policy layers with provenance and evaluate actions against protected, versioned, waiver-aware rules.

## Use it when

AI SDLC versioned policy-as-code workflow. Use when an AI assistant needs to resolve layered delivery policy, evaluate an action with explainable rules and gates, protect organization minimums from weaker overrides, apply or reject an expiring waiver, or select a reusable assurance profile. Supports `--quick-flow` for deterministic evaluation and `--full-flow` for strict owner and exception review.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use policy evaluation to create requirements or product decisions. Use the owning refinement or `ai-sdlc-sdd` skill instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Action name and TOON context for evaluation.
- Base policy plus optional organization profile, project, and user layers.
- Explicit owner-approved waiver record when an allowed exception is requested.

## Tell your agent

```text
Use ai-sdlc-policy for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `_ai_sdlc/policy-resolution.toon` or fingerprint-addressed TOON records below `_ai_sdlc/policy-decisions/` when `--write` is requested, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Versioned base, organization, project, and user policy layers.
- A stable action such as `change.apply`, `release.publish`, or
  `command.destructive` and a TOON context object.
- Optional waiver files tied to exact rule IDs, actions, subjects, constraints,
  owners, approvers, decisions, issue times, and expiry times.

## What it may write

- Keep approved policy layers in visible repository-owned paths.
- Write generated resolution and decision records only below `_ai_sdlc/`.
- Never overwrite a source policy or waiver during evaluation.

## Human checkpoints

- Ask when action identity, subject, accountable waiver owner, or decision
  reference is missing.
- Reject unknown fields, operators, layer scopes, and ambiguous rule identity.
- Never infer approval or create a waiver on the requester's behalf.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes use the same fail-closed evaluator and protected-rule semantics.
- Full flow requires explicit review of every matched rule, rejected override,
  required gate, and waiver result.

## Procedural step selectors

The router loads these skill-owned procedures just in time. Read only the selector matching the current phase, active role, and action; a selected step is normative and an unselected step stays out of context.

| Selector | Type | Phases | Roles | Dependencies | Operation | Side effect | Load rule | Step | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `preflight` | `analysis` | `prepare` | `product-manager`, `software-architect` | none | `inspect-and-route` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-policy/steps/01-prepare.md) | establish inputs, authority, lifecycle state, and safe artifact routing |
| `context` | `context` | `clarify`, `route` | `product-manager`, `software-architect` | `preflight` | `compile-context` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-policy/steps/02-context.md) | compile the minimum sufficient context before the owning action |
| `execute` | `action` | `execute` | `product-manager`, `software-architect` | `context` | `execute-procedure` | `workspace-write` | `on-demand` | [`steps/02-execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-policy/steps/02-execute.md) | perform only the selected owning-skill procedure |
| `validate` | `validation` | `validate` | `product-manager`, `software-architect` | `execute` | `validate-evidence` | `none` | `before-completion` | [`steps/03-validate-and-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-policy/steps/03-validate-and-handoff.md) | validate outputs, evidence, acceptance, and residual risk |
| `handoff` | `handoff` | `handoff`, `complete` | `product-manager`, `software-architect` | `validate` | `handoff-result` | `none` | `before-completion` | [`steps/04-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-policy/steps/04-handoff.md) | return a journal-backed owner and next-action handoff |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` or `.claude/skills/<skill>/...` path reported by your profile. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`policy.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-policy/scripts/policy.py) | Resolve layered policy and evaluate explainable waiver-aware decisions. | `python3 skills/ai-sdlc-policy/scripts/policy.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-policy/scripts/policy.py . --resolve --profile high-assurance --format toon
python3 skills/ai-sdlc-policy/scripts/policy.py . --evaluate change.apply --context policy-context.toon --profile regulated --format toon
python3 skills/ai-sdlc-policy/scripts/policy.py . --explain release.publish --context release-context.toon --waiver waiver.toon --format markdown
```

## Success criteria

Complete canonical TOON resolution records contain normalized rules, provenance, source hashes,
protected rule IDs, and a deterministic fingerprint. Decision records contain
the exact action and context fingerprint, matched and waived rules, gates,
reasons, result, evaluation time, and policy fingerprint.

Quality gate:

- Pass when all layers are valid, protected rules remain at least as strict,
  each waiver is current and authorized, and the action result plus gates are
  understood.
- Fail closed on invalid policy, unknown action, protected weakening, malformed
  or expired waiver, and missing context required by a predicate.

## Blockers and recovery

- Non-matching rules remain visible in explain output only when requested.
- Multiple matching deny rules remain deny even if another rule allows.
- A valid waiver suppresses only its named waivable rule, never an entire action.
- Expiry is evaluated at explicit `--as-of` time for reproducible decisions.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Report resolved policy fingerprint, layer provenance, action decision, matched
  rules, required gates, reason codes, and applied or rejected waivers.
- Return validation and handoff summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v2` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read canonical `_ai_sdlc/state.toon` before applying a decision to feature
      work. Policy evaluation does not create or advance feature `state.toon`.
    - A deny or unsatisfied required gate blocks the owning workflow transition.

??? info "Artifact metadata"

    - Policy-related Markdown uses canonical `artifact_metadata` and `metatags`.
    - Machine records use `ai-sdlc-policy-layer/v1`, `ai-sdlc-policy-waiver/v1`,
      `ai-sdlc-policy-resolution/v1`, and `ai-sdlc-policy-decision/v1`.

??? info "Specs index"

    - Read `_ai_sdlc/specs-index.toon` first and use feature-local `index.md` for human
      discovery when evaluation context refers to feature artifacts.
    - Policy evaluation does not refresh either specs index.

## Example

A high-assurance profile may add `security-review` and `fresh-evidence` gates to
`change.apply`. A project layer can add more gates. A user layer cannot remove
those gates or turn a protected `require` into `allow`.

## Source contract

This page is generated from [`skills/ai-sdlc-policy/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-policy/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
