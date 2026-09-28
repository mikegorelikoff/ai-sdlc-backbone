# Context — Specification State Hierarchy Retrieval

## Entry

Retrieve the current specification state hierarchy from the configured storage repository.

## Procedure

### 2.1 Fetch Specification Context

Connect to configured storage (`storage.repository`, `storage.branch`, `storage.root`):
1. Locate latest repository index (`YYYYMMDD-<repository-id>.md`).
2. Locate latest baseline specification (`baselinespec-<repository-id>-<version>-YYYYMMDD.md`).
3. Locate latest decision knowledgebase archive (`decision-knowledgebase-<repository-id>-<version>-YYYYMMDD.md`), if present.
4. Locate incremental decision logs created after the latest decision archive.
5. Locate incremental feature specifications created after the latest baseline.
6. Assemble active work plans and metadata.

### 2.2 Hierarchical Context Assembly

Construct the compact context hierarchy without flooding tokens:
```text
repository index
        ↓
latest baseline
        ↓
latest decision archive
        ↓
incremental decision logs
        ↓
feature specs after baseline
        ↓
current feature artifacts
```

### 2.3 Local Staging

Cache the fetched artifacts locally in `.ai-sdlc/spec-state/` for fast downstream access by SDD skills.

## Exit

Deterministic specification hierarchy package is assembled and ready for planning or execution.
