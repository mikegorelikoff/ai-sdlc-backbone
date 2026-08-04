# Changelog

## v4.2.1 - 2026-08-04

### Fixed

- Extended the installed record validator to accept canonical
  `modules:<sorted-module-ids>` selections and verify that they include the
  complete default inventory plus only packaged opt-in skills.
- Added the packaged opt-in skill inventory to installed shared-runtime
  references and made the native optional-module test validate the resulting
  record and lock end to end.

### Validation

- Reproduced the `v4.2.0` post-install validation failure from its immutable
  published tag, then passed focused install-record and native installer tests
  with the corrective contract.
- Preserved the Harness API at `4.1.0`, TOON-only portable records, and the
  optional `context-cache` module contract at `4.2.0`.

## v4.2.0 - 2026-08-04

### Added

- Added the opt-in `context-cache` module and `ai-sdlc-context-cache` skill for
  deterministic local SQLite FTS5 and graph-enhanced RAG, incremental refresh,
  freshness verification, and context-pack/v4 assembly.
- Added `--module context-cache` to both project-scoped native installer
  profiles without changing the default 45-skill installation.
- Added TOON golden benchmark cases and receipts comparing lexical,
  graph-enhanced, packed, and direct-read behavior with path recall, anchor
  recall, savings, and stable fingerprints.
- Added deterministic read-through cache integration at the StepCard context
  boundary with one-writer coordination, aggregate observations, and safe
  direct-read recovery.
- Added a complete offline Tree-sitter AST graph for TypeScript, Python,
  JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift, including
  typed symbol, call, import, path, adjacency, and specification-trace edges.

### Security and context engineering

- Kept repository files authoritative, labeled retrieved content as untrusted
  evidence, excluded secret-like and unsafe sources before indexing, confined
  cache mutation and purge, and returned direct reads for missing, stale,
  corrupt, incompatible, or uneconomic cache state.
- Kept every portable machine input and output canonical TOON; SQLite is only
  disposable local binary state and no alternate machine format was added.
- Required every cache-backed pack to begin with its manifest-resolved owning
  step document, retain 100 percent of declared critical anchors, and achieve
  at least 15 percent net savings or fall back explicitly to direct reading.
- Isolated native parsers in time-bounded child processes with a minimal
  environment and denied network, pinned every runtime wheel by exact version
  and SHA-256, and made incomplete or failed AST parsing incapable of claiming
  graph completeness.

## v4.1.1 - 2026-08-03

### Fixed

- Updated the Pages checked-out candidate smoke to use the supported
  `codex-project` install profile after the removed legacy `--agent` flag
  caused the v4.1.0 documentation workflow to fail before build.
- Added a documentation regression that keeps workflow invocations aligned
  with the native installer CLI.

### Validation

- Re-ran the complete repository validation and both main workflows; release
  API and semantic skill contracts remain `4.1.0`.

## v4.1.0 - 2026-08-03

### Added

- Added the 45th skill, `ai-sdlc-scheduler`, with deterministic readiness,
  exclusive leases, optimistic revisions, expiry recovery, stale-worker
  rejection, and isolated StepCard runtime dispatch.
- Added allowlisted `workspace.write-text` and `external.toon-post` effect
  drivers with exact negotiation/context binding, approval enforcement,
  secret-key rejection, durable receipts, and replay-safe idempotency.
- Added strict provider execution observations and live receipts. The
  release-owned Codex/OpenAI TC-012 run records six passing scenarios,
  thresholds, context economics, recovery evidence, and an actual effect
  receipt; offline or unattested runs remain pending.
- Added deterministic `codex-project` and `claude-code-project` native install
  profiles targeting `.agents/skills` and `.claude/skills` respectively.

### Changed

- Raised the Harness API and every semantic graph manifest to `4.1.0`, with 45
  skills and 18 protected TOON contracts.
- Extended source and installed path resolution across both declared host
  profiles without adding global installation or source-checkout fallbacks.
- Kept per-step context compilation mandatory across scheduler dispatch and
  provider evaluation, including fingerprints, budgets, selection reasons,
  critical-anchor recall, and direct-read fallback.

### Validation

- Passed all 99 skill-owned test files with receipt fingerprint
  `ed5f433cd6d89af236a23f0e557d216845bd0b60b71849009527fb59602676d4`.
