# Start here

This is the canonical first-run path for AI SDLC Harness.

## Prerequisites

- Node.js 20 or newer with `npx`.
- Python 3.10 or newer for the packaged installation operation.
- A valid AI SDLC Harness license key.
- Network access to the configured licensing service.

Keep the key in `AI_SDLC_LICENSE_KEY` or use the masked interactive prompt. Do
not place the key in a CLI argument, source file, issue, or log.

## Install

From the project that should receive the Harness, run:

```bash
npx @ai-sdlc/install
```

The default profile is `codex-project`. Select another supported profile with
`--profile`; see the [install guide](../guides/install.md).

## Verify

Use the verification command printed by the successful installer. Confirm the
installed version matches the version authorized by the licensing response.

## First request

Ask the installed agent host to explore a bounded change before applying it:

```text
Use ai-sdlc-flow to Explore this request. Show the route, evidence, rigor,
roles, blockers, planned writes, and next checkpoint. Do not Apply until I
approve the card.

Request: add a health endpoint to this service.
```

Next, learn the [delivery mental model](../how-it-works/index.md).
