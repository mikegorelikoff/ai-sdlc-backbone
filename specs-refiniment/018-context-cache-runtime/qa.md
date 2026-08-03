---
type: "ai-sdlc.qa-plan"
title: "QA Plan"
description: "Acceptance, regression, risk, and manual validation plan."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T12:21:09Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "qa.md"
  path: "specs-refiniment/018-context-cache-runtime/qa.md"
  workspace: "refinement"
  skill: "ai-sdlc-qa"
  flow_mode: "full"
  state_file: "specs-refiniment/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/018-context-cache-runtime/decision-log.md"
  status: "approved"
  owner: "QA Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-008"
    - "BR-001"
    - "BR-006"
    - "DEC-001"
    - "DEC-007"
    - "WF-001"
    - "WF-002"
    - "WF-003"
    - "WF-004"
  related_artifacts:
    - "specs-refiniment/018-context-cache-runtime/backlog-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/backlog.md"
    - "specs-refiniment/018-context-cache-runtime/business-context.md"
    - "specs-refiniment/018-context-cache-runtime/decision-log.md"
    - "specs-refiniment/018-context-cache-runtime/delivery-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/delivery-spec.md"
    - "specs-refiniment/018-context-cache-runtime/discovery.md"
    - "specs-refiniment/018-context-cache-runtime/goal-capability-map.md"
    - "specs-refiniment/018-context-cache-runtime/index.md"
    - "specs-refiniment/018-context-cache-runtime/prfaq.md"
    - "specs-refiniment/018-context-cache-runtime/release-slicing.md"
    - "specs-refiniment/018-context-cache-runtime/requirements-readiness.md"
    - "specs-refiniment/018-context-cache-runtime/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-qa"
    - "qa"
    - "approved"
---

# qa.md

## Feature Summary
QA validates that the optional context cache becomes a safe StepCard optimization without changing authority or default-install behavior. The plan covers automatic activation, concurrent and fresh warming, strict policy, manifest limits, pack acceptance, private aggregate observations, stable fault recovery, deterministic receipts, documentation, and installation compatibility across AC-001 through AC-008.

## Actors and Stakeholders
Contributors and AI agents are affected consumers. Harness maintainers supply runtime and cache fixtures. Repository maintainers validate policy behavior. QA owns scenario coverage, regression selection, deterministic evidence, and signoff; Security separately approves confinement and observation privacy. Product and Architecture are consulted only if evidence contradicts accepted DEC-001 through DEC-007.

## Scope and Boundaries
QA scope includes local unit, integration, multi-process, fault-injection, policy, privacy, install-layout, docs, and deterministic economics checks. It includes automatic and direct-read paths plus inspect and reset operations. Remote services, embeddings, daemons, network telemetry, cross-project retrieval, full GraphRAG, production credentials, and nondeterministic latency thresholds remain outside this feature and its test data.

## Workflows and Failure Paths
Coverage follows WF-001 cached success, WF-002 absent or unhealthy fallback, WF-003 concurrent fresh publication, and WF-004 support inspection/reset. Required failures include contention, crash or corruption, mutation during build, invalid policy, budget excess, adapter timeout, FTS5 absence, missing anchors, stale hashes, low savings, unsafe paths, and unknown observation fields; every viable path must end with accepted evidence or direct reads.

## Requirements and Business Rules
Tests map FR-001 through FR-008 and BR-001 through BR-006 to AC-001 through AC-008. Highest invariants are repository authority, optional activation, manifest ceiling, owning-step and mandatory-anchor retention, aggregate-only observations, and non-blocking direct fallback. A scenario fails if it fabricates evidence, widens authority, exposes partial state, persists raw content, or changes default behavior.

## Data, Integrations, and Non-Functional Requirements
Fixtures use temporary project roots, deterministic Markdown sources, valid and malformed TOON policies, isolated SQLite projections, controlled subprocess timeouts, and installed versus absent optional-skill layouts. Assertions cover stable ordering and fingerprints, atomic replacement, one logical accepted state, offline operation, confinement, privacy, bounded execution, v4 schema, token economics, and repeatable output.

## Dependencies, Risks, and Constraints
Tests depend on Python, host SQLite with FTS5 for active-cache scenarios, shared runtime codecs, current manifests, and temporary writable directories. Runtime-specific FTS5 absence is a recoverable scenario. Risks are flaky concurrency, timing-sensitive mutation, accidental source-tree activation, false savings, and observation leakage. Barriers, deterministic fixtures, bounded joins, exact schema checks, and repeated runs control these risks.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-007 govern QA scope. Owner: QA Maintainers. Assumptions: supported test hosts can run Python multiprocessing and at least one fixture can exercise FTS5; an unavailable feature must demonstrate direct fallback. Impact: no missing product choice blocks planning. Next step: synthesize executable cases and suites. Latency remains observational and cannot decide deterministic pass or fingerprint equality.

## Success Measures
Signoff requires every AC mapped to at least one executable case; all P0 cases pass; mandatory anchors show complete recall; no stale, partial, or divergent accepted projection is observed; absent/unhealthy paths match direct reads; limits respect manifests; observation schemas contain no raw evidence; deterministic receipts repeat byte-for-byte; docs gates pass; and security review has no unresolved high finding.

