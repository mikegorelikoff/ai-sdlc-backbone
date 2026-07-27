---
title: Roadmap
description: The direction of the AI SDLC Harness and the principles that govern future expansion.
---

The harness evolves around one goal: make AI-assisted delivery faster without making it less inspectable, portable, or safe.

## Now

- Validate `v3.0.0-rc.2` through protected CI and tagged installation, then
  decide whether to promote the reviewed capability set to stable `v3.0.0`.
- Preserve `v2.1.0` as the stable rollback target while the Harness API 3.0
  migration is evaluated.
- Measure adoption, compatibility failures, recovery outcomes, and documentation gaps without collecting source content.

## Next

- Connect host adapters to real execution surfaces while preserving capability negotiation, policy checks, and deterministic fallbacks.
- Add signed package attestations and configurable organization trust roots on top of existing digest and provenance validation.
- Add local longitudinal trend reports and regression thresholds without exporting repository content.

## Later

- Add reusable regulated and high-assurance policy profiles with maintained evidence mappings.
- Add more evidence-council execution adapters and reproducible research evidence ingestion.
- Evolve Harness API `3.x` additively and require an explicit migration before any future API major.

## Active program

The role-guided installable-flow program is tracked in the
[Feature 013 implementation specification](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/specs/013-role-guided-installable-flow/requirements.md).
The [release 3.0 candidate](reference/release-3.0.md) combines guided flow,
progressive skill steps, one canonical runtime, and OKF v0.2 artifact bundles.
Release 2.1 remains the stable baseline; earlier release audits remain
completed history.

## Roadmap rules

New capability must preserve artifact authority, explain its decisions, provide deterministic validation where possible, and remain optional when it serves a specialized domain. Proposals become roadmap work only when their user value, compatibility impact, evidence model, and maintenance owner are clear.
