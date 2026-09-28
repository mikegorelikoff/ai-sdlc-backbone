# Validate and Handoff — ai-sdlc-spec-state: Specification State & Lifecycle Management

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected synchronized artifacts, status metrics, or rotated state.

## Procedure

## Output Spec

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

## Examples

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

## Edge Cases

- If storage repository is offline or credentials fail, enter fail-open mode: log an error message and allow local development to proceed against staged context.
- If the repository index does not exist, require index generation before proceeding with feature development.
- If index age exceeds `refresh_index_after_days` (14 days), notify the user and recommend `refresh-index`.
- If feature specifications since the last baseline exceed 50 (or version changes), prompt for atomic baseline rotation.
- If concurrent edits in storage create merge conflicts, do not force-push; report the conflict and ask for human resolution.
- Retention cleanup should never delete unarchived artifacts when `cleanup_archived_artifacts: false`.

## Exit

Status is reported and specification context is cleanly handed off to downstream SDD skills.
