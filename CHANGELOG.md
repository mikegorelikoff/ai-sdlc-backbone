# Changelog

## Unreleased

### Changed

- Renamed the licensed product to **AI SDLC Backbone** and the public installer
  package to `ai-sdlc-backbone`; the canonical install action is now
  `npx ai-sdlc-backbone`.
- Renamed the public and private-core repository identities to
  `ai-sdlc-backbone` and `ai-sdlc-backbone-core` while preserving public paths
  and established `ai-sdlc-*` runtime compatibility identifiers.
- Restricted the current public tree to documentation, examples, onboarding,
  project metadata, and the public licensed installer.
- Moved executable implementation and release tooling to the private core,
  which consumes this repository at a pinned submodule commit.
- Added the public licensing API contract and documented short-lived download
  grants, checksum verification, and the no-private-GitHub-access user model.

### Security

- Added public leakage and installer corruption tests.
- Documented that historical public Apache-2.0 grants are unaffected and that
  history will not be rewritten without a separate owner and legal decision.

## v4.4.0 - 2026-08-05

- Added portable project installation and update behavior across supported
  Codex, Claude Code, and Agent Skills-compatible profiles.
- Improved installation safety, deterministic records, and platform support.

Earlier implementation-level release notes remain available in historical Git
tags. Future entries here describe public user-visible behavior only.
