# Execute — ai-sdlc-approvals-sandbox: Approvals And Sandbox

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/approval_plan.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.

## Script Usage

- Validate approval requests before asking for escalation or recording an approval decision.
- Quick flow: `python3 skills/ai-sdlc-approvals-sandbox/scripts/approval_plan.py --quick-flow --command "<command>" --justification "<user-facing question?>"`
- Full flow: `python3 skills/ai-sdlc-approvals-sandbox/scripts/approval_plan.py --full-flow --command "<command>" --justification "<user-facing question?>" --prefix-rule "<safe reusable prefix>"`
- Use `--prefix-rule` only when proposing a reusable non-destructive approval prefix; omit it for destructive or one-off commands.

## Purpose

Decide, request, and report sandbox escalation for AI SDLC commands only when the sandbox blocks a required action or the task explicitly requires approved external access.

## Inputs

- Collect the command structure that failed or must run outside the sandbox;
  redact secret-bearing values before collecting or returning it.
- Collect the task reason that makes the command necessary.
- Collect the sandbox error or expected restriction: filesystem, network, listener, GUI, external service, or destructive action.
- Collect whether the command is destructive, secret-bearing, shell-heavy, or reusable.
- Collect an intended narrow `prefix_rule` only when repeated approval is safe.

## Steps

1. Run normal reads, workspace writes, local tests, and formatting in the default sandbox first.
2. Classify the command into one segment per shell operator when the command contains pipes, separators, logical operators, or subshells.
3. Request escalation only when a required command is blocked by sandbox restrictions or explicitly needs approved external access.
4. Do not request escalation to bypass SDD, skip validation, avoid fixing a local setup issue, or run unrelated broad commands.
5. Validate the approval plan before asking when time permits:

   ```bash
   python3 skills/ai-sdlc-approvals-sandbox/scripts/approval_plan.py \
     --command 'go test ./internal/service/...' \
     --justification 'Allow running focused service tests with the required sandbox permissions?' \
     --prefix-rule 'go test ./internal/service/...'
   ```

6. Phrase `justification` as a short user-facing question.
7. Provide `prefix_rule` only for narrow, reusable, non-destructive command classes.
8. Rerun the command only after approval is granted.
9. Report denied or partial approval and continue with the best safe fallback.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
