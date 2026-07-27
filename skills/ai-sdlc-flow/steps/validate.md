# Validate — Guided Explore and Apply

> Selector: validate

## Entry

Recompute route, source, configuration, role, flow-step, and owning-skill-step evidence before mutation or completion.

## Procedure

## Context Rule

Use packed context only when it retains 100% of configured critical anchors and
saves at least 15% after targeted rereads. Otherwise use direct reading and
show raw, packed, reread, net, savings, and recall values.

## Review Rule

For review routes, capture findings against requirements, acceptance criteria,
tests, and diff before exposing AI rationale or prior verdicts. Preserve the
independent finding set for later comparison.

## Safety and Boundaries

- Never accept caller-selected output roots, arbitrary commands, or multiple
  actions.
- Reject ambiguous intent, malformed feature slugs, symlink roots, root escape,
  divergent roots, stale evidence, and fingerprint drift before mutation.
- Do not repair global installation, create compatibility symlinks, publish a
  release, or collect live telemetry.
- Direct skills retain their own prerequisites and authority checks.

## Existing Phase Guidance

# Validate

Inspect requirements, tests, and the changed behavior independently. Run focused deterministic checks, record gaps, then compare implementation rationale.

## Exit

Reject drift or unsafe context; otherwise expose validation and remaining risk.