- Passed both fresh 45-skill native installed workflows through complete SDD
  gates and commit readiness, plus compatibility, semantic graph, and
  provider-executed TC-012 validation.

## v4.0.1 - 2026-07-30

### Fixed

- Replaced the external consumer installer with a Harness-owned deterministic
  installer after the post-publication `v4.0.0` smoke exposed a non-TOON
  generated lock.
- Added clean-revision binding, staged content hashing, symlink and non-TOON
  rejection, reviewed replacement authority, caught-failure rollback, and an
  installed tree-integrity validator.
- Replaced unsupported structured-list examples with the installed native
  record validator and narrowed the validated install target to
  project-scoped Codex.

### Added

- Added `ai-sdlc-install-record/v2` and
  `ai-sdlc-install-lock/v1`, including deterministic per-skill SHA-256
  fingerprints without timestamps or absolute machine paths.
- Added native installer regression tests and installed-layout smoke coverage.

### Validation

- Passed all 95 skill-owned test files with receipt fingerprint
  `4d7881a8cdb44d4f8cbbb7e995d8384f8d07968a4bdf0d892bbfb30ef0e47d9f`.
- Passed the native 44-skill installed workflow, exact API `4.0.0`
  compatibility, documentation source/tests, strict site build, rendered-link
  validation, and repository-wide TOON-only gates.

## v4.0.0 - 2026-07-30

### Added

- Added executable `ai-sdlc-skill-steps/v2` semantic DAGs, generated concise
  routers, StepCards, and at least five context/operation/validation/handoff
  nodes for all 44 skills.
- Added deterministic per-step `ai-sdlc-context-pack/v4` compilation with
  mandatory anchors, exact authority-labeled ranges, selected/skipped reasons,
  critical recall, savings thresholds, and direct-read fallback.
- Added all-skill offline evaluations for happy, blocked, invalid, resume, and
  context scenarios plus a provider-neutral live evaluation protocol.
- Added a complete skill test-file runner with a canonical receipt so
  hyphenated package paths cannot silently produce a zero-test pass.

### Changed

- Hard-cut every structured machine contract, fixture, CLI, state record,
  journal event, and generated artifact to one canonical TOON codec.
- Compiled workflows from installed skill entrypoints into immutable runtime
  plans and negotiated complete StepCards with host adapters.
- Strengthened runtime replay around strict planned, started, terminal,
  evidence, result ordering and one hash-chained TOON file per event.
- Bound each terminal result, evidence set, and effect receipt to one completion
  fingerprint so interrupted completion resumes only missing journal events
  and conflicting replays fail closed.

### Fixed

- Acquired the per-run mutation lock before replay, rejected journal sequence
  replacement, prevented retry from bypassing exhausted budgets, and validated
  event payloads without coercion.
- Bounded explicitly requested evaluation receipts to the owning repository.
- Aligned the protected release-history sequence with the three pre-v4
  installer and documentation commits so the exact post-commit audit passes.

### Removed

- Removed alternate serializers, parsers, CLI output modes, compatibility
  readers, source artifacts, and in-runtime legacy conversion paths.

### Known issue

- The initial external consumer installer creates a non-TOON lock. Preserve
  the immutable `v4.0.0` tag and update fresh or existing installations to
  `v4.0.1`.

### Documentation

- Documented the executable skill graph, deterministic context-engineering
  contract, StepCard handoff, per-event journal, all-skill harness, and
  repository-wide TOON-only gates.
- Redesigned the README around a short verified start and expected result.
- Reorganized GitHub Pages into the shared six-section product-family
  architecture.
- Added outcome-first Home and onboarding paths with lifecycle and role skill
  discovery.
- Aligned navigation, components, and accessibility tokens with Context Guard
  and AI SDLC Metrics.
- Kept deep skills, learning material, release detail, and audits available
  through progressive-disclosure catalogs.
- Added durable documentation governance and contract validation.
- Made the one-line project installer a distinct primary action before its
  read-only verification step.

## v3.0.0-rc.2 - 2026-07-27

### Fixed

- Checked out complete tagged history in skills CI so the release-roadmap audit
  can validate the sequence from `v2.1.0`.
- Updated the immutable remote installation smoke target from the pre-v3
  package to the published `v3.0.0-rc.1` commit.

### Validation

