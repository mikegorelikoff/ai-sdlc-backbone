# Validate and Handoff — ai-sdlc-validation: Validation Command Selection

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Use this format:

```text
Validation:
- command: exact command
  outcome: passed | failed | skipped | blocked
  reason: why this command was selected or skipped

Coverage:
- Changed surface: files or package group.
- Behavior covered: requirement, scenario, or risk covered by the command.

Residual risk:
- none | explicit unvalidated behavior and why it remains.
```

Quality gate:

- Pass when validation commands match the changed surfaces, required checks are current for the active diff, and skipped checks include residual risk.
- Fail when validation is broad but irrelevant, narrow but misses a changed contract, or reports success while a command failed.

## Examples

Focused Go package change:

```text
Validation:
- command: GOCACHE=/tmp/ai-sdlc-go-cache go test ./internal/service -run 'TestLoanTransfer|TestReturnPreflight' -count=1
  outcome: passed
  reason: covers changed service behavior and preflight failure paths.
- command: git diff --check
  outcome: passed
  reason: required whitespace validation for all changes.

Residual risk:
- none
```

Tool setup change:

```text
Validation:
- command: PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-harness-pycache python3 -m py_compile skills/ai-sdlc-validation/scripts/validation_plan.py
  outcome: passed
  reason: validates changed skill metadata.
- command: python3 skills/ai-sdlc-sdd/scripts/sdd_status.py --spec specs/185-spec-kit-sdd-quality-gates
  outcome: passed
  reason: confirms the active governance spec is structurally valid and ready for implementation.
- command: find skills -name SKILL.md -maxdepth 2
  outcome: passed
  reason: validates SDD governance shape.
```

Invalid counter-example:

```text
Validation passed.
```

Reject this because it omits exact commands, changed surface coverage, and residual risk.

## Edge Cases

- Mark a check `blocked` when sandbox, missing dependency, missing credential, or unavailable service prevents execution.
- Request escalation only after a required command fails for a likely sandbox reason; do not escalate to bypass project policy.
- Run broader suites after focused checks when the changed surface spans handlers, services, providers, config, or generated contracts.
- Do not run production integrations unless the user explicitly requests them and required credentials are already available through approved mechanisms.
- Treat stale validation as absent when files changed after the command ran.

## Scope Boundary

- Do not design acceptance scenarios; use `$ai-sdlc-qa`.
- Do not derive scenario matrices; use `$ai-sdlc-test-cases`.
- Do not review code for findings; use `$ai-sdlc-code-review` or `$ai-sdlc-security-testing`.
- Do not mark work done when validation is failed, blocked without disclosure, or unrelated to the changed surface.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
