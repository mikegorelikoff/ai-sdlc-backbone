# Execute — ai-sdlc-branching: Branching

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/branch_plan.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- No external reference files are required for this skill.

## Script Usage

- Run `scripts/branch_plan.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-branching/scripts/branch_plan.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-branching/scripts/branch_plan.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Create or verify the correct Git-flow task branch before repo-tracked file
mutation, keep branch names aligned with active specs, and hand completed work
to validation and commit prep without mixing unrelated changes.

## Inputs

- Collect the user-visible task name and change classification.
- Collect the active spec folder for medium or large work.
- Collect the current branch and dirty tree from:

  ```bash
  git status --short --branch
  ```

- Collect the repository's declared base branch before creating any new task branch.
- Collect whether the intended change is feature, fix, docs-only, or
  repo-local maintenance/governance.
- Collect sandbox or approval constraints from `$ai-sdlc-approvals-sandbox` if
  Git branch commands fail because Git refs cannot be written.

## Steps

1. Run `git status --short --branch` before mutating repo-tracked files.
2. Allow read-only planning, repository inspection, and SDD drafting before a
   task branch exists when those actions do not mutate repo-tracked files.
3. Classify dirty files as related, unrelated, or unclear.
4. Stop before branch creation or branch switching when unrelated or unclear
   dirty files would be carried into the task without explicit user approval.
5. Choose the branch name:
   - Medium or large SDD work: `feature/NNN-short-feature-name`.
   - Small bug fix: `fix/<short-name>`.
   - Docs-only work: `docs/<short-name>`.
   - Repo-local governance or maintenance: `chore/<short-name>`.
6. For medium or large work, preserve the full active spec slug after the
   prefix, for example `feature/191-branching-workflow`.
7. Resolve the base branch in this order: explicit repository policy
   (`ai-sdlc.baseBranch`), `origin/HEAD`, then an existing local `dev`, `main`,
   or `master`. Use `dev` only when it is declared or actually present.
8. If already on a correctly named task branch for the current task, continue
   and report `already correct`; do not recreate the branch.
9. Before creating a new task branch, switch to the resolved base and pull the
   latest remote state with fast-forward-only semantics:

   ```bash
   git checkout <base-branch>
   git pull --ff-only origin <base-branch>
   ```

10. If the resolved base cannot be checked out or pulled cleanly, stop and report the
    blocker instead of branching from stale or divergent local state.
11. Create the new branch from the refreshed resolved base with a non-interactive
    command, for example:

   ```bash
   git checkout -b feature/191-branching-workflow
   ```

12. If checkout, pull, or branch creation fails because sandboxing blocks Git
    refs or network access, use `$ai-sdlc-approvals-sandbox` and request narrow
    approval for the specific Git command.
13. Perform implementation only after the branch is verified or created from
    refreshed `dev`.
14. When the user-visible task is complete, run `$ai-sdlc-validation`, then
    `$ai-sdlc-commit-prep`.
15. Use one branch and one commit per user-visible task by default. Do not treat
    individual `tasks.md` checkboxes as automatic branch or commit boundaries.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