- Re-ran all 133 shared-runtime tests after the history correction.
- Verified a fresh remote Skills CLI installation from the exact
  `v3.0.0-rc.1` commit before preparing this corrected candidate.

## v3.0.0-rc.1 - 2026-07-27

### Added

- Added one guided `ai-sdlc-flow` Explore→Apply entry point with deterministic
  role/action selection, explicit handoffs, fingerprints, and bounded context.
- Added five neutral role contracts and just-in-time selectors for complete
  skill-owned prepare, execute, validation, and handoff steps.
- Added a shared OKF v0.2 renderer, bounded parser, provenance rules, artifact
  profiles, bundle indexes, conformance validation, and atomic migration.

### Changed

- Consolidated every installable helper under `ai-sdlc-shared-runtime` and
  removed the repository-only `_shared` runtime.
- Reduced all 44 `SKILL.md` entry points to concise routers backed by validated
  progressive-disclosure step manifests.
- Replaced workspace human specs indexes with feature-local `index.md` files
  and moved runtime project context under `_ai_sdlc/context/`.
- Changed the Harness API to `3.0.0`; bundled modules now declare
  `>=3.0.0,<4.0.0`.

### Removed

- Removed `ai-sdlc-navigator`; use `ai-sdlc-flow` Explore or invoke a known
  owning skill directly.
- Removed flow v1 acceptance, root `project-context.md`, workspace
  `specs-index.md`, and runtime fallbacks to legacy artifact paths.

### Validation

- Passed the Feature 013 11-command full-flow receipt, including 133 shared
  runtime tests, full/selective/global installation smoke, OKF bundle checks,
  compatibility, SDD, generated documentation, and diff hygiene.
- Revalidated the merged release candidate against Harness API 3.0.0,
  documentation, module, installation, and release-history gates.

## v2.1.0 - 2026-07-21

### Added

- Added an Apache License 2.0 `LICENSE` file so GitHub Community Standards and
  downstream adoption have explicit redistribution terms.
- Added GitHub community health files: Code of Conduct, issue forms, issue
  configuration, and pull request template.

### Changed

- Simplified the README into a beginner-friendly quick start and made agent
  host guidance tool-agnostic, with Codex shown only as an example.
- Updated release and installation documentation to describe `v2.1.0` and the
  Apache-2.0 licensing status.

### Fixed

- Pinned the remote installation smoke test in Pages CI to the exact `v2.1.0`
  commit SHA. The installer smoke helper requires a 40-character commit and
  no longer accepts the annotated release tag directly.

## v2.0.0-rc.1 - 2026-07-21

### Added

- Added a modern context, prompt, and personalization guide covering minimum
  sufficient context, prompt boundaries, evaluation, and safe interaction
  preferences.
- Added an opt-in typed interaction profile for preferred name, language,
  response style, technical depth, and status-update cadence.
- Added complete beginner foundations, role guides, practical tutorials,
  adoption governance, operations guidance, and evidence-backed audit reports.
- Added safe external-specification snapshots and field-tested post-specification
  workflow guidance.

### Changed

- Upgraded shared context snapshots and task packs to v3 with goal-relevant
  range selection, repository-instruction authority labels, explicit context
  sufficiency, and targeted next reads.
- Changed the harness API to `2.0.0`; bundled modules now declare the matching
  `>=2.0.0,<3.0.0` range.
- Made project-scoped installation the default and documented an explicit
  Codex-only global installation that avoids unsupported Eve and PromptScript
  targets.
- Made navigator discovery combine source, project, and packaged/global skill
  roots without recommending absent optional skills.

### Fixed

- Corrected installed consumer-root resolution across SDD and commit workflows.
- Hardened validation receipts, state transitions, repository-bounded writes,
  credential redaction, prompt-injection boundaries, recovery manifests, and
  compatibility inspection of untrusted target roots.
- Corrected documentation, generated catalogs, version links, installation
  ownership, and release-regression coverage identified by the production audit.

### Security and release status

- This is a release candidate because the repository owner has not yet selected
  a license and protected remote CI evidence is not available at tag-creation
  time. The tag does not grant permissions absent a license.
- Codex project/global installation and a complete installed workflow were
  validated locally; other agent hosts remain unverified unless listed in the
  supported-environments matrix.

## v1.2.0 - 2026-07-19

