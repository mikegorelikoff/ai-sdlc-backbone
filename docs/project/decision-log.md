# Documentation decision log

## 2026-08-21 — Product and installer releases use independent versions

AI SDLC Backbone `5.0.1` is the current licensed product release, while
`ai-sdlc-backbone` `1.0.1` remains the current public installer. Product
artifacts and the npm installer advance independently; every product manifest
declares its minimum compatible installer version. The public versions
reference is the canonical user-facing status surface.

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

## 2026-09-08 — Backbone 5.1.0 release

Publish customer-facing notes for discovery and deterministic skill execution.
Preserve the licensed distribution boundary: implementation is released from
the private core, and the public repository contains no skill or runtime source.
Product 5.1.0 and installer 1.0.1 use independent version lines.

## 2026-09-08 — Backbone 5.2.0 release

Publish per-skill chat output contracts with deterministic validation while
preserving native artifacts and existing authority boundaries. Core source and
licensed archives remain private. Loop 0.4.0 and Context Guard 0.1.3 are separate
product releases; the unchanged public installer stays at 1.0.1. Simulation
results do not establish live model reliability. Roll back to Backbone 5.1.0
when a consumer cannot adopt this additive presentation update.

## 2026-09-08 — Deterministic execution reinforcement

The next Backbone change strengthens existing runtime primitives and all 48 local skill boundaries. The public repository records customer-visible behavior; implementation, fixtures and internal source inventory remain in Backbone Core. This entry does not announce a published release or change the installation command.

## 2026-09-08 — Release 5.3.0

Publish the user-authorized determinism reinforcement from feature 026. Keep native artifact formats and existing approval boundaries. Structural and fixture-based tests do not establish live model reliability. Roll back by pinning 5.2.0; do not rewrite published tags.
