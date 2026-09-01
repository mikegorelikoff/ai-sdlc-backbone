---
title: Engineering Quality Gate
description: Human-facing operating guide for ai-sdlc-engineering-quality-gate, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-engineering-quality-gate`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Mandatory post-implementation engineering quality gate | Dev | QA, Architecture, Security | `core` | Canonical TOON context and quality report plus a concise evidence-based presentation |

## Why it exists

Inspect a bounded implementation against repository evidence, remediate safe material defects, rerun relevant checks, and decide whether the current diff is ready for the next stage.

## Use it when

AI SDLC post-implementation engineering quality gate. Use after an AI or human implementation when the assistant must inspect the current diff in repository context, compare representative local implementations, review correctness and repository fit adversarially, run deterministic verification, safely fix evidence-backed High and localized Medium findings, rerun checks, and issue a current evidence-based readiness report. Supports `--quick-flow` for bounded focused review and `--full-flow` for stricter trace and verification coverage.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use it before a bounded implementation diff and accepted change contract exist. Use `ai-sdlc-sdd` or the owning implementation workflow instead.
- Do not use it only to execute an already defined check list. Use `ai-sdlc-validation` instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- A concise requested change or an accepted specification.
- A Git repository and current implementation diff, or an explicit base
  revision that resolves inside it. `context` defaults the base to `HEAD`.
- Repository instructions and any requirements, design, tasks, tests, or
  acceptance evidence that define the expected behavior.
- The write boundary for fixes and the host authority needed to edit files and
  execute repository commands.

Block when the request or review target is missing. Do not manufacture a diff,
acceptance criterion, permission, comparison, or verification result. If the
working tree includes unrelated changes, inventory them and preserve their
bytes, index state, and ownership.

## Tell your agent

```text
Use ai-sdlc-engineering-quality-gate for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report Canonical TOON context and quality report plus a concise evidence-based presentation, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Read the requested change or accepted specification, current Git status and
  diff, bounded context profile, selected repository examples, applicable
  repository instructions, direct tests/contracts, and authorized command
  sources.
- Read pre-existing validation only when it is bound to the exact current diff;
  otherwise mark it stale and run the required check.

### References

- Read `references/quality-gate-contract.md` before reviewing or fixing code.
- Read `references/context-schema.toon` before persisting context.
- Read `references/report-schema.toon` before creating a draft or final report.
- Read `references/usage-examples.md` only when invocation or report assembly
  needs an example. `references/example-quality-report.toon` is illustrative,
  not evidence for the active repository.

### Deterministic helper

Resolve the logical skill root before using the helper. Use argv, never a shell
command string:

```bash
python3 skills/ai-sdlc-engineering-quality-gate/scripts/engineering_quality_gate.py context --root . --request "<requested change>" --base <revision> --output <context.toon> --quick-flow
python3 skills/ai-sdlc-engineering-quality-gate/scripts/engineering_quality_gate.py finalize --root . --context <post-fix-context.toon> --draft <draft.toon> --output <quality-report.toon>
python3 skills/ai-sdlc-engineering-quality-gate/scripts/engineering_quality_gate.py verify --root . --report <quality-report.toon>
```

`context` also accepts `--feature <slug>` for a Loop-compatible fingerprint and
`--max-candidates <n>` for an explicit bound from 2 through 5. Full flow replaces
`--quick-flow` with `--full-flow`. `finalize` validates, canonicalizes, sorts,
fingerprints, and writes atomically. `verify` is read-only and rejects drift.

## What it may write

- Resolve `skills/` as a logical skill root and verify that this skill and
  `ai-sdlc-shared-runtime` exist in the chosen source or installed layout.
- Use repository-relative, contained `.toon` paths for durable context, draft,
  and report artifacts. Use an owning feature `_ai_sdlc` directory when one is
  already canonical; otherwise make the output path explicit.
- Reject absolute output paths, parent traversal, symlink escape, and
  non-TOON durable machine output. Never persist secrets, raw unbounded command
  output, timestamps, durations, or absolute temporary paths in signed data.
