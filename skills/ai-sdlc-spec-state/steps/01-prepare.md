# Prepare — ai-sdlc-spec-state: Specification State & Lifecycle Management

> Selector: prepare, clarify, or route

## Entry

Verify repository context, locate `.sdlc.toon`, and parse/validate the specification state policy.

## Procedure

### 0.1 Required Inputs

- Path to project `.sdlc.toon` configuration file (or repository root for auto-discovery).
- Current feature identifier slug when performing fetch or publish operations.
- Storage repository location and branch reference (`storage.repository`, `storage.branch`).
- Active repository identity and semver version (`repository.id`, `repository.version`).

### 0.2 Clarification Rules

- Resolve discoverable configuration from `.sdlc.toon` before asking.
- When `.sdlc.toon` is missing, deterministically launch wizard mode (`spec_state.py wizard` / `run_wizard`): auto-detect repository identity (`pyproject.toml`, `package.json`, Git remote) and version, prompt for storage location and thresholds, and scaffold the configuration cleanly.
- Pause only when storage repository connectivity or authentication fails and cannot be recovered automatically.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.

### 0.3 Output Rules

- Keep output structured with headings and bullet points.
- Return deterministic status, storage synchronization health, and artifact counts in every response.
- Emit machine-readable format (`--format toon` or `--format json`) when invoked programmatically by downstream skills.
- Before final response, emit the `ai-sdlc-handoff/v2` contract with `result`, `blockers`, `next_required`, and `next_optional`.
- Keep durable writes confined to the configured specification storage path and local staging cache (`.ai-sdlc/spec-state/`).

### 0.4 Artifact Routing

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

## 0.4.1 Runtime Path Resolution

- In a harness source checkout, use `skills/ai-sdlc-spec-state/scripts/spec_state.py`; in a project-scoped consumer installation, resolve it to `.agents/skills/ai-sdlc-spec-state/scripts/spec_state.py`.
- Ensure `ai-sdlc-shared-runtime` is present for TOON serialization and safe I/O.

## 0.5 Feature State Machine

Registered stage: `spec-state`; workspace: `specs`.
Canonical output: synchronized specification hierarchy in `.ai-sdlc/spec-state/context/`.
Required predecessors: none.
Possible downstream consumers: `ai-sdlc-sdd`, `ai-sdlc-flow`, `ai-sdlc-requirements-discovery`.

Follow the shared registered-stage protocol for `check`, `begin`, and evidence-backed `complete`. Keep feature state at `_ai_sdlc/state.toon`.

## 0.6 Artifact Metadata And Metatags

All published artifacts must maintain structured frontmatter including:
- `spec_id`: logical specification identifier across multi-repo features.
- `repository_id`: originating repository identity.
- `version`: repository version at time of artifact generation.
- `ticket_id`: associated tracker ticket when provided.
- `date`: publication date in `YYYYMMDD` format.

## 0.7 Specs Index

- Before starting new feature development, verify repository index freshness using `spec_state.py status`.
- If index is older than configured `refresh_index_after_days` (default: 14 days), regenerate the index before implementation planning.
- When feature specifications since baseline exceed `rotation_spec_threshold` (default: 50) or repository version changes, trigger baseline rotation.

## Execution contract

Read the shared execution contract once for this invocation. Apply its input rules, record material facts, and validate output contracts before completion.

## Exit

Configuration is validated and storage parameters are resolved into an active runtime policy.
