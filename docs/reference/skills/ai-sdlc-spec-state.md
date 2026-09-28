---
title: Spec State
description: Human-facing operating guide for ai-sdlc-spec-state, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-spec-state`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Cross-lifecycle specification state persistence and rotation | Software Architect, Software Engineer, Tech Lead | BA, PM, PO, QA | `core` | Synchronized specification context hierarchy (index, baseline, decision archive, incremental specs), published feature artifacts, rotated baselines, and status reports. |

## Why it exists

Keep repository specification context synchronized, compact, fresh, and deterministically accessible for downstream SDD skills without token bloat.

## Use it when

Maintain persistent specification state, repository index freshness, baseline specifications, and decision rotation across feature development and multi-repository delivery. Operates against declarative .sdlc.toon configuration.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use it to invent requirements, author feature implementation code, or bypass the SDD workflow. Use `ai-sdlc-sdd` or the owning refinement skill instead.
- Do not use it as a general Git repository synchronization tool or code branch manager. Use `ai-sdlc-branching` instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Path to project `.sdlc.toon` configuration file (or repository root for auto-discovery).
- Current feature identifier slug when performing fetch or publish operations.
- Storage repository location and branch reference (`storage.repository`, `storage.branch`).
- Active repository identity and semver version (`repository.id`, `repository.version`).

## Tell your agent

```text
Use ai-sdlc-spec-state for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report Synchronized specification context hierarchy (index, baseline, decision archive, incremental specs), published feature artifacts, rotated baselines, and status reports., preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Declarative configuration file `.sdlc.toon` in the target project.
- Local feature artifacts (spec, plan, decision log, readable spec) staged in the local repository.
- Shared planning storage repository (local clone or Git remote reference).

## What it may write

- Persistent feature artifacts are written to the configured Git storage repository under `<storage.root>/<repository.id>/`.
- Standard artifact naming convention:
  - Feature specification: `YYYYMMDD-<feature>-spec.md`
  - Implementation plan: `YYYYMMDD-<feature>-plan.md`
  - Feature decision log: `YYYYMMDD-<feature>-decisions.md`
  - Human-readable specification: `YYYYMMDD-<feature>-readable.md`
- Compact structural index: `YYYYMMDD-<repository.id>.md`
- Compacted baseline specification: `baselinespec-<repository.id>-<version>-YYYYMMDD.md`
- Compacted decision knowledgebase archive: `decision-knowledgebase-<repository.id>-<version>-YYYYMMDD.md`
- In local consumer repositories, context is staged into `.ai-sdlc/spec-state/context/`.

## Human checkpoints

- Resolve discoverable configuration from `.sdlc.toon` before asking.
- When `.sdlc.toon` is missing, deterministically launch wizard mode (`spec_state.py wizard` / `run_wizard`): auto-detect repository identity (`pyproject.toml`, `package.json`, Git remote) and version, prompt for storage location and thresholds, and scaffold the configuration cleanly.
- Pause only when storage repository connectivity or authentication fails and cannot be recovered automatically.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.

## Procedural step selectors

The router loads these skill-owned procedures just in time. Read only the selector matching the current phase, active role, and action; a selected step is normative and an unselected step stays out of context.

| Selector | Type | Phases | Roles | Dependencies | Operation | Side effect | Load rule | Step | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `preflight` | `analysis` | `prepare` | `business-analyst`, `product-manager`, `software-engineer`, `qa-engineer` | none | `validate-configuration` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-spec-state/steps/01-prepare.md) | locate and validate declarative .sdlc.toon configuration |
| `context` | `read` | `clarify`, `route` | `business-analyst`, `product-manager`, `software-engineer`, `qa-engineer` | `preflight` | `fetch-spec-hierarchy` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-spec-state/steps/02-context.md) | retrieve compact specification hierarchy from configured storage |
| `execute` | `mutation` | `execute` | `business-analyst`, `product-manager`, `software-engineer`, `qa-engineer` | `context` | `synchronize-spec-state` | `transactional-write` | `on-demand` | [`steps/03-execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-spec-state/steps/03-execute.md) | execute publish, rotate, refresh-index, or cleanup according to policy |
| `handoff` | `gate` | `validate`, `complete` | `business-analyst`, `product-manager`, `software-engineer`, `qa-engineer` | `execute` | `report-status-and-handoff` | `none` | `before-completion` | [`steps/04-validate-and-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-spec-state/steps/04-validate-and-handoff.md) | emit deterministic status report and hand off context to downstream skills |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` or `.claude/skills/<skill>/...` path reported by your profile. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`spec_state.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-spec-state/scripts/spec_state.py) | Main CLI and Python library interface for ai-sdlc-spec-state. | `python3 skills/ai-sdlc-spec-state/scripts/spec_state.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`spec_state_config.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-spec-state/scripts/spec_state_config.py) | Configuration parser and validator for ai-sdlc-spec-state. | `Imported helper; use the owning skill rather than invoking it directly.` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`spec_state_rotation.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-spec-state/scripts/spec_state_rotation.py) | Rotation engine, freshness evaluation, repository indexing, and retention for ai-sdlc-spec-state. | `Imported helper; use the owning skill rather than invoking it directly.` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`spec_state_storage.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-spec-state/scripts/spec_state_storage.py) | Git storage and artifact hierarchy resolution for ai-sdlc-spec-state. | `Imported helper; use the owning skill rather than invoking it directly.` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

- Scaffold configuration:
  ```bash
  python3 skills/ai-sdlc-spec-state/scripts/spec_state.py init --repo-id <id> --storage-repo <repo>
  ```
- Fetch and stage context hierarchy before feature work:
  ```bash
  python3 skills/ai-sdlc-spec-state/scripts/spec_state.py fetch --feature <name> --format toon
  ```
