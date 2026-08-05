---
title: Update safely
description: Upgrade a project-scoped installation from an exact release without losing its profile, selection, provenance, or local review.
---

# Update safely

## Goal

Update a verified AI SDLC Harness installation with one cross-platform command
while preserving its recorded agent profile, skills root, optional modules,
TOON provenance, and unrelated project content.

## When to use it

Use this procedure for a same-release repair or an upgrade to a reviewed
release. Run it from the consumer repository that contains
`.ai-sdlc/harness-install.toon`, not from a Harness source checkout.
A **Consumer repository** uses its installed `.agents/skills` or recorded
custom root. A **Source checkout** contains maintainer paths such as
`skills/ai-sdlc-shared-runtime`; do not confuse those execution contexts.

## Prerequisites

- the existing installation is committed or otherwise recoverable;
- `.ai-sdlc/harness-install.toon`, `.ai-sdlc/harness-install-lock.toon`, and
  `.ai-sdlc/harness-managed-skills.txt` are present;
- the target release and migration notes have been reviewed;
- Git and Python `3.10+` are available.

## Procedure

### Establish the consumer baseline

For the Codex profile, validate the current installation and inspect the
working tree:

```bash
PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py
git status --short
```

For Claude Code or a custom `agent-project` root, run the validator from the
recorded skills root instead. Stop if it reports digest drift. The updater
deliberately refuses to overwrite a local skill edit.

### Apply the exact release

On Linux or macOS, run the updater pinned to the reviewed release:

```bash
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-harness/v4.4.0/install.sh | sh -s -- update
```

On Windows PowerShell, use the same release and native Python bootstrap:

```powershell
irm https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-harness/v4.4.0/install.py | py -3 - update
```

`update` verifies the existing TOON record, lock, inventory, and every managed
digest before mutation. It recovers the recorded profile, target, explicit
selection, and optional modules automatically. The target source is still
bound to an annotated tag and exact commit.

The native installer stages and hashes the replacement, keeps rollback backups
during the transaction, preserves unrelated skills, and writes a new
deterministic lock. It does not remove retired directories automatically.
Remove one only when Git proves it is unchanged Harness-owned content.

### Clean up and review

For the Codex profile:

```bash
"$PYTHON_BIN" .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py
git status --short
git diff --check
git diff -- .agents/skills .ai-sdlc
```

Use the recorded root in those commands for Claude Code or a custom agent
profile. Commit the update separately from product changes:

```bash
git add .agents/skills .ai-sdlc/harness-install.toon .ai-sdlc/harness-install-lock.toon .ai-sdlc/harness-managed-skills.txt
git diff --cached --check
git commit -m "chore: update AI SDLC Harness"
```

## Verify

- the installed record validator passes;
- record and lock point to the reviewed target revision;
- the profile, target, selection, and optional modules are unchanged;
- all managed names and digests match;
- no unrelated agent skill or product file changed;
- one bounded Explore flow and the relevant project validation pass.

Maintainers validating a source checkout must also run the canonical release
suite and native installed-layout smoke before publishing. Consumer
repositories must not substitute source-only tests for their installed
validator.

## Troubleshooting

| Symptom | Safe response |
| --- | --- |
| Installed skill digest differs | Preserve the diff and identify its owner; the updater will not overwrite it. |
| Existing metadata is missing or unsafe | Restore the committed `.ai-sdlc` record, lock, and inventory before updating. |
| Target revision does not match the tag | Stop and resolve remote/tag integrity before running installer code. |
| Replacement is interrupted | Inspect Git status and rerun the same exact target after confirming no unowned content was touched. |
| Retired directory remains | Compare it with the prior accepted revision; remove only confirmed unmodified Harness content. |
| Post-update validation fails | Use the installation commit to restore only the recorded skills root and `.ai-sdlc`, then validate again. |

## Next step

Run the target release migration guide and a low-risk first workflow. Promote
the same installation commit across environments; do not let each workstation
resolve “latest” independently.
