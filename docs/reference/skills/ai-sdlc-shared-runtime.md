---
title: Shared Runtime
description: Human-facing operating guide for ai-sdlc-shared-runtime, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-shared-runtime`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Installation and cross-lifecycle runtime support | agent runners, platform engineers, harness maintainers | AI assistants and repository owners diagnosing install failures | `core` | Read-only runtime verification or an explicit installation blocker |

## Why it exists

Provide the single deterministic Python runtime used by source checkouts and installed skill sets.

## Use it when

Portable AI SDLC shared-helper runtime. Use when an AI assistant installs, verifies, diagnoses, or repairs project-scoped AI SDLC skills whose deterministic scripts depend on shared state, artifact, context, path, canonical TOON, semantic graph, StepCard, evaluation, or index modules. This is an installation dependency, not a lifecycle entry point.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use shared helpers as a lifecycle entry point. Use `ai-sdlc-flow` Explore or the owning skill instead.
- Do not patch installed copies ad hoc. Use the authorized install or update workflow and the canonical runtime package instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- The installed skills root, normally `.agents/skills/` for a project-scoped
  universal installation.
- The consumer repository root.
- The downstream skill script that failed or must be verified.
- The installed package revision or trusted source identity when known.

## Tell your agent

```text
Use ai-sdlc-shared-runtime for <target>.
Do not select a flow flag independently; preserve the mode of the owning downstream skill as described below.
Read the required evidence,
produce or report Read-only runtime verification or an explicit installation blocker, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Resolve the current skill file and its sibling skills root.
- Locate `ai-sdlc-shared-runtime/scripts/` under that root.
- Select the smallest downstream helper that exercises the reported dependency.
- Preserve the consumer repository as the helper's working directory.

## What it may write

- This skill creates no refinement or implementation artifact.
- Read installed files from the agent-owned skills root and consumer evidence
  from the current repository.
- Do not write `specs-refiniment/`, `specs/`, `_ai_sdlc/state.toon`, or an
  `_ai_sdlc/specs-index.toon` during runtime verification.
- Route repair to the canonical install/update workflow and lifecycle work to
  the owning skill.

## Human checkpoints

- Ask only when the installed skills root or failing downstream script cannot
  be located safely.
- Distinguish a missing runtime package from a corrupt runtime copy, missing
  Python, an unsupported package revision, and an application-level failure.
- Never infer that an import failure is permission to download or execute an
  unreviewed replacement.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- This package has no independent quick/full lifecycle flow.
- Preserve `--quick-flow` and `--full-flow` flags for the downstream owning
  skill; this runtime must not reinterpret them.
- Verification is read-only. Reinstallation or repair requires the same human
  authority and trusted source used for installation.

## Procedural step selectors

The router loads these skill-owned procedures just in time. Read only the selector matching the current phase, active role, and action; a selected step is normative and an unselected step stays out of context.

| Selector | Type | Phases | Roles | Dependencies | Operation | Side effect | Load rule | Step | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `preflight` | `analysis` | `prepare` | `software-engineer` | none | `inspect-and-route` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/steps/01-prepare.md) | establish inputs, authority, lifecycle state, and safe artifact routing |
| `context` | `context` | `clarify`, `route` | `software-engineer` | `preflight` | `compile-context` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/steps/02-context.md) | compile the minimum sufficient context before the owning action |
| `execute` | `action` | `execute` | `software-engineer` | `context` | `execute-procedure` | `workspace-write` | `on-demand` | [`steps/02-execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/steps/02-execute.md) | perform only the selected owning-skill procedure |
| `validate` | `validation` | `validate` | `software-engineer` | `execute` | `validate-evidence` | `none` | `before-completion` | [`steps/03-validate-and-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/steps/03-validate-and-handoff.md) | validate outputs, evidence, acceptance, and residual risk |
| `handoff` | `handoff` | `handoff`, `complete` | `software-engineer` | `validate` | `handoff-result` | `none` | `before-completion` | [`steps/04-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/steps/04-handoff.md) | return a journal-backed owner and next-action handoff |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| None | This capability is instruction-only. | Use the agent prompt below. | Follow artifact routing. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

- Verify the canonical runtime in a harness source checkout:

  ```bash
  python3 -m unittest discover -s skills/ai-sdlc-shared-runtime/tests -p 'test*.py' -v
  ```

- Verify every skill-owned test file, including hyphenated package paths:

  ```bash
  python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_test_suite.py \
    --format toon
  ```

- Verify an installed downstream helper from a consumer repository:

  ```bash
  python3 .agents/skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py --help
  ```

- Validate all source or installed step manifests without loading their
  procedures:

  ```bash
  python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py \
    --validate-all --format toon
  ```

- Select one bounded procedure with `ai_sdlc_steps.py --skill <name>
  --phase <phase> [--role <canonical-role>] [--action <action>]`.
- A missing `ai-sdlc-shared-runtime/scripts/` directory, incomplete package, import
  traceback, or non-zero helper smoke result is a blocker.

## Success criteria

A passing verification reports:

```text
runtime: present
downstream helper: executable
consumer root: preserved
mutation: none, or disposable fixture only
next: owning lifecycle skill
```

Quality gate:

- Pass when the canonical runtime inventory is complete and an installed
  downstream helper imports and executes successfully.
- Fail when inventory exists but imports fail, the runtime is installed under a
  different root, package files are inconsistent, or verification mutates real delivery
  artifacts.

## Blockers and recovery

- Source and installed layouts use the same runtime package contract; only the
  skills-root prefix differs.
- A project may expose host-specific symlinks, but all selected skill folders
  and the runtime must resolve to compatible bytes.
- Installing only one downstream skill without this dependency is incomplete.
- `--help` proves importability, not correctness of a consumer feature; run the
  downstream workflow's own validation for that claim.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Report the installed skills root, runtime path, checked downstream script,
  exact command, exit status, and any missing module.
- Return progress, blockers, and recommendations directly in the active agent response.
- Before the final response, emit the `ai-sdlc-handoff/v2` contract with
  `result`, `blockers`, `next_required`, and `next_optional`; every action
  includes `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or a runtime status artifact.
- Do not claim an installation is healthy from inventory alone; execute a
  representative downstream helper.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - This runtime is a utility and never begins or completes a feature stage.
    - It may load `ai_sdlc_state_machine` for another skill, but it must not mutate
      lifecycle state on its own.
    - Use `state.toon` only through the downstream owning workflow.

??? info "Artifact metadata"

    - Runtime verification is ephemeral and carries no `artifact_metadata` or
      `metatags`.
    - The packaged helpers preserve the downstream skill's existing metadata and
      authority contracts; they do not create a second source of truth.

??? info "Specs index"

    - The runtime exposes feature-local OKF `index.md` and compact workspace TOON
      helpers but does not rebuild them during read-only routing.
    - Index reads and writes remain owned by the selected lifecycle workflow.

## Example

Valid diagnosis:

```text
The SDD helper cannot import ai_sdlc_artifact_helper because the shared runtime
package is absent. Reinstall the complete pinned package, then rerun --help.
```

Invalid diagnosis:

```text
Copy one module from an arbitrary checkout into the installed package and keep
working.
```

Reject the invalid path because it bypasses package provenance and can mix
incompatible runtime bytes.

## Source contract

This page is generated from [`skills/ai-sdlc-shared-runtime/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
