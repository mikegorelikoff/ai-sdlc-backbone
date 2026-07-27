# Execute — ai-sdlc-validation: Validation Command Selection

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/run_validation.py` to execute a human-reviewed JSON argv plan
  without a shell and write `_ai_sdlc/validation-receipt.json` containing actual
  exit codes, revision/diff identity, environment, duration, and output digests.
  The runner rejects executable paths, Python `-c`, mutating Git, and unbounded
  downloader/build command families, but repository test/scripts still execute
  code and require the normal sandbox. Use `--verify` before full-flow commit
  readiness. The local self-hash is forgeable by a workspace writer and proves
  neither authenticated execution nor human approval; protected CI is the
  independent source when that assurance is required. A receipt also does not
  prove that the tests express the right requirement.
  Store the reviewed plan as `_ai_sdlc/validation-plan.json` beside the receipt;
  the receipt binds its path and digest. The runner requires a valid Git `HEAD`,
  streams bounded output (10 MB total by default), and terminates a noisy or
  timed-out process group rather than retaining unbounded output in memory.
- `run_validation.py --complete-state` is intentionally rejected. Write
  finalized `validation.md`, execute the final plan, rerun it with `--verify`,
  then complete the validation stage with `state_machine.py complete`; completion revalidates
  the current receipt and rejects failed, malformed, forged, or stale evidence.
  Canonical `state.toon`, specs indexes, and downstream review/commit artifacts
  are derived evidence excluded from the workspace fingerprint; changing
  validated source, specs, tests, `validation.md`, or the plan still makes the
  receipt stale.

- Use `scripts/validation_plan.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.

## Script Usage

- Run validation planning after identifying changed files and before choosing commands manually.
- Quick flow: `python3 skills/ai-sdlc-validation/scripts/validation_plan.py --quick-flow <changed-file>...`
- Full flow: `python3 skills/ai-sdlc-validation/scripts/validation_plan.py --full-flow <changed-file>...`
- If no files are supplied, the script inspects the current git worktree.
- Execute the suggested commands that match the requested risk level; document skipped broader commands as residual risk.

## Purpose

Select, run, and report focused deterministic validation checks for AI SDLC code, SQL, API, provider, SDD, documentation, and tool-governance changes.

## Inputs

- Collect changed files from `git status --short`, `git diff --name-only`, or explicit user-provided paths.
- Read the active spec and `qa.md` when the work is medium, large, release-sensitive, or user-visible.
- Collect previous validation output only when it is current for the same diff signature.
- Collect sandbox constraints that affect Go cache, network access, local listeners, or external services.
- Run the validation planner when changed files are not trivial:

  ```bash
  python3 skills/ai-sdlc-validation/scripts/validation_plan.py
  ```

## Steps

1. Classify changed files by surface: Go package, SQL/sqlc, API contract, provider integration, frontend/docs, SDD/spec, tool governance, or mixed.
2. Select the narrowest command set that proves the changed behavior.
3. Prefer focused tests before broad suites when the risk is localized.
4. Use `GOCACHE=/tmp/ai-sdlc-go-cache` for Go tests to avoid sandbox cache write failures.
5. Run spec and skill validators for SDD, skill, helper script, or spec changes.
6. For active feature specs, run structural SDD validation plus clarify,
   checklist, analyze, and workflow-status commands when the spec changed or is
   the main subject of the work.
7. Run `git diff --check` for every change before completion.
8. Rerun with escalation only when a required command fails due to sandbox restrictions and the command is still necessary.
9. Record each command exactly as run and its outcome: passed, failed, skipped, or blocked.
10. Fix failures caused by the current change before reporting success.
11. Report skipped or blocked checks with residual risk.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