## Source Coverage
Consumed sources: specs-refiniment/018-context-cache-runtime/discovery.md; specs-refiniment/018-context-cache-runtime/prfaq.md; specs-refiniment/018-context-cache-runtime/delivery-gap-review.md; specs-refiniment/018-context-cache-runtime/requirements-readiness.md; specs-refiniment/018-context-cache-runtime/goal-capability-map.md; specs-refiniment/018-context-cache-runtime/backlog-gap-review.md; specs-refiniment/018-context-cache-runtime/backlog.md; specs-refiniment/018-context-cache-runtime/user-stories.md; specs-refiniment/018-context-cache-runtime/release-slicing.md; specs-refiniment/018-context-cache-runtime/business-context.md; specs-refiniment/018-context-cache-runtime/delivery-spec.md; specs-refiniment/018-context-cache-runtime/decision-log.md; specs-refiniment/018-context-cache-runtime/index.md. Implementation validation evidence is tracked separately and cannot be inferred from this plan.

## Acceptance Scenarios
| QA ID | Actor | Setup | Action | Expected Result | Evidence | Risk |
| --- | --- | --- | --- | --- | --- | --- |
| QA-001 | agent | optional module absent | compile StepCard | authoritative direct paths match baseline | integration test | High: compatibility |
| QA-002 | runtime | multiple processes and stale cache | warm concurrently | one fresh logical fingerprint; no partial reads | multi-process test | High: corruption |
| QA-003 | repository maintainer | defaults, exact overrides, invalid fields | resolve policy | exact valid values apply within manifest; invalid input recovers safely | unit test | High: governance |
| QA-004 | agent | valid and invalid pack candidates | compile context | only fresh owner-complete anchor-complete economical v4 is accepted | integration test | High: authority |
| QA-005 | maintainer | hit, miss, fallback, reset operations | inspect observations | only bounded aggregate counts and token totals appear; reset clears them | schema test | High: privacy |
| QA-006 | agent | each fault fixture | compile context | stable reason-coded direct reads return | fault matrix | High: availability |
| QA-007 | QA | repeated identical fixture | compare receipts and latency | receipts match; latency is reported separately | repeatability test | Medium: trust |
| QA-008 | Security | unsafe path and offline guard | exercise runtime | writes stay confined and no network or deferred retriever runs | security test | High: boundary |

## Regression Targets
Protect direct StepCard selection when the module is absent, mandatory repository-instruction loading, owning-step precedence, context-pack/v4 deterministic ordering and fingerprints, existing feature-017 build/query/pack/verify/purge behavior, source exclusion and symlink confinement, TOON-only command output, generated catalogs, docs navigation, project install smoke, and shared runtime state/index behavior. Each target is at risk from auto-detection or adapter integration.

## Risk-Based Coverage
| Priority | Risk | Coverage | Release Rule |
| --- | --- | --- | --- |
| P0 | stale, partial, or divergent accepted evidence | concurrent warm, mutation, corruption, interrupted build, source recheck | any failure blocks |
| P0 | authority or budget widening | owner, mandatory anchors, exact override, manifest clamp, unsafe source | any failure blocks |
| P0 | privacy or confinement breach | observation allowlist, secret-like fixture, symlink/path tests, offline guard | any failure blocks |
| P0 | default behavior regression | absent-module parity and source-checkout non-activation | any failure blocks |
| P1 | token regression or support ambiguity | savings gate, stable reasons, observe/reset, docs | release requires documented resolution |
| observational | latency variation | repeated bounded timings outside fingerprints | report only; investigate timeouts |

## Test Data and Environment
Use temporary repositories containing known skill steps, repository instructions, ordinary docs, excluded paths, symlinks, mutable sources, malformed policy, low-savings text, and secret-like sentinel values that must never persist. Run installed-module and absent-module layouts, clean/stale/corrupt caches, concurrent processes, forced timeouts, and optional FTS5-unavailable simulation. No production repositories, credentials, identities, remote endpoints, or uncontrolled clocks enter golden fixtures.

## Validation Commands
Planned and already exercised focused commands:
- `python3 -m unittest skills/ai-sdlc-context-cache/tests/test_context_cache.py -v` validates cache lifecycle, concurrency, privacy, recovery, packing, confinement, and TOON output.
- `python3 -m unittest skills/ai-sdlc-shared-runtime/tests/test_steps.py -v` validates StepCard integration, strict policy, limits, and compatibility.
- `python3 docs/scripts/validate_docs.py` and `python3 -m unittest discover -s docs/tests -v` validate documentation contracts.
- `python3 skills/skill-creator/scripts/quick_validate.py skills/ai-sdlc-context-cache` validates skill structure when the helper is available.
- `git diff --check` validates patch whitespace.
Final signoff records exact pass counts and any skipped broader suite with reason.

## Manual Checks
Maintainer review must inspect resolved policy precedence, one cached and one fallback StepCard receipt, aggregate observe/reset output, reason-code clarity, and the public guide’s install/automatic/fallback/troubleshooting flow. Security manually reviews stored control columns and derived path confinement. Manual review does not replace automated correctness evidence and remains planned until final implementation receipts are assembled.

## Signoff Criteria
QA status is Ready for test synthesis, not yet release-approved. Final release signoff requires all P0 automated scenarios, focused regressions, security boundary review, docs validation, installed and absent smoke, deterministic receipt comparison, and observation privacy review to pass with current evidence. Any stale acceptance, partial publication, authority widening, raw observation data, unbounded timeout, or default-install drift blocks release.
