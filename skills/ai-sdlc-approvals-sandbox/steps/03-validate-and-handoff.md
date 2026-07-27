# Validate and Handoff — ai-sdlc-approvals-sandbox: Approvals And Sandbox

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Return this decision record when escalation is requested, denied, or skipped:

```text
Sandbox decision:
- Command: sanitized command with every secret-bearing value shown as <redacted>
- Required for: task-specific reason
- Sandbox issue: filesystem | network | listener | GUI | external service | destructive | none
- Escalation: requested | not requested | denied | granted
- Prefix rule: proposed rule | none and why
- Result: passed | failed | skipped | blocked
- Residual risk: none | concrete limitation
```

Quality gate:

- Pass when escalation is narrow, justified by the task, and avoids broad reusable approval for dangerous commands.
- Fail when the request uses vague justification, proposes broad interpreter or shell prefixes, includes secrets, or escalates unrelated work.

## Examples

Valid request:

```json
{
  "sandbox_permissions": "require_escalated",
  "justification": "Allow running Go tests with a writable external cache for this package?",
  "prefix_rule": ["go", "test", "./internal/service/..."]
}
```

Invalid counter-example:

```json
{
  "sandbox_permissions": "require_escalated",
  "justification": "Need permissions.",
  "prefix_rule": ["python3"]
}
```

Reject this because the justification is vague and the prefix allows arbitrary scripts.

## Edge Cases

- Skip reusable `prefix_rule` for destructive commands such as `rm`, `git reset`, force push, or data deletion.
- Skip reusable `prefix_rule` for heredocs, redirection, wildcards, command substitution, environment-heavy one-liners, or shell wrappers.
- Warn immediately and avoid reusing commands when a command contains credentials, bearer tokens, private keys, webhook secrets, or production-only values.
- Never repeat the raw secret-bearing command while warning; refer only to the
  sanitized structure and the credential category.
- Treat a missing dependency error as a setup issue first, not an escalation reason, unless the dependency download is required and network is blocked.
- Report partial approval when one command segment is approved but another remains blocked.

## Scope Boundary

- Do not decide which validation commands are required; use `$ai-sdlc-validation`.
- Do not approve destructive commands on the user's behalf.
- Do not weaken developer SDD, review, or validation requirements because sandbox permissions are inconvenient.
- Do not replace the active runtime’s higher-priority sandbox and approval policies.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
