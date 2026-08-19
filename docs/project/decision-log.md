# Documentation decision log

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
