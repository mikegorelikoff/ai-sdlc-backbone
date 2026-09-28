# Execute — ai-sdlc-spec-state: Specification State & Lifecycle Management

> Selector: execute

## Entry

Enter only after the prepare and context steps pass and this skill is the selected owner for the specification state operation.

## Procedure

## Script Usage

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

## Purpose

Maintain persistent specification state across feature development, repositories, and spec rotations using declarative `.sdlc.toon` configuration.

## Inputs

- Declarative configuration file `.sdlc.toon` in the target project.
- Local feature artifacts (spec, plan, decision log, readable spec) staged in the local repository.
- Shared planning storage repository (local clone or Git remote reference).

## Steps

1. **Verify Configuration**: Load `.sdlc.toon` and validate storage provider, repository identity, and threshold parameters.
2. **Connect Storage**: Resolve local clone directory in `.ai-sdlc/spec-state/storage_repo` or mounted directory.
3. **Execute Requested Operation**:
   - For `fetch`: Resolve latest index, baseline, decision archive, incremental specs, and stage into `.ai-sdlc/spec-state/context/`.
   - For `publish`: Inject metadata and `spec_id`, copy files to `<storage.root>/<repo.id>/`, and commit/push to Git.
   - For `refresh-index`: Inspect structural architecture, modules, and dependencies; generate `YYYYMMDD-<repo>.md` and synchronize.
   - For `rotate`: Compact feature specs into a new baseline, compact decision logs into a new decision knowledgebase, refresh index, and commit atomically.
   - For `cleanup`: Evaluate historical baselines against retention policy (`keep_current_baseline + keep_previous_baselines`), moving older artifacts into `archive/`.

## Exit

All artifacts are deterministically written, verified, and synchronized in the persistent storage repository.
