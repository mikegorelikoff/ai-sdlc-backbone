---
title: Roadmap
description: The direction of the AI SDLC Harness and the principles that govern future expansion.
---

The harness evolves around one goal: make AI-assisted delivery faster without
making it less inspectable, portable, or safe.

## Now

- Verify `v4.0.0` through protected CI and a fresh tagged installation, then
  link that post-publication evidence from the release.
- Record provider-executed live protocol receipts for the reference host and
  expand the certification matrix only where an accountable owner exists.
- Measure adoption, compatibility failures, recovery outcomes, and
  documentation gaps without collecting source content.

## Next

- Connect host adapters to real execution surfaces while preserving capability
  negotiation, policy checks, and deterministic fallbacks.
- Add signed package attestations and configurable organization trust roots on
  top of existing digest and provenance validation.
- Add local longitudinal trend reports and regression thresholds without
  exporting repository content.

## Later

- Add reusable regulated and high-assurance policy profiles with maintained
  evidence mappings.
- Add more evidence-council execution adapters and reproducible research
  evidence ingestion.
- Evolve Harness API `4.x` additively and require an explicit migration before
  any future API major.

## Active program

The executable skill harness program is tracked in the
[Feature 015 implementation specification](https://github.com/mikegorelikov/ai-sdlc-harness/blob/main/specs/015-executable-skill-harness-v4/requirements.md).
[Release 4.0](reference/release-4.0.md) combines semantic skill DAGs,
deterministic per-step context engineering, StepCards, durable replay, and one
canonical TOON machine boundary. Earlier release audits remain completed
history.

## Roadmap rules

New capability must preserve artifact authority, explain its decisions,
provide deterministic validation where possible, and remain optional when it
serves a specialized domain. Proposals become roadmap work only when their user
value, compatibility impact, evidence model, and maintenance owner are clear.
