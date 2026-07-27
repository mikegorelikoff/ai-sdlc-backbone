# Validate and Handoff — ai-sdlc-code-review: Code Review

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Use this format:

```text
Findings:
- [CRITICAL|HIGH|MEDIUM|LOW] path:line - concise issue statement.
  Why it matters: concrete failure, regression, or maintenance risk.
  What should change: specific fix or test.

Open questions:
- Only blockers or assumptions that affect correctness, scope, or severity.

Validation gaps:
- Missing, failed, skipped, or stale checks.

Secondary observations:
- Deep-audit mode only; material non-blocking observations.

Summary:
- Brief change summary after findings.
```

Quality gate:

- Pass when every finding has a path, severity, impact, and fix; no-finding reports still include validation gaps.
- Fail when the review starts with a summary, lists style nits as findings, omits spec comparison for medium/large work, or hides missing validation.

## Examples

Finding example:

```text
Findings:
- [HIGH] internal/service/orders.go:218 - Accepted orders can be repriced after execution because the status guard excludes only cancelled orders.
  Why it matters: A borrower could see a different rate after the lender accepted the order, violating the order contract.
  What should change: Reject repricing unless the order is still in draft or requested state, and add a service test for accepted orders.
```

No-finding example:

```text
Findings:
- None found.

Validation gaps:
- `go test ./internal/service` was not run, so service-level regressions remain unverified.

Summary:
- Reviewed the staged service diff against `specs/NNN-feature-name`; no material defects found.
```

Invalid counter-example:

```text
Looks good. Nice cleanup.
```

Reject this because it is not findings-first and does not mention validation.

## Edge Cases

- State `target unclear` and ask for the review boundary when no diff, commit, branch, or subsystem is available.
- Keep docs-only review lightweight unless docs change SDD policy, API contracts, setup, security, or validation behavior.
- Use deep-audit mode only when the user asks for a broad pass or the surface spans multiple high-risk areas.
- Do not spawn subagents when the active runtime requires explicit permission and the user did not request delegation.
- Report stale validation when files changed after tests ran.
- Treat hook-driven review as advisory-first; warnings do not replace human-readable findings.

## Scope Boundary

- Do not edit code during review unless the user explicitly asks for fixes.
- Do not perform security-focused exploitability review as a side effect; use `$ai-sdlc-security-testing`.
- Do not choose final validation commands except to identify gaps; use `$ai-sdlc-validation`.
- Do not approve scope changes that are missing from `tasks.md`; require a spec update first.

## Hook Policy

- Skip automatic review for docs-only or metadata-only changes with no code, config, hook, spec-runtime, or test behavior impact.
- Require review for non-trivial production code, repo-local automation logic, config, hook, workflow, provider, transport, schema, or test changes.
- Recommend deep audit for high-churn surfaces, multiple risk categories, or changes spanning handlers, services, providers, and config.
- Keep hook enforcement advisory-first; emit warnings before hard blocks.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
