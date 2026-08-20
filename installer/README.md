# AI SDLC Backbone Installer

Secure, license-based installation for **AI SDLC Backbone** — the workflow
backbone for structured AI-assisted software delivery.

> Structure delivery. Control context. Measure adoption.

This package validates your license, downloads an authorized release, verifies
its SHA256 checksum, and installs the product into your project. You do not
need a GitHub account or access to the private source repository.

## Requirements

- Node.js 20 or newer
- Python 3 available as `python3`
- An AI SDLC Backbone license key
- Network access to the licensing service

## Install

From the project you want to configure:

```bash
AI_SDLC_LICENSE_KEY="ASDL-..." npx ai-sdlc-backbone
```

For interactive terminals, you can omit the environment variable and enter
the key at the masked prompt:

```bash
npx ai-sdlc-backbone
```

The environment-variable form is recommended for automation. The installer
deliberately does not accept a license key as a command-line argument, keeping
it out of shell history and process listings.

## Verify

At the end of a successful installation, the installer prints the exact
verification command for the selected profile. Run that command from the
project root to inspect the recorded version and installation state.

## Profiles

The default profile installs project-local Codex skills:

```bash
npx ai-sdlc-backbone --profile codex-project
```

Supported profiles:

| Profile | Destination |
| --- | --- |
| `codex-project` | `.agents/skills` in the project |
| `claude-code-project` | `.claude/skills` in the project |
| `agent-project` | A custom directory provided with `--skills-root` |

Example for a custom agent skills directory:

```bash
npx ai-sdlc-backbone --profile agent-project --skills-root ./agent-skills
```

## Options

```text
ai-sdlc-backbone \
  [--profile PROFILE] \
  [--project-root PATH] \
  [--skills-root PATH] \
  [--version X.Y.Z|latest]
```

- `--project-root PATH` installs into another project; the current directory
  is the default.
- `--version latest` requests the newest version allowed by your license.
- `--version X.Y.Z` requests an exact product version.
- `--skills-root PATH` is required with `--profile agent-project`.

## Environment variables

| Variable | Purpose |
| --- | --- |
| `AI_SDLC_LICENSE_KEY` | License key used for authorization. |
| `AI_SDLC_LICENSE_API` | Licensing API origin; intended for managed or development environments. |
| `AI_SDLC_PYTHON` | Python executable used by the controlled installer. |

## Security model

- The licensing API is authoritative; there is no client-side-only license
  validation or embedded universal secret.
- The key is sent only to the configured licensing API.
- Download grants are short-lived and do not expose GitHub credentials.
- Every artifact is verified against the server-provided SHA256 checksum before
  extraction. A mismatch aborts installation.
- Archive paths and member types are validated before files are extracted.
- Temporary release files are removed after success or failure.

## Troubleshooting

### `AI_SDLC_LICENSE_KEY is required in non-interactive mode`

Set the key in the process environment before running the installer.

### License errors

Errors such as `INVALID_LICENSE`, `EXPIRED_LICENSE`, `REVOKED_LICENSE`, or
`VERSION_NOT_ALLOWED` come from the licensing service. Confirm the key and the
version covered by your license.

### Artifact integrity verification failed

The installer fails closed and does not install the artifact. Retry on a
trusted network; if the error repeats, contact support with the requested
version and platform. Never bypass checksum verification.

### Python is not available as `python3`

Point the installer to your Python 3 executable:

```bash
AI_SDLC_PYTHON=/path/to/python3 npx ai-sdlc-backbone
```

## Documentation and support

- [Product documentation](https://mikegorelikoff.github.io/ai-sdlc-backbone/)
- [Public repository](https://github.com/mikegorelikoff/ai-sdlc-backbone)
- [Issue tracker](https://github.com/mikegorelikoff/ai-sdlc-backbone/issues)

The implementation and release artifacts are distributed as a licensed
product. This public installer is Apache-2.0 licensed; installing the product
does not change the product license that accompanies its release.
