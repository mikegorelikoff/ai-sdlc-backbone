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
