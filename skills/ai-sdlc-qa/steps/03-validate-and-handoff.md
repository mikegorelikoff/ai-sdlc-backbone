# Validate and Handoff — ai-sdlc-qa: QA Planning And Evidence

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Use this format:

```text
QA plan:
- Change boundary: one sentence.

Acceptance scenarios:
- QA-001:
  Actor: role or system.
  Setup: required state.
  Action: user/API/system action.
  Expected result: observable result.
  Evidence: automated test | manual check | not yet covered.
  Risk: high | medium | low and reason.

Regression targets:
- Existing behavior and why it is at risk.

Validation evidence:
- command -> passed | failed | skipped: reason.

Manual checks:
- Check, environment, expected result, and owner if known.

Signoff:
- Ready | blocked | partial, with reason.
```

Quality gate:

- Pass when every acceptance scenario has actor, setup, action, expected result, evidence, and risk.
- Fail when a scenario says only "verify it works", when skipped validation has no reason, or when the plan claims a pass without executed evidence.

## Examples

Valid QA scenario:

```text
- QA-001:
  Actor: operations user.
  Setup: organization has BitGo configured with one enterprise wallet.
  Action: open the custodian setup endpoint.
  Expected result: response includes the BitGo enterprise ID and wallet display label without exposing secrets.
  Evidence: transport test plus manual API response review.
  Risk: high because incorrect wallet scope can block settlement operations.
```

Invalid counter-example:

```text
Acceptance scenarios:
- Test the endpoint.
```

Reject this because it lacks setup, action, expected result, evidence, and risk.

## Edge Cases

- State `blocked` when no environment, fixture, credentials, or sample payload exists for a manual check.
- Do not mark manual QA as passed from code inspection alone.
- Mark flaky or nondeterministic evidence as partial and name the unstable dependency.
- Use redacted examples for provider payloads; never include secrets or production-only values.
- Keep QA signoff separate from developer validation when acceptance requires human workflow review.

## Scope Boundary

- Do not implement automated tests; use `$ai-sdlc-test-cases` to design tests and normal coding workflow to implement them.
- Do not select broad test suites by default; use `$ai-sdlc-validation`.
- Do not approve product scope; use `$ai-sdlc-ba` for unresolved business decisions.
- Do not claim release readiness when validation, manual checks, or signoff are incomplete.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