- Added guided onboarding, complete skill/script reference, adoption governance,
  and tagged install/runtime validation.

## v1.1.0 - 2026-07-19

### Added

- Added isolated change sets with semantic deltas, non-mutating preview,
  policy-gated atomic apply, recovery evidence, and archive.
- Added a repository delivery graph, evidence ledger, freshness propagation,
  policy-as-code, waivers, and bounded Context Engine v2 task packs.
- Added resumable task execution, append-only journals, deterministic TOON
  state, declarative workflows, approval gates, hooks, dependency waves, and
  one-task-one-commit enforcement.
- Added portable host capability negotiation, installation doctor and upgrade
  planning, package integrity and provenance checks, and content-free local
  metrics.
- Added versioned release navigation, a `1.1` migration guide, and an exact
  T001–T015 task-to-commit audit.

### Changed

- Made complete deterministic TOON the default agent-facing representation for
  the new control plane. TOON is limited to schema, external interoperability,
  recovery, and per-event TOON journal boundaries.
- Expanded the compatibility gate to protect all 43 skills, public flags,
  routes, module contracts, handoff fields, and the release commit sequence.
- Migrated the public documentation to Material for MkDocs and expanded its
  task-oriented navigation.

### Compatibility

- Release `1.1.0` remains on harness API `1.0.0` and is additive over `v1.0.0`.

## v1.0.0 - 2026-07-19

### Added

- Expanded `concepts/` with detailed system architecture, the canonical
  18-stage refinement lifecycle, context/quality semantics, and safe
  migration/concurrency behavior.
- Added authority hierarchies, invariants, status matrices, worked traceability
  examples, consistency checks, and recovery playbooks across concept docs.
- Added safe `--check`/`--apply` migration for legacy TOON and Markdown paths,
  with hard failure for divergent canonical and legacy content.
- Added tiered artifact quality signals and full-cascade gating.
- Added per-skill context snapshots and a skill-neutral feature source manifest.
- Added bounded `ai-sdlc-context/v2` TOON packs with exact source evidence,
  trace anchors, structural gaps, and targeted `next_reads` ranges.
- Added optional fingerprinted feature-local context caching and an
  informational raw/pack/targeted-reread benchmark CLI.
- Added SDD-specific compact context and TOON workflow status output.
- Added a short human-readable stdout summary after successful artifact
  finalization.
- Added stdin-driven `--section` and `--finalize` artifact assembly across the
  20 shared profile skills.
- Added deterministic decision-log row insertion with `--decision-row`.
- Added `sdd_artifact_scaffold.py` for content-only generation of the five SDD
  source Markdown artifacts.

### Changed

- Centralized the 18-stage refinement order, predecessors, artifact names,
  sections, tables, and token budgets in one canonical profile registry.
- Moved delivery handoff after QA traceability and made index writes atomic and
  state-aware.
- Routed every maintained TOON file through `_ai_sdlc`; derived context files
  are reproducible and ignored by Git.
- Profile analysis keeps Markdown as the human-readable default and exposes
  bounded TOON through `--format toon` for token-efficient agent context.
- Scaffold scripts now own Markdown initialization, section placement, metadata,
  atomic writes, and index refresh; the AI supplies only section bodies.
- Centralized SDD artifact section definitions for scaffold and validator reuse.

## v0.3.0 - 2026-07-10

### Added

- Added `concepts/` documentation for the core system model:
  - artifact routing;
  - artifact metadata and metatags;
  - decision logs;
  - flow modes;
  - feature state machine;
  - scripts;
  - specs index;
  - traceability.
- Added PM and Dev role guides to match the existing BA and QA guide model.
- Added role/workflow diagrams showing skill relationships, handoffs, and feedback loops.
- Added the original repository-only shared script infrastructure for:
  - artifact metadata generation;
  - specs index generation;
  - state machine enforcement;
  - script contract tests.
- Added deterministic helper scripts and tests across skills so agents can offload repetitive artifact scaffolding, validation, and token-heavy checks.
- Added `decision-log.md` requirements and a shared decision-log structure across skills.
- Added `--quick-flow` and `--full-flow` behavior across skill descriptions and helper scripts.
- Added TOON-based feature state machine guidance so LLMs can enforce lifecycle sequencing before moving to the next skill.
- Added specs index outputs for both AI and humans:
  - `specs-index.toon`
  - `specs-index.md`