- Durable schemas are `ai-sdlc-engineering-quality-gate-context/v1`,
  `ai-sdlc-engineering-quality-gate-draft/v1`, and
  `ai-sdlc-engineering-quality-gate/v1`.

## Human checkpoints

- Ask only when the request, review target, acceptance boundary, fix authority,
  or required verification cannot be recovered from repository evidence.
- Keep confirmed facts, assumptions, and blockers distinct. Product ambiguity
  becomes a remaining finding; it is not permission to guess.
- A missing optional comparison is not a blocker when the bounded search and
  shortfall reason are explicit.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support mutually exclusive `--quick-flow` and `--full-flow` modes; reject an
  invocation that supplies both.
- Quick flow uses the smallest relevant diff, the highest-ranked local
  comparisons, focused checks, and visible reversible assumptions. Ask only
  when continuing could cause material correctness, security, data-loss,
  compatibility, or authority risk.
- Full flow verifies every available trace artifact, inspects all applicable
  review dimensions, and runs the justified repository gates required for
  delivery confidence. Stop on material ambiguity rather than guessing.
- Both modes require findings before mutation, the same severity/fix policy,
  current post-fix evidence, and the same readiness invariants.

## Procedural step selectors

The router loads these skill-owned procedures just in time. Read only the selector matching the current phase, active role, and action; a selected step is normative and an unselected step stays out of context.

