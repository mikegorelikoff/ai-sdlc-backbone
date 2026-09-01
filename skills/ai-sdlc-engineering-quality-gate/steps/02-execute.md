# Execute — ai-sdlc-engineering-quality-gate

> Selector: execute

## Entry

Enter only after preflight and context pass and this skill owns the bounded
post-implementation gate. Keep unrelated work unchanged.

## Procedure

## Inputs

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

## Examples

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

## Exit

Stop only after the final report is bound to the post-fix context and `verify`
has returned current evidence, or after a blocker is recorded without unsafe
mutation. Do not silently begin delivery, commit, or another skill.
