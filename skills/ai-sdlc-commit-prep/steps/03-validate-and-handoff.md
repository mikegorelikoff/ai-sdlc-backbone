# Validate and Handoff — ai-sdlc-commit-prep: Commit Preparation

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Return this final report:

```text
Commit:
- Hash: full_hash
- Subject: conventional subject
- Branch: branch-name
- Spec: specs/NNN-feature-name | none
- Task: TNNN[, TNNN] | none

Staging:
- Included: path groups and why they belong.
- Excluded: unrelated dirty paths or none.

Validation:
- command -> outcome

Post-commit:
- Working tree: clean | dirty with listed paths.
- Residual risk: none | concrete issue.
```

Quality gate:

- Pass when the branch/spec relationship is explicit, the commit contains only related files, validation is current, message validation passes, and post-commit status is reported.
- Fail when branch/spec mismatch is hidden, unrelated files are staged, validation is stale, the message validator fails, or the final report hides a dirty tree.

## Examples

Valid staging rationale:

```text
Staging:
- Included: `skills/*/SKILL.md` because every file is part of the skill instruction upgrade.
- Included: `specs/177-skill-instruction-upgrade/*` because the SDD package documents this change.
- Excluded: `apps/web/.env.local` because it is unrelated and sensitive.
```

Invalid counter-example:

```text
Ran git add -A and committed everything.
```

Reject this when the working tree contains files not inspected for scope.

## Edge Cases

- Stop and ask before staging when unrelated changes are mixed inside a file required for the current change.
- Stop and resolve branch state with `$ai-sdlc-branching` when medium or large work is still on `dev`, `main`, `master`, or a branch that does not include the active spec slug.
- Use `--allow-unstaged` on the readiness checker only when unrelated unstaged files are intentionally left out and reported.
- Do not amend an existing commit unless the user explicitly requests amend.
- Do not run destructive cleanup commands unless the user requested or approved them.
- Report failed commit hooks with the hook output and do not claim a commit exists.

## Scope Boundary

- Do not draft commit message content without `$ai-sdlc-conventional-commit`.
- Do not decide test coverage; use `$ai-sdlc-test-cases`, `$ai-sdlc-qa`, and `$ai-sdlc-validation`.
- Do not revert user changes to make staging easier.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
