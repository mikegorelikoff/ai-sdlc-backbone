# Execute — ai-sdlc-code-review: Code Review

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/review-checklist.md` when the task needs the detailed structure, checklist, or examples for this skill.
- Use `scripts/review_readiness.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.

## Script Usage

- Run review readiness before producing findings when reviewing diffs, branches, staged changes, or full-repo surfaces.
- Quick flow: `python3 skills/ai-sdlc-code-review/scripts/review_readiness.py --quick-flow`
- Full flow with spec: `python3 skills/ai-sdlc-code-review/scripts/review_readiness.py --full-flow --spec specs/<feature-name>`
- Branch review: add `--base <branch-or-commit>`; broad audit: use `--full-repo` instead of `--base`.
- Treat errors as blockers; treat warnings as review focus areas unless the user explicitly narrowed scope.

## Purpose

Review AI SDLC code, diffs, branches, commits, or completed implementations for correctness, regressions, contract drift, missing tests, SDD drift, and material maintainability risks.

## Inputs

- Collect the review target: staged diff, unstaged diff, branch, commit, PR, package, or subsystem.
- Run `git status --short` and `git diff --stat` for local diffs.
- Read the relevant diff:
  - staged: `git diff --cached`
  - unstaged: `git diff`
  - branch: `git diff <base>...HEAD`
- Read relevant `requirements.md`, `design.md`, `test-cases.md`, `qa.md`, `tasks.md`, `_ai_sdlc/plan.toon`, and `plan.md` for medium or large work.
- Read validation output or record that it is absent.
- Read `references/review-checklist.md` for deep-audit mode or complex surfaces.

## Steps

1. Identify review mode: normal review or deep-audit review.
2. Define the exact review boundary before judging code.
3. Read requirements, acceptance criteria, tests, and the diff first. Do not read AI implementation rationale, prior review verdicts, or approval summaries yet.
4. Record independent findings, including an explicit `No findings.` result for a clean pass.
5. Only after step 4, reveal AI rationale or prior verdicts and compare them with the independent findings; preserve disagreements in the review evidence.
6. Use the `review` subagent only when the user requested review work and the active runtime policy permits delegation; otherwise perform the review locally.
7. Inspect high-risk files first: handlers, services, workflows, providers, config, schema, migrations, generated contracts, tests, and repo-local automation runtime files.
8. Compare implementation against spec requirements, design contracts, task scope, and validation evidence.
9. Check authorization, data integrity, state transitions, decimal math, asset identifiers, provider routing, errors, observability, and exported Go doc comments when touched.
10. Escalate to `$ai-sdlc-security-testing` when exploitability, auth boundaries, secrets, or abuse paths are the primary concern.
11. Report findings first, ordered by severity.
12. Report validation gaps and residual risks after findings.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