| Selector | Type | Phases | Roles | Dependencies | Operation | Side effect | Load rule | Step | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `preflight` | `analysis` | `prepare` | `qa-engineer`, `software-architect`, `software-engineer` | none | `inspect-and-route` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-engineering-quality-gate/steps/01-prepare.md) | establish the request, diff boundary, authority, and safe TOON routes |
| `context` | `context` | `clarify`, `route` | `qa-engineer`, `software-architect`, `software-engineer` | `preflight` | `compile-context` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-engineering-quality-gate/steps/02-context.md) | compile the smallest repository-grounded engineering review context |
| `execute` | `action` | `execute` | `qa-engineer`, `software-architect`, `software-engineer` | `context` | `execute-procedure` | `workspace-write` | `on-demand` | [`steps/02-execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-engineering-quality-gate/steps/02-execute.md) | review adversarially, fix safe material findings, and rerun checks |
| `validate` | `validation` | `validate` | `qa-engineer`, `software-architect`, `software-engineer` | `execute` | `validate-evidence` | `none` | `before-completion` | [`steps/03-validate-and-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-engineering-quality-gate/steps/03-validate-and-handoff.md) | enforce report truthfulness, current evidence, and readiness policy |
| `handoff` | `handoff` | `handoff`, `complete` | `qa-engineer`, `software-architect`, `software-engineer` | `validate` | `handoff-result` | `none` | `before-completion` | [`steps/04-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-engineering-quality-gate/steps/04-handoff.md) | return a current report with an unambiguous owner and next action |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` or `.claude/skills/<skill>/...` path reported by your profile. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`engineering_quality_gate.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-engineering-quality-gate/scripts/engineering_quality_gate.py) | Build and validate deterministic repository-grounded quality-gate evidence. | `python3 skills/ai-sdlc-engineering-quality-gate/scripts/engineering_quality_gate.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage



## Success criteria

Validate and return one canonical `ai-sdlc-engineering-quality-gate/v1` TOON
report plus a concise YAML presentation and `ai-sdlc-handoff/v2`. The report is
the durable authority; presentation and handoff must agree with its readiness.

### Evidence gate

Validate all of the following before completion:

- The context and report parse as TOON, use supported schemas, contain only
  repository-relative paths, and bind to the current change fingerprint.
- The repository profile cites 2–5 representative examples where practical,
  or records an evidence-based shortfall, and every applicable pattern has
  repository evidence.
- Findings were captured before mutation, IDs are unique, ordering is
  canonical, severities are not inflated, and fixed versus remaining state is
  truthful.
- High findings and safe localized Medium findings were fixed when authorized;
  every unfixed material item states why it could not be resolved safely.
- Verification commands use argv, focused checks precede broader checks,
  post-fix results exist after fixes, and each status reflects an actual
  `pass`, `fail`, `not_run`, or `unavailable` outcome.
- Change-scope counts match the post-fix diff, new dependencies and public API
  changes are explicit, and unrelated modifications made by the gate are zero.
- `finalize` succeeded atomically and `verify --root . --report <path>` succeeds
  against the unchanged repository state.

### Decision rules

- `PASS`: `ready_for_next_stage: true`, no remaining finding, no verification
  gap, and every required available deterministic check passes.
- `PASS_WITH_FINDINGS`: `ready_for_next_stage: true`, no unresolved High or
  blocking Medium finding, every required available check passes, and only
  explicit non-blocking Low/Medium findings or optional/unavailable checks
  remain.
- `FAIL`: readiness is false because a High or blocking Medium remains, an
  available required check failed or was not run, required evidence is absent,
  the report is invalid/stale, or status and decision disagree.

Treat an applicable repository command that cannot execute because of the
environment as `not_run`, with a reason; do not relabel it `unavailable`.
`unavailable` means the repository exposes no applicable command or source for
that optional verification kind. A required `unavailable` check is blocking.
If verification fails, final status cannot be `PASS`.

### Human presentation

Keep the durable report in canonical TOON. Present a concise YAML projection in
the active response using, where practical:

```yaml
status: PASS | PASS_WITH_FINDINGS | FAIL
summary: evidence-based assessment
repository_profile:
  representative_examples: []
  applicable_rules: []
findings_fixed: []
remaining_findings: []
verification: []
change_scope:
  files_changed: 0
  lines_added: 0
  lines_removed: 0
  new_dependencies: []
  unrelated_changes: []
quality_evidence:
  repository_consistency: []
  correctness: []
  testing: []
  simplicity: []
final_decision:
  ready_for_next_stage: false
  blocking_reasons: []
```

Scores are optional. Never include a score without concrete evidence for that
dimension.

## Blockers and recovery

- If no credible comparison exists, state the bounded search and continue only
  with other repository evidence; do not invent a local convention.
- If there are no findings, retain explicit empty finding arrays and actual
  verification evidence.
- If authority is review-only, leave safe material fixes documented and set
  readiness according to their blocking state.
- If a command cannot run, preserve its exact status and reason. Never claim a
  stale, skipped, blocked, unavailable, or inferred result passed.
- If finalization or current-report verification fails, leave no partial output
  and report `FAIL` with the recovery action.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Return context/report paths and fingerprints, finding counts, exact command
  statuses, readiness, blockers, and next action directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v2` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone prose
  summary. Durable machine evidence is canonical TOON; the concise YAML final
  projection is presentation only.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - The gate does not advance lifecycle state by itself. Read an existing
      feature `_ai_sdlc/state.toon` to confirm the implementation stage and owner.
    - Do not create a state file merely for standalone invocation. In AI SDLC Loop,
      `--feature` validates the current specification and Implement approval and
      writes only the requested quality artifacts; it does not imply approval.
    - Route lifecycle completion through the owning workflow after this report is
      current and ready.

??? info "Artifact metadata"

    - This skill creates TOON by default, so `artifact_metadata` Markdown
      frontmatter is not added to the canonical context or report.
    - If the user explicitly requests a durable Markdown companion, use the shared
      `artifact_metadata` contract and include `metatags` for `ai-sdlc`,
      `implementation`, `engineering-quality-gate`, and current status. The
      Markdown remains a projection; it cannot replace the TOON report.

??? info "Specs index"

    - Before broad feature reads, inspect `specs/_ai_sdlc/specs-index.toon` for
      implementation work and the feature-local `index.md` for human traceability.
    - Refresh an owning workspace index only when repository policy registers the
      quality report there. Never use `specs-index.toon` or `index.md` as a
      substitute for the selected requirement, source, test, or report evidence.

    ### Adjacent Capability Boundary

    - Use `$ai-sdlc-code-review` for a read-only findings review that must not fix
      code or make a delivery decision.
    - Use `$ai-sdlc-validation` when command selection and execution evidence are
      the only requested outcome.
    - Use `$ai-sdlc-security-testing` when exploitability, abuse cases, or security
      boundaries are the primary scope. This gate still records evidence-backed
      security and reliability findings relevant to the changed behavior.

## Example

- TypeScript explicit-zero correction: compare neighboring services, record
  the fallback defect before editing, fix it locally, and rerun focused tests
  plus typecheck.
- Go retry transaction regression: use a branch base, inspect transaction and
  provider examples, fix the supported idempotency boundary, and rerun focused
  then repository-required tests.
- Review-only path safety: retain the unresolved High finding and return
  `FAIL` when mutation authority is absent.

Read `references/usage-examples.md` for the three complete invocation examples
and `references/example-quality-report.toon` for a final report shape.

### Mandatory order

1. Read the request, acceptance evidence, current diff, status, and diff scope.
   Generate the bounded context profile and confirm it describes the intended
   implementation rather than unrelated work.
2. Inspect the smallest relevant repository area for supported engineering
   conventions. Select and read 2–5 representative implementations when
   practical; disclose an evidence-based shortfall instead of padding it.
3. Build the repository engineering profile from concrete paths and lines.
   Inspect relevant tests, interfaces, abstractions, validation, error handling,
   naming, architecture boundaries, data access, dependency injection, logging,
   utilities, mocking, and verification configuration.
4. Review as a skeptical Staff Engineer in this priority order: correctness,
   repository consistency, regression safety, simplicity, maintainability,
   testability, and relevant performance. Inspect correctness, repository fit,
   simplicity, maintainability, tests, security/reliability, and change scope.
   Apply the anti-AI and diff-budget checks in the contract.
5. **Before any implementation edit**, create the complete typed findings set.
   Give every finding a stable ID, non-inflated severity, category, contained
   file/location, observed evidence, impact, concrete recommended fix,
   blocking state, and resolution state. An empty set is valid only after all
   applicable dimensions were inspected.
6. Detect repository-owned build, typecheck, lint, test, and static-analysis
   commands from source. Human-review each argv, then run the smallest relevant
   authorized checks first. Record actual pre-fix outcomes as `pass`, `fail`,
   `not_run`, or `unavailable`; never infer success from configuration or old
   output.
7. Fix every High finding that can be resolved safely inside authority and
   every safe localized Medium finding. Reuse repository patterns and existing
   utilities. If a material fix needs product clarification, broader paths,
   architecture redesign, a new dependency, or unsafe refactoring, leave it
   explicit and blocking rather than guessing. Do not fix Low findings merely
   for cleanup.
8. Reinspect the diff after every fix batch. Remove only changes proven
   unrelated to the request and made by this gate. Regenerate the bounded
   context against the post-fix diff, rerun every relevant affected check, then
   run broader required checks only when repository contracts or risk justify
   them. Any later source change makes earlier evidence stale.
9. Create an `ai-sdlc-engineering-quality-gate-draft/v1` TOON payload from the
   current repository profile, fixed and remaining findings, executed
   verification, final change scope, and evidence-based decision. Finalize it
   against the post-fix context, then run `verify` on the written report.

### Guardrails

- Do not evaluate generated code in isolation or substitute model confidence
  for repository evidence.
- Do not redesign the application, invent architecture, add casual
  dependencies, perform style-only refactors, broaden public behavior, weaken
  lint/type rules, suppress failures, delete tests, or rewrite unrelated files.
- Flag or revise evidence-backed AI-code smells: obvious comments, one-use
  generic abstractions, invented layers, excessive helpers or wrappers,
  duplicated utilities, silent or catch-all fallback, excessive mocking, TODO
  placeholders, speculative compatibility/configurability, unrelated refactors,
  oversized changes, impossible-state checks, and over-general solutions.
- Treat every extra file, line, dependency, abstraction, and public API change
  as risk. Do not perform opportunistic cleanup.

## Source contract

This page is generated from [`skills/ai-sdlc-engineering-quality-gate/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-engineering-quality-gate/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
