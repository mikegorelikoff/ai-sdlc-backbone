# Guided Flow Contract

## DecisionCard

Schema: `ai-sdlc-flow/v1`.

Semantic fingerprint inputs are repository identity, normalized intent,
classification and confidence, feature, workspace, stage, skill, rigor, activated roles and
their evidence, project-context status, selected source hashes, context
economics, blockers, and planned writes. Presentation order, timestamps, and
diagnostic wording are excluded.

The SHA-256 fingerprint detects route drift. It is not authentication,
authorization, approval, or a sandbox bypass.

## Explore

Explore may read bounded repository evidence but must not create or update
files, state, indexes, branches, caches, or logs. A blocked Explore still emits
a complete card and has no planned writes.

Explicit sources extend rather than replace mandatory configuration, state,
index, module, and project-context evidence.

For an existing explicit feature, an active skill or the earliest incomplete
prerequisite for the requested stage controls resume order. Unrelated optional
stages do not hijack the route. When no feature state exists, implementation
on `dev`, `main`, or `master` routes to branching first.
Explore discovers owning skills from source, project-scoped, and packaged
sibling roots and blocks when the selected skill is unavailable.

## Apply

Apply accepts a complete JSON DecisionCard, rebuilds the card from current
repository evidence, and requires an exact fingerprint match. Verification-only
mode reports the single allow-listed state transition. `--execute` starts that
one transition through the canonical state-machine helper.

Apply rejects arbitrary commands, output-root overrides, unsupported skills,
multiple transitions, and every drift condition before mutation.

## Workspaces

- Refinement: `specs-refiniment/<NNN-feature>`.
- Implementation: `specs/<NNN-feature>`.

Feature roots must remain within their physical canonical root and must not be
symlinks. The flow does not collapse roots or create links between them.

## Context Economics

`net_tokens = packed_tokens + targeted_reread_tokens`.

Packed context is selected only when critical-anchor recall equals 100% and
`(raw_tokens - net_tokens) / raw_tokens * 100 >= 15`. All other cases select
direct reading.
