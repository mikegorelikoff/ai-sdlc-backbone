---
title: Supported environments
description: Distinguish validated Harness environments from portable but unverified host combinations.
---

# Supported environments

Support is an evidence claim, not a synonym for copying a directory. Use this
page before installation or rollout.

## Runtime requirements

| Component | Required | Why |
| --- | --- | --- |
| Git | Current supported release | Resolve immutable source, branch, diff, and preserve evidence |
| Python | `>=3.10` | Run the native installer and deterministic helpers |
| Agent host | Project-scoped host | Discover its configured Agent Skills directory containing `SKILL.md` packages |
| Network | Git remote during first install | Fetch the reviewed Harness tag; an approved local mirror may replace it |

The native installer does not require Node.js, npm, a package registry, or a
third-party skill installer.

## Tested combinations

| Environment | Evidence | Status |
| --- | --- | --- |
| Ubuntu 24.04, Python 3.10 and 3.13 | Repository workflow, portable installer matrix, and native installed-layout smoke | Configured; support depends on the published workflow result |
| macOS 15, Python 3.10 | Portable Python bootstrap, custom profile, named-profile regression, records, modules, and locks | Configured; support depends on the published workflow result |
| Windows 2025, Python 3.10 | Native Python bootstrap, custom profile, records, modules, and `msvcrt` locking | Configured; support depends on the published workflow result |
| macOS, POSIX shell, Python 3.11 | v4 source gates, deterministic evaluations, docs build, and native installation smoke | v4 mechanically validated locally |
| Codex on macOS, project `.agents/skills/` | v4.1 installed-layout smoke and provider-executed TC-012 on 2026-08-03 | Validated |
| Claude Code profile on macOS, project `.claude/skills/` | v4.1 installed-layout smoke through complete SDD and commit readiness on 2026-08-03 | Package and discovery path validated; model execution is not certified by the Codex receipt |
| Windows Subsystem for Linux | POSIX shell or portable Python bootstrap | Supported by the Linux-compatible package path; workflow result remains release evidence |
| Other Agent Skills-compatible project hosts | `agent-project --skills-root` installs and validates package placement at a safe relative root | Portable package contract; host discovery and model execution are not certified |
| Global or home-directory scope | No installer path; repository containment rejects it | Not supported |

“Mechanically validated” means the exact deterministic workflow passed. It is
not a promise about every provider, model, operating-system release, or agent
host.

## Installation contract

The supported profiles install all 45 skills into the host's project directory:

```bash
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-harness/v4.4.0/install.sh | sh -s -- codex-project
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-harness/v4.4.0/install.sh | sh -s -- claude-code-project
```

Native PowerShell and configurable compatible-host roots use `install.py`:

```powershell
irm https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-harness/v4.4.0/install.py | py -3 - agent-project --skills-root .agent/skills
```

The additive `context-cache` module is opt-in and makes the installed set 46
skills. It uses the same two project-scoped host profiles and requires local
Python SQLite FTS5 support:

```bash
./install.sh codex-project --module context-cache
```

The project also receives:

```text
.ai-sdlc/harness-install.toon
.ai-sdlc/harness-install-lock.toon
.ai-sdlc/harness-managed-skills.txt
```

The record binds agent, target, selection, installer identity, and immutable
revision. The deterministic lock binds every managed installed path to a
SHA-256 tree digest over relative paths, permission modes, lengths, and bytes.
The validator recomputes those digests and rejects symbolic links or non-TOON
machine artifacts.

The project-scoped installation commit is the team authority. Workstation
global state cannot replace it.

## Release support

Consumer instructions resolve annotated tag `v4.4.0` to an exact commit. Local
deterministic, documentation, and installed-layout gates pass before
publication. Protected remote CI and a fresh tagged remote installation are
post-publication signals and must be reported separately.

The release-owned Codex/OpenAI TC-012 receipt is stored with specification 016.
It certifies only the recorded provider, host, model family, scenario version,
execution identity, and evidence. Offline protocol checks remain non-certified.

## Evidence checklist

- [ ] Git and Python meet the required versions.
- [ ] Installation resolves a reviewed immutable revision.
- [ ] The exact project profile and target are named in pilot evidence.
- [ ] The install-record validator recomputes all managed digests successfully.
- [ ] Flow and SDD helper usage commands succeed.
- [ ] One complete workflow passes in a disposable repository.
- [ ] Unsupported combinations and skipped tests are recorded.

See [Install the harness](../how-to/install.md), [Troubleshooting and
recovery](../operations/troubleshooting.md), and [Governance and
trust](../operations/governance.md).
