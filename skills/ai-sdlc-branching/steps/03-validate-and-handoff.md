# Validate and Handoff — ai-sdlc-branching: Branching

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Use this branch handoff report when branch state matters:

```text
Branching:
- Task: user-visible task name
- Change size: small | medium | large
- Spec: specs/NNN-short-feature-name | none
- Base branch: resolved branch | blocked with reason
- Base refresh: pulled latest resolved base | reused existing task branch | blocked
- Current branch: branch-name
- Expected branch: branch-name
- Action: already correct | created | reused with reason | blocked
- Dirty tree: clean | related files listed | unrelated/unclear blocker
- Next phase: implementation | validation | commit-prep
```

Quality gate:

- Pass when implementation starts on a branch that matches the task type and,
  for medium or large work, includes the active spec slug.
- Fail when repo-tracked files are mutated on a shared/default branch, unrelated
  dirty files are carried silently, branch/spec mismatch is hidden, or Git
  command failures are ignored.

## Examples

Valid medium-work start:

```text
Branching:
- Task: AI SDLC Git-flow branching skill and workflow update
- Change size: medium
- Spec: specs/191-branching-workflow
- Base branch: main (origin/HEAD)
- Base refresh: pulled latest resolved base
- Current branch: main
- Expected branch: feature/191-branching-workflow
- Action: created
- Dirty tree: clean
- Next phase: implementation
```

Valid small fix:

```text
Branching:
- Task: fix typo in validation warning
- Change size: small
- Spec: none
- Base branch: main (repository default)
- Base refresh: pulled latest resolved base
- Current branch: main
- Expected branch: fix/validation-warning-typo
- Action: created
- Dirty tree: clean
- Next phase: implementation
```

Invalid counter-example:

```text
Edited files directly on the shared base and will make a branch later.
```

Reject this because branch verification must happen before repo-tracked file
mutation for implementation work.

## Edge Cases

- If the repository has no declared/present base branch, stop and ask the owner
  to declare one; do not invent `dev`.
- If already on a correctly named task branch, continue and report `already
  correct`.
- If already on a non-default branch that clearly belongs to the same task,
  report `reused with reason`; do not create a second branch.
- For new task branches, do not skip checkout/pull of the resolved base merely
  because it looks recent.
- If `git pull --ff-only` reports divergence, stop and ask for repository
  maintenance instead of merge-committing during task setup.
- If the branch name matches multiple specs or no spec for medium or large work,
  resolve the active spec with `$ai-sdlc-sdd` before implementation.
- If unrelated dirty files exist, do not run destructive cleanup. Ask the user
  whether to keep, commit, stash, or otherwise handle them.
- If branch creation fails from sandboxing, request escalation rather than
  inventing an alternate branch state.
- Do not push branches unless the user explicitly asks or the commit workflow
  requires it.

## Scope Boundary

- Do not create or update SDD artifacts; use `$ai-sdlc-sdd`.
- Do not decide validation commands; use `$ai-sdlc-validation`.
- Do not stage files or create commits; use `$ai-sdlc-commit-prep`.
- Do not draft commit messages; use `$ai-sdlc-conventional-commit`.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
