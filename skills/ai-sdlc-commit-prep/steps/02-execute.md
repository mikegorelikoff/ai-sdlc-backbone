# Execute — ai-sdlc-commit-prep: Commit Preparation

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/check_commit_ready.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.

## Script Usage

- Run commit readiness before staging final commit content or writing the final commit summary.
- Quick flow: `python3 skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py --quick-flow --spec specs/<feature-name> --allow-unstaged --no-require-staged`
- Full flow: `python3 skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py --full-flow --spec specs/<feature-name>`
- For an explicitly task-scoped commit in a larger active SDD plan, add
  `--task TNNN`. The selected task must be present and complete; later pending
  tasks remain allowed. Without `--task`, every spec task must be complete.
- Every medium or large traced SDD commit message must include the completed
  task identity as `Task: TNNN` (or a comma-separated list). `--task` narrows
  the readiness check; it does not replace the commit-message trailer.
- Use `--allow-unstaged` only when intentionally checking readiness before final staging.
- Use `--no-require-staged` only for preflight checks; omit it immediately before commit creation.

## Purpose

Prepare and create a safe AI SDLC commit by reviewing the branch and working tree, staging only related files, validating SDD evidence, using a valid Conventional Commit message, and reporting post-commit traceability.

## Inputs

- Collect the user’s explicit commit request or workflow state showing commit prep is justified.
- Collect the active spec folder for medium or large work.
- Collect validation commands and outcomes that are current for the active diff.
- Collect the current branch and dirty tree from `git status --short --branch`.

## Steps

1. Run `git status --short --branch`.
2. Run `git diff --stat` and `git diff --cached --stat` when staged changes already exist.
3. Inspect relevant diffs for scope, accidental edits, generated files, secrets, and unrelated user changes.
4. Confirm medium or large work has current `requirements.md`, `design.md`, `test-cases.md`, `qa.md`, `tasks.md`, `_ai_sdlc/plan.toon`, and `plan.md`.
5. For medium or large work, confirm the current branch includes the active spec slug after a typed Git-flow prefix, for example `feature/NNN-short-feature-name`; otherwise report the branch/spec mismatch before committing.
6. Confirm completed tasks in `tasks.md` match the diff.
7. Run or confirm current validation before staging.
8. Ensure the active spec passes structural validation plus clarify,
   checklist, and analyze before final commit.
9. Run the readiness checker before final commit:

   ```bash
   python3 skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py --spec specs/NNN-feature-name --no-require-staged
   ```

   When the user explicitly requested one commit per SDD task, add
   `--task TNNN` and verify that the staged diff belongs only to that task.

10. Stage only files belonging to the current change.
11. Leave unrelated dirty files unstaged and report them.
12. Use `$ai-sdlc-conventional-commit` to draft and validate the message.
    Include `Spec:`, `Task:`, and exact `Validation:` evidence for medium or
    large SDD work.
13. Commit with a non-interactive command, for example `git commit -F /tmp/message.txt`.
14. Run `git status --short --branch` after committing.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
