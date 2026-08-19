# Install the Harness

## Goal

Install an authorized AI SDLC Harness release into a local project.

## When to use it

Use this guide for a first installation or to reinstall the same authorized
version safely.

## Prerequisites

- Node.js 20+, Python 3.10+, and a valid license key.
- The target project directory.
- The licensing API URL when using a non-production environment.

## Procedure

Provide `AI_SDLC_LICENSE_KEY` through a protected environment mechanism, or
use the masked prompt. From the target project, run:

```bash
npx @ai-sdlc/install
```

Optional public flags are `--profile`, `--project-root`, `--skills-root`, and
`--version`. Do not put the license key in an argument.

## Verify

Run the profile-specific verification command printed by the installer and
confirm the installed version.

## Troubleshooting

- `INVALID_LICENSE`, `EXPIRED_LICENSE`, or `REVOKED_LICENSE`: contact the
  license administrator; the installer cannot override the backend.
- `artifact integrity verification failed`: do not retry from cached bytes;
  request a new grant and investigate release storage.
- `UNSUPPORTED_PLATFORM`: use a supported platform or contact support.
- Controlled install failure: correct the reported local permissions or target
  conflict, then rerun. Temporary download data is removed automatically.

## Next step

Return to [Start here](../start-here/index.md) for the first Explore request.
