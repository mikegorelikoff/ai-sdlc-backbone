---
title: Update safely
description: Repair or upgrade a project-scoped installation from an exact revision without losing provenance or local review.
---

# Update safely

## Goal

Replace only reviewed Harness-managed skill directories, regenerate
deterministic TOON provenance, and preserve unrelated project and third-party
content.

## When to use it

Use this procedure for a same-revision repair or an upgrade to a reviewed
release. A **Consumer repository** contains the installed `.agents/skills`
tree. A **Source checkout** contains this Harness repository and maintainer
paths such as `skills/ai-sdlc-shared-runtime`. Keep those execution contexts
separate.

## Prerequisites

- the existing installation is committed or otherwise recoverable;
- `.ai-sdlc/harness-install.toon`,
  `.ai-sdlc/harness-install-lock.toon`, and the managed inventory are present;
- the current validator result and Git diff have been preserved;
- the target release and migration notes have been reviewed;
- Git and Python `3.10+` are available.

## Procedure

### Establish the consumer baseline

```bash
PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py
git status --short
git diff -- .agents/skills .ai-sdlc
```

Stop if a managed directory differs from its recorded digest and ownership of
that change is unclear. The validator is expected to fail on a local edit; that
failure is evidence to resolve, not a reason to discard the edit.

### Resolve the exact target

```bash
TARGET_TAG=v4.0.1
TARGET_TMP="$(mktemp -d)"
TARGET_SRC="$TARGET_TMP/ai-sdlc-harness"
git init "$TARGET_SRC"
git -C "$TARGET_SRC" remote add origin https://github.com/mikegorelikoff/ai-sdlc-harness.git
git -C "$TARGET_SRC" fetch --depth 1 origin "refs/tags/$TARGET_TAG:refs/tags/$TARGET_TAG"
git -C "$TARGET_SRC" checkout --detach "$TARGET_TAG^{commit}"
TARGET_REV="$(git -C "$TARGET_SRC" rev-parse HEAD)"
test "$(git -C "$TARGET_SRC" rev-list -n 1 "$TARGET_TAG")" = "$TARGET_REV"
git -C "$TARGET_SRC" status --short
```

For a same-release repair, fetch the exact revision already recorded in
`harness-install.toon` instead of selecting a newer tag.

Compare the old and target managed inventories:

```bash
comm -23 .ai-sdlc/harness-managed-skills.txt "$TARGET_SRC/config/ai-sdlc-managed-skills.txt"
comm -13 .ai-sdlc/harness-managed-skills.txt "$TARGET_SRC/config/ai-sdlc-managed-skills.txt"
```

The first command prints retired managed names; the second prints newly added
names. Review both sets and the target migration guide before replacement.

### Apply the reviewed replacement

The installer normally refuses any differing managed destination. The explicit
environment flag below is the human-reviewed replacement authority:

```bash
AI_SDLC_SOURCE="$TARGET_SRC" \
AI_SDLC_REVISION="$TARGET_REV" \
AI_SDLC_INSTALL_REPLACE=1 \
"$TARGET_SRC/install.sh" codex
```

The native installer stages and hashes all target skills before applying
changes, keeps rollback backups during the operation, preserves unrelated
skills, and writes a new deterministic `harness-install-lock.toon`.

It does not remove retired directories automatically. For each retired name,
compare `.agents/skills/<name>` with the previously accepted revision. Remove
it only when it is confirmed to be an unmodified Harness-owned directory;
retain and document any ambiguous or locally modified directory.

### Clean up and review

```bash
"$PYTHON_BIN" .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py
git status --short
git diff --check
git diff -- .agents/skills .ai-sdlc
rm -rf "$TARGET_TMP"
```

Commit the update separately from product changes:

```bash
git add .agents/skills .ai-sdlc/harness-install.toon .ai-sdlc/harness-install-lock.toon .ai-sdlc/harness-managed-skills.txt
git diff --cached --check
git commit -m "chore: update AI SDLC harness"
```

## Verify

- the install-record validator passes;
- record and lock point to `TARGET_REV`;
- all managed names and digests match;
- additions and retirements match the reviewed inventory comparison;
- no unrelated agent skill or product file changed;
- one bounded Explore flow and the relevant project validation pass.

Maintainers validating a source checkout must also run the canonical release
suite and the native installed-layout smoke before publishing. Consumer
repositories must not substitute source-only test paths for their installed
validator.

## Troubleshooting

| Symptom | Safe response |
| --- | --- |
| Existing managed digest differs before review | Preserve the diff and identify its owner; do not set the replacement flag yet. |
| Target revision does not match the tag | Stop and resolve remote/tag integrity before running installer code. |
| Replacement is interrupted | Inspect Git status and rerun the same exact target after confirming no unowned content was touched. |
| Retired directory remains | Compare it with the prior accepted revision; remove only confirmed unmodified Harness content. |
| Post-update validation fails | Use the installation commit for rollback of only `.agents/skills` and `.ai-sdlc`, then validate the restored record. |

## Next step

Run the target release migration guide and a low-risk first workflow. Promote
the same installation commit across environments; do not let each workstation
resolve “latest” independently.
