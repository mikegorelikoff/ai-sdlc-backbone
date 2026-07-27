# Execute — ai-sdlc-sdd: Specification-Driven Development

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/analyze_spec.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.
- Use `scripts/check_checklist.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.
- Use `scripts/check_clarify.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.
- Use `scripts/resolve_active_spec.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.
- Use `scripts/sdd_status.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.
- Use `scripts/sdd_context.py` before broad SDD reads; inspect its exact AC/TC/task/decision anchors and follow only the reported `next_reads` ranges.
- Use `scripts/spec_helpers.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.
- Use `scripts/validate_spec.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.
- Use `scripts/plan_links.py` to emit, write, or validate the required `_ai_sdlc/plan.toon` machine plan plus `plan.md` execution plan and cross-artifact trace map.
- Use `scripts/sdd_artifact_scaffold.py` to write `requirements.md`, `design.md`, `test-cases.md`, `qa.md`, and `tasks.md` one stdin section at a time.
- Use `scripts/check_refinement_context.py` in `--full-flow` before SDD handoff to ensure upstream refinement delivery and QA readiness are complete.
- Treat commands under `qa.md` as `PLANNED` until executed. Bare `PASS` claims
  require a current `_ai_sdlc/validation-receipt.json` produced by
  `ai-sdlc-validation/scripts/run_validation.py`; a non-zero command or changed
  revision/diff makes readiness fail.

## Script Usage

- Use SDD scripts as ordered gates for implementation work; pass the same flow flag supplied to the skill.
- Resolve active spec when the target is unclear: `python3 skills/ai-sdlc-sdd/scripts/resolve_active_spec.py --quick-flow --files <changed-file>...` or `python3 skills/ai-sdlc-sdd/scripts/resolve_active_spec.py --full-flow <spec-or-folder>`.
- Check workflow state for people with `python3 skills/ai-sdlc-sdd/scripts/sdd_status.py --spec specs/<feature-name> --quick-flow`; agents add `--format toon`, and full-flow remains required before handoff.
- Build bounded implementation context: `python3 skills/ai-sdlc-sdd/scripts/sdd_context.py specs/<feature-name> --quick-flow`; use `--cache-context` only when cross-session reuse is useful.
- Write one artifact section: `python3 skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py specs/<feature-name> --artifact <requirements|design|test-cases|qa|tasks> --section "<section>" --quick-flow`; provide only the section body on stdin.
- Repeat section writes and then replace `--section ...` with `--finalize`; the AI must not create a temporary content file or directly edit the generated Markdown artifact.
- Add a decision with `--decision-row` and one nine-cell Markdown table row on stdin; `--artifact` is not required for this action.
- Validate structure: `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/<feature-name> --quick-flow`.
- Create or refresh the execution plan pair: `python3 skills/ai-sdlc-sdd/scripts/plan_links.py specs/<feature-name> --write --quick-flow|--full-flow`.
- Emit compact machine plan only: `python3 skills/ai-sdlc-sdd/scripts/plan_links.py specs/<feature-name> --emit-toon --quick-flow|--full-flow`.
- Validate the execution plan links: `python3 skills/ai-sdlc-sdd/scripts/plan_links.py specs/<feature-name> --check --quick-flow|--full-flow`.
- Full-flow upstream gate: `python3 skills/ai-sdlc-sdd/scripts/check_refinement_context.py specs/<feature-name> --full-flow`.
- Full-flow pre-implementation gates, in order: `check_refinement_context.py`, `check_clarify.py`, `check_checklist.py`, `plan_links.py --check`, `analyze_spec.py`, then `validate_spec.py`, each with `specs/<feature-name> --full-flow`.
- Use quick flow for fast structural confidence; use full flow before expanding implementation tasks, handoff, review, or commit prep.

## Purpose

Create, update, validate, and enforce the AI SDLC SDD package for medium and large changes before implementation expands.

## Inputs

- Read `AGENTS.md` for change classification and repository workflow rules when
  it exists. If it is absent, record that fact and use the default risk rubric
  below; absence is not permission to invent repository policy.
- Collect the user request, affected systems, and likely spec name.
- Search existing `specs/` folders for a matching active or historical spec.
- Use `$ai-sdlc-ba`, `$ai-sdlc-test-cases`, and `$ai-sdlc-qa` when those phases are incomplete.
- In `--full-flow`, read `specs-refiniment/_ai_sdlc/specs-index.toon`, upstream `state.toon`, `delivery-spec.md`, `qa-readiness.md`, and `decision-log.md` before finalizing implementation SDD.
- Read existing code only after the spec intent and affected surface are clear enough to avoid scope drift.

## Steps

1. Classify the change using `AGENTS.md` when present. Otherwise use this
   default rubric and record the provisional classification:
   - **small:** documentation/wording or a localized behavior-preserving fix
     with no public contract, data, authorization, dependency, or deployment
     impact;
   - **medium:** one bounded feature or refactor with testable behavior and
     reversible implementation inside one subsystem;
   - **large:** public API/schema, architecture, security/authorization,
     provider, migration, irreversible data, multi-system, or broad operational
     impact.
   When signals differ, choose the larger class.
2. Use the small-change path only for typo fixes, tiny bug fixes, test-only fixes, log text changes, or other no-contract changes.
3. For medium or large work, find a matching `specs/NNN-short-name/` folder or create the next numbered folder.
4. Treat the full folder name as the canonical delivery ID; do not rely on the numeric prefix alone.
5. Add or update `specs/spec-registry.md` for tracked governance or delivery-critical work.
6. Ensure these files exist before implementation:
   - `requirements.md`
   - `design.md`
   - `test-cases.md`
   - `qa.md`
   - `tasks.md`
   - `_ai_sdlc/plan.toon`
   - `plan.md`
7. Write requirements before design; write design before implementation tasks.
8. Run the clarify gate after requirements are current:

   ```bash
   python3 skills/ai-sdlc-sdd/scripts/check_clarify.py specs/NNN-feature-name
   ```

9. Record implementation traceability, source artifact links, or documented no-ticket exceptions in `requirements.md`.
10. Derive test cases before writing tests.
11. Derive QA acceptance and regression scope before final validation.
12. Write task entries with explicit `Output:` and `Refs:` metadata for new or updated active specs.
13. Generate `_ai_sdlc/plan.toon` from `tasks.md` as the required compact machine projection linking SDD artifacts, AC IDs, TC IDs, task IDs, dependencies, decisions, task status, and validation order.
14. Generate `plan.md` as the human-readable execution projection from the same links. Task checkboxes in `tasks.md` are authoritative; regenerate both plans with `plan_links.py --write` after a status change.
15. Run the checklist gate before implementation tasks expand:

   ```bash
   python3 skills/ai-sdlc-sdd/scripts/check_checklist.py specs/NNN-feature-name
   ```

16. Implement only tasks described in `tasks.md` and sequenced in `_ai_sdlc/plan.toon` / `plan.md`.
17. Mark a task checkbox complete in `tasks.md` only after code, docs, and
    required validation satisfy it; then regenerate `_ai_sdlc/plan.toon` and
    `plan.md`. Never hand-edit generated task status.
18. Run the analyze gate before implementation handoff or commit prep:

   ```bash
   python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py specs/NNN-feature-name
   ```

19. Validate the active spec:

   ```bash
   python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/NNN-feature-name
   ```

20. Use workflow-state status when the next phase is unclear:

   ```bash
   python3 skills/ai-sdlc-sdd/scripts/sdd_status.py --spec specs/NNN-feature-name
   ```

21. Report compliance, completed tasks, validation, and open risks.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
