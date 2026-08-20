# Documentation decision log

## 2026-08-20 — npm package documentation is a supported entry point

The `ai-sdlc-backbone` package README now provides the complete installer
contract: prerequisites, supported profiles, CLI options, environment
variables, verification, security behavior, and troubleshooting. Canonical
product concepts remain in the public documentation site; the npm README links
there instead of duplicating the broader architecture.

## 2026-08-20 — AI SDLC Backbone product identity

The licensed product is now **AI SDLC Backbone**. Its public package and
machine product identifier are `ai-sdlc-backbone`; the primary installation
action is `npx ai-sdlc-backbone`. Existing `ai-sdlc-*` skill names,
`AI_SDLC_*` environment variables, `.ai-sdlc/` project paths, and `ASDL-*`
license keys remain stable compatibility contracts.

Historical AI SDLC Harness entries, tags, and release assets are retained as
historical evidence. Public documentation paths and the required top-level
navigation remain unchanged.

## 2026-08-19 — Licensed distribution boundary

The public repository now owns only documentation, examples, onboarding,
public metadata, and the public installer. Executable product implementation,
skills, runtime logic, internal templates, tests that expose internals, and
release tooling move to the private core repository.

The private core pins this public repository as a Git submodule. The public
repository never points to or embeds the private core. Public paths for Home,
Start here, How it works, Guides, Reference, and Project remain stable.

Historical public releases contained implementation under Apache-2.0. Removing
it from the current tree does not revoke prior grants or make history private.
Any history rewrite, replacement repository, or future-version licensing
policy requires a separate owner and legal decision; this migration does not
rewrite history automatically.