- Publish feature artifacts before PR:
  ```bash
  python3 skills/ai-sdlc-spec-state/scripts/spec_state.py publish --feature <name> --spec <path> --plan <path> --decisions <path> --readable <path> --ticket <id>
  ```
- Inspect specification status, freshness, and rotation progress:
  ```bash
  python3 skills/ai-sdlc-spec-state/scripts/spec_state.py status --format text
  ```
- Refresh repository structural index:
  ```bash
  python3 skills/ai-sdlc-spec-state/scripts/spec_state.py refresh-index --force
  ```
- Rotate baseline specification and decision knowledgebase:
  ```bash
  python3 skills/ai-sdlc-spec-state/scripts/spec_state.py rotate --force
  ```
- Apply retention cleanup to historical archived artifacts:
  ```bash
  python3 skills/ai-sdlc-spec-state/scripts/spec_state.py cleanup --dry-run
  ```

## Success criteria

Use this specification state report when communicating status to users or downstream workflows:

```text
Spec State:
- Repository: <repo-id> (v<version>)
- Storage: <storage-repo>:<branch>
- Sync status: clean | ahead | behind | diverged
- Repository index: <date> (<age> days old, <status>)
- Latest baseline: <filename> (v<version>, <date>)
- Latest decision archive: <filename> (<date>)
- Incremental feature specs: <count> / <threshold>
- Incremental decision logs: <count> / <threshold>
- Rotation recommendation: none | baseline rotation recommended | version change
- Staged context: .ai-sdlc/spec-state/context/
- Next phase: refinement | implementation | pr-publish
```

Quality gate:
- Pass when storage is synchronized, index freshness is within policy, and required artifacts follow naming and metadata conventions.
- Fail when `.sdlc.toon` is invalid, storage Git connection is unreachable without fallback, or published artifacts escape the designated repository directory.

## Blockers and recovery

- If storage repository is offline or credentials fail, enter fail-open mode: log an error message and allow local development to proceed against staged context.
- If the repository index does not exist, require index generation before proceeding with feature development.
- If index age exceeds `refresh_index_after_days` (14 days), notify the user and recommend `refresh-index`.
- If feature specifications since the last baseline exceed 50 (or version changes), prompt for atomic baseline rotation.
- If concurrent edits in storage create merge conflicts, do not force-push; report the conflict and ask for human resolution.
- Retention cleanup should never delete unarchived artifacts when `cleanup_archived_artifacts: false`.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Keep output structured with headings and bullet points.
- Return deterministic status, storage synchronization health, and artifact counts in every response.
- Emit machine-readable format (`--format toon` or `--format json`) when invoked programmatically by downstream skills.
- Before final response, emit the `ai-sdlc-handoff/v2` contract with `result`, `blockers`, `next_required`, and `next_optional`.
- Keep durable writes confined to the configured specification storage path and local staging cache (`.ai-sdlc/spec-state/`).

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    Registered stage: `spec-state`; workspace: `specs`.
    Canonical output: synchronized specification hierarchy in `.ai-sdlc/spec-state/context/`.
    Required predecessors: none.
    Possible downstream consumers: `ai-sdlc-sdd`, `ai-sdlc-flow`, `ai-sdlc-requirements-discovery`.

    Follow the shared registered-stage protocol for `check`, `begin`, and evidence-backed `complete`. Keep feature state at `_ai_sdlc/state.toon`.

??? info "Artifact metadata"

    All published artifacts must maintain structured frontmatter including:
    - `spec_id`: logical specification identifier across multi-repo features.
    - `repository_id`: originating repository identity.
    - `version`: repository version at time of artifact generation.
    - `ticket_id`: associated tracker ticket when provided.
    - `date`: publication date in `YYYYMMDD` format.

??? info "Specs index"

    - Before starting new feature development, verify repository index freshness using `spec_state.py status`.
    - If index is older than configured `refresh_index_after_days` (default: 14 days), regenerate the index before implementation planning.
    - When feature specifications since baseline exceed `rotation_spec_threshold` (default: 50) or repository version changes, trigger baseline rotation.

## Example

Valid fetch result:

```text
Spec State:
- Repository: payment-service (v1.2.0)
- Storage: vestwell/agent-planning-docs:main
- Sync status: clean
- Repository index: 20260920 (8 days old, fresh)
- Latest baseline: baselinespec-payment-service-1.2.0-20260901.md (v1.2.0, 20260901)
- Latest decision archive: decision-knowledgebase-payment-service-1.2.0-20260901.md (20260901)
- Incremental feature specs: 4 / 50
- Incremental decision logs: 3 / 50
- Rotation recommendation: none
- Staged context: .ai-sdlc/spec-state/context/
- Next phase: implementation
```

Valid rotation result:

```text
Spec State:
- Repository: auth-service (v2.0.0)
- Storage: vestwell/agent-planning-docs:main
- Sync status: clean
- Repository index: 20260928 (0 days old, fresh)
- Latest baseline: baselinespec-auth-service-2.0.0-20260928.md (v2.0.0, 20260928)
- Latest decision archive: decision-knowledgebase-auth-service-2.0.0-20260928.md (20260928)
- Incremental feature specs: 0 / 50
- Incremental decision logs: 0 / 50
- Rotation recommendation: none (rotated 52 specs and 50 decisions)
- Staged context: .ai-sdlc/spec-state/context/
- Next phase: refinement
```

Invalid counter-example:

```text
Published feature spec without version, date, or logical spec_id metadata directly into git root.
```

Reject this because all feature artifacts must be routed to `<storage.root>/<repo.id>/` with structured frontmatter.

## Source contract

This page is generated from [`skills/ai-sdlc-spec-state/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-spec-state/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
