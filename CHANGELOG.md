# Changelog

## v5.1.0 - 2026-09-08

### Added

- Requirements discovery with bounded source preparation, typed validation and
  freshness checks.
- Repository-grounded engineering review and deterministic execution contracts
  across all 48 product skills.

### Changed

- Reject invalid step histories and handoffs that bypass verification; bind
  mandatory context to source fingerprints and bound recovery behavior.
- Keep licensed product implementation in the private core. The public
  installer remains 1.0.1; existing runtime paths and schema identities remain
  compatible. Loop 0.3.0 remains a separately installed product.

### Validation and limitations

- Structural and mutation evaluations validate mechanical contracts; they do
  not establish live model reasoning quality. Release archives remain
  allowlisted and checksummed. Version 5.0.1 remains the rollback target.

## v5.0.1 - 2026-08-21

### Changed

- Expanded the npm package metadata and installer README with requirements,
  profiles, CLI options, environment variables, security behavior, and
  troubleshooting guidance.
- Renamed the licensed product to **AI SDLC Backbone** and the public installer
  package to `ai-sdlc-backbone`; the canonical install action is now
  `npx ai-sdlc-backbone`.
- Renamed the public and private-core repository identities to
  `ai-sdlc-backbone` and `ai-sdlc-backbone-core` while preserving public paths
  and established `ai-sdlc-*` runtime compatibility identifiers.

### Fixed

- Fixed the npm symlink entrypoint so `npx ai-sdlc-backbone` executes the CLI
  instead of exiting without output.
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
