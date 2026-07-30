---
title: Documentation decision log
description: Record the AI SDLC Harness documentation architecture, URL, governance, and validation decisions.
---

# Documentation decision log

Execution date: 2026-07-27

## Previous model

The site exposed six product-specific tabs and placed the complete learning
curriculum, skill inventory, role catalog, release records, and production
audit in the primary navigation. The Home page led with release detail and a
long pinned installation sequence.

## Selected architecture

The site now uses Home, Start here, How it works, Guides, Reference, and
Project. README and Home lead with the user outcome and one project-scoped
path. Deep skill pages and audit evidence remain built and searchable through
catalogs.

## Alternatives considered

- Keep the existing navigation and change labels only: rejected because the
  initial sidebar would still expose dozens of equal choices.
- Move or delete deep pages: rejected to preserve public URLs and evidence.
- Create a shared runtime style package: rejected because each site must build
  independently without a new external dependency.

## Product-specific decisions

- `ai-sdlc-flow` Explore is the recommended default.
- Quick flow, full flow, and direct expert invocation remain supported and are
  visually differentiated.
- The short project-scoped installer stays on README and Home. Pinned,
  rollback, host-specific, telemetry, and trust details remain in the install
  guide.
- Repository tests are described as mechanism evidence, not proof of ROI,
  quality, cost, or delivery improvement.

## Reference influences

Spec Kit informed the visible artifact flow; OpenSpec informed example-first
progressive disclosure; BMAD Method informed task, explanation, reference, and
role-aware routes. No text, commands, branding, or assets were copied.

## URL compatibility

No existing public page moved or was deleted. Individual skill pages, release
detail, role detail, learning lessons, and audits remain directly addressable.

## Validation evidence

See the root workspace `.docs-unification/validation-report.md` for exact
commands and results.

## One-line installation

On 2026-07-28, README, Home, Start here, and the installation guide made the
existing project-scoped `install.sh` pipeline one clearly isolated primary
command. Verification remains separate so readers can distinguish the
state-changing install from its read-only inventory check. The command follows
`main`; immutable and review-first installation remains in the detailed guide
for higher-trust environments.

## Executable skills and canonical TOON

On 2026-07-30, all 44 skills moved from coarse three-document progression to
validated `ai-sdlc-skill-steps/v2` semantic DAGs. The manifest and linked step
documents are canonical; concise `SKILL.md` selector tables and public
catalogs are generated projections. A valid graph has at least five semantic
nodes and explicit operations, context contracts, gates, outputs, side-effect
classes, idempotency, retry, and recovery boundaries.

Context is compiled per dependency-ready step into
`ai-sdlc-context-pack/v4`. Packed context requires every critical anchor and a
minimum token saving; otherwise the StepCard requires exact direct reads.
Selected and skipped sources, instruction authority, recall, savings, and
fingerprints are reviewable.

Canonical TOON is now the only structured machine-data representation across
contracts, fixtures, configuration, manifests, context, plans, per-event
journals, state, compatibility baselines, and evaluation receipts. Runtime
contains no alternate parser, silent coercion, or in-place legacy conversion
mode. Repository and strict documentation-build gates enforce absence,
decodability, and canonical byte stability. Markdown remains the human
authority and review surface where prose is required.

The public `docs/explanation/toon-first.md` path is preserved for URL
compatibility, but its title and content now describe the TOON-only contract.

The built-in Material search plugin is disabled because it emits an alternate
machine artifact. Public paths remain unchanged; the generated lifecycle,
role, script, module, and skill catalogs remain the supported discovery
surface. Rendered validation fails if a build introduces an alternate machine
artifact extension.