- Added artifact metadata and metatag requirements for generated Markdown artifacts.
- Added SDD `plan.toon` as the machine-readable implementation execution plan.
- Added SDD `plan.md` as the human-readable execution plan generated from plan links and TOON task status.
- Added `skills/ai-sdlc-sdd/scripts/plan_links.py` to emit, write, and validate `plan.toon` plus `plan.md`.
- Added `skills/ai-sdlc-sdd/scripts/check_refinement_context.py` to enforce upstream refinement context in SDD full flow.
- Added SDD tests for:
  - `plan.toon` presence;
  - `plan.md` link coverage;
  - TOON task status syncing into Markdown task checkboxes;
  - full-flow refinement blockers;
  - completed upstream refinement context.

### Changed

- Reworked the top-level `README.md` to keep setup, repository purpose, skill workflow, and starting points concise.
- Updated `guides/workflow.md` to describe the full PM -> BA -> QA -> Delivery -> Dev lifecycle and how AI produces/consumes artifacts.
- Updated `guides/dev.md` to include `plan.toon` and `plan.md` in Dev-owned SDD context and diagrams.
- Updated `concepts/artifact-routing.md` to document `plan.toon` and `plan.md` as implementation SDD artifacts.
- Updated every skill to describe:
  - consistent flow flags;
  - decision-log usage;
  - artifact metadata;
  - state machine participation;
  - specs index refresh behavior;
  - helper script usage where available.
- Updated references across skills with more detailed templates, structures, checklists, and examples.
- Updated SDD validation so the implementation package now requires:
  - `requirements.md`
  - `design.md`
  - `test-cases.md`
  - `qa.md`
  - `tasks.md`
  - `plan.toon`
  - `plan.md`
- Updated SDD full flow so it consumes upstream refinement artifacts from `specs-refiniment/<feature-name>/`, including delivery spec and QA readiness evidence.
- Updated SDD analysis to require `plan.md` links for acceptance criteria, test cases, tasks, and core SDD artifacts.
- Updated SDD status evaluation to include `plan.toon`, `plan.md`, and full-flow upstream refinement gates.
- Updated code review readiness to require `plan.toon` and `plan.md` for medium/large SDD-backed work.
- Updated commit readiness to run SDD gates and `plan_links.py --check` when a spec is provided.
- Moved script tests out of `scripts/` folders into per-skill `tests/` folders for consistency.
- Standardized test coverage expectations so every skill script has colocated tests.

### Removed

- Removed old test-file placement from `scripts/` directories in favor of dedicated `tests/` directories.
- Removed old SDD assumptions that treated the implementation package as a five-file spec.

### Validation

- Verified Python syntax for the updated SDD, code-review, and commit-prep scripts.
- Ran SDD validator tests.
- Ran SDD workflow tests.
- Ran the shared repository-wide skill script contract test suite.

## v0.2.0 - 2026-07-09

### Added

- Added a tool-agnostic `README.md` that explains the AI SDLC skill library purpose, artifact routing, guides, installation, and usage across AI tools.
- Added operating guides under `guides/`:
  - `guides/workflow.md`
  - `guides/ba.md`
  - `guides/qa.md`
- Added missing local references for planning and PRFAQ workflows:
  - `skills/ai-sdlc-backlog-requirements-gap-review/references/planning-gap-review-framework.md`
  - `skills/ai-sdlc-prfaq-package-synthesis/references/prfaq-package-structures.md`

### Changed

- Standardized skill documentation around `ai-sdlc-<slug>` naming.
- Expanded every skill card with audience metadata for PM, BA, QA, Dev, and Delivery usage.
- Documented artifact routing rules:
  - PM, BA, QA, Delivery, discovery, refinement, and readiness outputs go to `specs-refiniment/<feature-name>/<file.md>`.
  - Developer SDD implementation packages go to `specs/<feature-name>/<file.md>`.
- Updated developer-facing skills to treat `specs-refiniment/` as upstream context and `specs/` as implementation-only output.
- Updated validation and commit helper scripts/tests after removing Asana traceability requirements.

### Removed

- Removed the duplicate Asana traceability skill.
- Removed Asana traceability requirements from SDD validation, commit validation, test fixtures, and skill documentation.
