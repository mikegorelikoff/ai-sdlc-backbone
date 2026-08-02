---
title: Install the harness
description: Install AI SDLC Harness from an immutable revision with deterministic TOON-only provenance.
---

# Install the harness

## Goal

Install all 45 Harness skills into one consumer repository, bind them to an
exact Git revision, and produce a portable content-addressed TOON record that
can be verified without a package registry.

## When to use it

Use the one-line path for a first Codex or Claude Code pilot. Use the pinned
path when release review, reproducibility, an approved mirror, or audit evidence
matters. The harness-owned deterministic installer validates only the explicit
`codex-project` and `claude-code-project` profiles.

## Prerequisites

- Git and network access to the reviewed source remote;
- Python `3.10+`;
- Codex or Claude Code configured for the consumer repository;
- permission to add the selected host skill root and `.ai-sdlc/`;
- a clean or understood consumer working tree.

Check the environment:

```bash
git --version
python3 --version
git status --short
```

Stop if Python is older than 3.10, existing changes are not understood, or the
source remote has not passed your trust policy.

## Procedure

### One-line project install

Run this from the consumer repository:

```bash
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-harness/v4.1.0/install.sh | sh -s -- codex-project
```

Use `claude-code-project` for `.claude/skills`. The bootstrap script fetches the
annotated `v4.1.0` tag into a temporary clean
checkout and runs the source-owned installer. It does not invoke npm, a package
registry, or the external Skills CLI. The installer rejects an unclean source,
unknown inventory entries, symbolic links, non-TOON machine artifacts,
unreviewed managed-file differences, digest drift, and undeclared profiles.

### Inspect and install an immutable release

Use this path when you need to inspect the exact source before execution:

```bash
HARNESS_TAG=v4.1.0
HARNESS_TMP="$(mktemp -d)"
HARNESS_SRC="$HARNESS_TMP/ai-sdlc-harness"
git init "$HARNESS_SRC"
git -C "$HARNESS_SRC" remote add origin https://github.com/mikegorelikoff/ai-sdlc-harness.git
git -C "$HARNESS_SRC" fetch --depth 1 origin "refs/tags/$HARNESS_TAG:refs/tags/$HARNESS_TAG"
git -C "$HARNESS_SRC" checkout --detach "$HARNESS_TAG^{commit}"
HARNESS_REV="$(git -C "$HARNESS_SRC" rev-parse HEAD)"
test "$(git -C "$HARNESS_SRC" rev-list -n 1 "$HARNESS_TAG")" = "$HARNESS_REV"
git -C "$HARNESS_SRC" status --short
git -C "$HARNESS_SRC" diff --check
```

Review `install.sh`, the managed inventory, the native installer, and the
selected skill directories. Then run the exact project-scoped install from the
consumer repository:

```bash
AI_SDLC_SOURCE="$HARNESS_SRC" AI_SDLC_REVISION="$HARNESS_REV" "$HARNESS_SRC/install.sh" codex-project
```

The operation stages all managed directories, checks source and staged
digests, preflights every destination, and applies the accepted set with
rollback backups. Existing unrelated skills are left untouched. An existing
managed directory with different content is a hard stop; follow the update
guide instead of overwriting it.

### Understand the installed artifacts

The native install creates only these Harness-owned roots:

```text
<profile-target>/skills/<managed-skill>/
.ai-sdlc/harness-install.toon
.ai-sdlc/harness-install-lock.toon
.ai-sdlc/harness-managed-skills.txt
```

For `codex-project`, `<profile-target>` is `.agents`; for
`claude-code-project`, it is `.claude`. `harness-install.toon` records the
immutable revision, profile, agent, selection, target, inventory, lock, and
installer identity.
`harness-install-lock.toon` contains sorted skill names, canonical installed
paths, and SHA-256 tree digests over relative paths, permission modes, lengths,
and file bytes. It contains no timestamps or machine-specific absolute paths,
so two installations of the same revision produce identical provenance. The
plain-text managed inventory exists for portable shell review; all structured
machine boundaries are TOON.

## Verify

Validate the record, inventory, lock, paths, and installed bytes:

```bash
PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" .agents/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py
"$PYTHON_BIN" .agents/skills/ai-sdlc-flow/scripts/flow.py --help
"$PYTHON_BIN" .agents/skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py --help
git status --short
```

Expected:

- the validator reports a valid install record;
- the managed inventory and lock contain 45 skills;
- every locked content digest matches the installed directory;
- helper usage renders without an import traceback;
- Git shows only the selected host root and `.ai-sdlc/` additions.

After verification, remove only the temporary reviewed checkout:

```bash
rm -rf "$HARNESS_TMP"
```

Review the complete diff and commit exact paths:

```bash
git add .agents/skills .ai-sdlc/harness-install.toon .ai-sdlc/harness-install-lock.toon .ai-sdlc/harness-managed-skills.txt
git diff --cached --check
git diff --cached --stat
git commit -m "chore: install AI SDLC harness"
```

## Trust and network boundary

The one-line convenience command executes the remote shell script from the
immutable `v4.1.0` tag; the script verifies and fetches the same release before
copying skills. Use
the pinned path when your policy requires review before execution. Set
`AI_SDLC_SOURCE` to a clean local checkout from an approved mirror and
`AI_SDLC_REVISION` to its exact HEAD when public GitHub access is unavailable.

The native installer makes no telemetry request. Git, the remote host, the
agent, and the model provider remain separate network and data boundaries. Do not put
credentials, restricted source, prompts, or model payloads into installation
evidence.

Global installation is intentionally outside the validated path. Commit the
project-scoped install so the repository, not workstation-global state, is the
reviewed authority.

## Troubleshooting

| Symptom | Safe response |
| --- | --- |
| `source checkout is dirty` | Fetch a fresh immutable checkout. Do not bypass this for a release install. |
| `managed destination differs` | Preserve `git status`, review local changes, and use the update procedure only after the difference is owned. |
| `legacy installer lock exists` | Run `git status --short`, confirm the diagnostic's exact root file is an installer-owned legacy artifact, then remove only that file before retrying. |
| `source revision mismatch` | Re-resolve the tag and compare its commit with `HARNESS_REV`; never relabel a different checkout. |
| `non-TOON machine artifact` | Stop and inspect the named source file; the v4 installer will not copy it. |
| `installed skill digest differs` | Treat the installation as modified or corrupt; compare with the accepted revision before repair. |
| Python is too old | Install an organization-approved Python 3.10+ runtime or set `AI_SDLC_PYTHON` to one. |
| Git fetch fails | Check approved proxy, DNS, TLS, credentials, or mirror access; do not substitute an unreviewed download. |

## Next step

Complete [your first 30 minutes](../onboarding/first-30-minutes.md), then use
the [safe update guide](update.md) for repair or upgrade. Review
[supported environments](../reference/supported-environments.md) before
claiming another host or scope is supported.
