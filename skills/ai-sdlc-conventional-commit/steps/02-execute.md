# Execute — ai-sdlc-conventional-commit: Conventional Commit Message

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/validate_commit_msg.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.

## Script Usage

- Validate commit messages before presenting or using them.
- Quick flow: `python3 skills/ai-sdlc-conventional-commit/scripts/validate_commit_msg.py --quick-flow --message "<type(scope): subject>"`
- Full flow: `python3 skills/ai-sdlc-conventional-commit/scripts/validate_commit_msg.py --full-flow path/to/commit-message.txt`
- Use `--require-traceability` when medium or large work must include `Spec:`,
  `Task: TNNN`, and `Validation:` metadata even outside full flow.

## Purpose

Draft, validate, or repair an AI SDLC commit message that uses Conventional Commit syntax and includes SDD, business, implementation, testing, and validation traceability when the change is medium or large.

## Inputs

- Collect the intended change type: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `build`, `perf`, or `revert`.
- Collect the optional scope when it adds useful precision, for example `api`, `bitgo`, `sdd`, `skills`, or `docs`.
- Collect the active spec folder for medium or large work, for example `specs/177-skill-instruction-upgrade`.
- Collect the completed task ID or IDs represented by the commit.
- Collect the implementation summary, reviewer-visible test path, and exact validation commands with outcomes.
- Collect breaking-change details when behavior, schema, API contract, migration requirements, or compatibility changes are not backward compatible.

## Steps

1. Write the subject as `type(scope): imperative summary` or `type: imperative summary`.
2. Keep the subject under 72 characters unless a longer subject prevents ambiguity.
3. Use a lowercase type and lowercase kebab-case scope.
4. Use an imperative summary, for example `fix bitgo wallet routing`, not `fixed bitgo wallet routing`.
5. Add `Spec: specs/NNN-feature-name` for medium or large work.
6. Add `Task: TNNN` (or a comma-separated list of canonical task IDs) for
   medium or large work. Each ID must represent completed work in the named
   specification; do not invent a task to satisfy the validator.
7. Add `Business context`, `Implementation details`, `Mermaid diagram`, `How to test`, and `Validation` sections for medium or large work.
8. Add `BREAKING CHANGE:` when the change requires a migration, client update, data backfill, or operator action.
9. Validate the message before committing:

   ```bash
   python3 skills/ai-sdlc-conventional-commit/scripts/validate_commit_msg.py path/to/message.txt --require-traceability
   ```

10. Fix every validator error before using the message.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
