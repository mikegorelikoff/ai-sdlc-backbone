---
title: Documentation decision log
description: Record the AI SDLC Harness documentation architecture, URL, governance, and validation decisions.
---

# Documentation decision log

Execution date: 2026-07-27

## Optional local context cache

On 2026-08-03, the documentation added an opt-in local context-cache path for
repeated repository retrieval. The cache is explicitly an optimization rather
than authority: canonical repository sources, accepted decisions, and human
approvals remain controlling. The portable boundary stays TOON-only, while the
SQLite FTS5 database is disposable project-local state excluded from Git.

The public install path remains the 45-skill baseline. Users deliberately add
the 46th cache skill with `--module context-cache`; that project-scoped install
is the opt-in for bounded automatic StepCard warming and reuse. A separate
rollback-journal control database serializes warmers, while source verification,
strict TOON policy, manifest-budget clamping, v4 validation, and direct-read
fallback keep the cache from becoming authority or an availability dependency.
Standalone build, query, verify, benchmark, observe, reset, and purge commands
remain available for reproducible operation and support.

Only low-cardinality aggregate operation outcomes and token economics persist
in the control database. Query text, prompts, retrieved content, credentials,
identity, and wall-clock values are excluded. The accepted index remains in
rollback-journal mode; unconditional WAL is deferred because the researched
host runtime falls within an upstream WAL-reset corruption advisory range.

Primary research and full-flow refinement define the first release as
graph-enhanced RAG rather than full GraphRAG: it combines deterministic FTS5
seeds with bounded repository relations, while LLM-extracted entities,
community summaries, embeddings, and global search remain deferred. A packed
result must include the owning step document, retain every critical anchor,
and save at least 15 percent; deterministic TOON golden benchmarks guard these
claims and direct reading remains the safe successful fallback.

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

## Native TOON-only installation correction

On 2026-07-30, the first fresh installation from the published `v4.0.0` tag
proved that the third-party installer generated a non-TOON lock and silently
ignored the documentation's requested structured-list flag. That contradicted
the release's repository-wide machine-boundary contract.

The published tag remains immutable. Corrective release `v4.0.1` replaces the
external installer with a source-owned Python installer, pins the primary
one-line command to the release tag, narrows the validated target to
project-scoped Codex, and writes a deterministic content-addressed TOON lock.
The installed validator recomputes all managed digests. Global and other-host
installation remain explicit future conformance work.

## Local context cache and AST graph release

On 2026-08-04, release `v4.2.0` adds the optional local context-cache module,
read-through StepCard integration, and a deterministic Tree-sitter AST graph
for twelve languages. The Harness API remains `4.1.0` because the capability is
additive and opt-in. Portable machine contracts remain TOON-only; SQLite is
derived local state, parser wheels are exact-version and SHA-256 locked, and
any incomplete, stale, unsafe, or uneconomic graph result falls back to
authoritative direct reads.

The immutable `v4.2.0` post-publication smoke then exposed that the installed
record validator rejected the installer's canonical
`modules:context-cache` selection. Corrective release `v4.2.1` adds a packaged
opt-in inventory and validates module selections against the complete default
inventory plus declared opt-in skills. It does not change the cache, AST graph,
Harness API, module version, or TOON-only boundary.

The first protected CI run for `v4.2.1` then proved that graph-required tests
were executed before a Tree-sitter runtime existed on clean Ubuntu runners.
Corrective release `v4.2.2` adds CPython 3.10 and 3.13 Linux x86_64 parser locks
in TOON, verifies exact wheel filenames and SHA-256 values, installs only the
verified bytes with network-disabled pip, and runs the twelve-grammar offline
preflight before repository tests. The Harness API and context-cache module
version remain unchanged.

## Local context graph explorer

On 2026-08-04, the optional context-cache module gained a reusable `visualize`
command for human exploration of its complete accepted graph. The command
creates one deterministic self-contained HTML file inside the project cache,
with repository search, layer controls, full direct incoming and outgoing
relations, node-to-node navigation, and an optional highlighted source view.

The viewer is a disposable read-only projection, not a new authority or
portable machine contract. It never warms or repairs the cache, may display
stale state only with explicit drift labels, makes no network request, and
excludes source bodies unless `--include-source` is supplied. Existing public
paths, canonical documentation ownership, Harness API, module version, and
TOON-only portable contracts remain unchanged.

Node inspection uses a centered accessible modal rather than a persistent
drawer so the complete graph remains the primary workspace. The modal preserves
selection while closed, supports relation navigation in place, manages keyboard
focus, and dismisses through Close, `Escape`, or a backdrop click. Layer
filters, connection visibility, fit, and zoom remain in a persistent top
control bar so graph settings are available without opening the inspector. The
viewer uses a compact Linear-inspired neutral shell: controls are rectangular,
tabs use a simple active underline, and status or relation metadata is presented
without decorative badges or pills. The inspector uses one selected-node header
and three task-specific panes: Details contains row-based properties and direct
context, Relations lists compact navigable edges, and Source owns code and
freshness. Global graph statistics stay outside node inspection.
