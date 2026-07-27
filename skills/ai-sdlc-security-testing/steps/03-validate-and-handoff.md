# Validate and Handoff — ai-sdlc-security-testing: Security Testing

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Use this findings-first format:

```text
Findings:
- [CRITICAL|HIGH|MEDIUM|LOW] path:line - concise issue statement.
  Impact: exploitable outcome.
  Evidence: code path, input, state, or missing check.
  Fix: concrete remediation.

Verified sources:
- Required when the output uses OWASP or standards-based claims.
- Include the current primary source link and the specific claim it supports.

Open questions:
- Trust-boundary or exploitability question that blocks severity or fix selection.

Validation gaps:
- Missing security test, QA check, or command and why it matters.

Summary:
- Brief security posture summary after findings.
```

Quality gate:

- Pass when every finding is tied to a concrete path, exploit condition, impact, and fix.
- Fail when the output recites generic OWASP categories, cites standards from memory without verification, inflates speculative issues, omits severity, or hides missing validation.

## Examples

Finding example:

```text
Findings:
- [HIGH] internal/transport/http/v1/handlers/transfers.go:142 - Transfer lookup does not verify organization ownership before returning wallet metadata.
  Impact: A user with access to one organization could enumerate another organization's provider wallet labels.
  Evidence: Handler uses transfer ID from the route and returns provider details before checking org ownership.
  Fix: Load the transfer through an organization-scoped query or compare `transfer.OrganizationID` before building the response.
```

No-finding example:

```text
Findings:
- None found.

Validation gaps:
- No automated test covers replay of duplicate webhook IDs; add a service-level idempotency test before release.
```

Invalid counter-example:

```text
Security looks fine.
```

Reject this because it omits reviewed boundaries, findings status, and validation gaps.

## Edge Cases

- Stop and warn immediately if real secrets, bearer tokens, private keys, or production-only values appear in the diff; do not paste them back.
- State `target unclear` when no diff, endpoint, workflow, or subsystem is provided and local context cannot infer one safely.
- Use `$ai-sdlc-code-review` when the main ask is correctness, regression, or maintainability rather than exploitability.
- If browsing or primary-source verification is unavailable, report `standards verification blocked` and limit the output to locally supported exploitability findings instead of presenting unverified OWASP guidance.
- Mark validation as blocked when required credentials, fixtures, or environment are unavailable.
- Do not lower severity because a path is "internal" unless the trust boundary proves only trusted callers can reach it.

## Scope Boundary

- Do not perform general code review unless security is the primary question.
- Do not run production attacks, live exploitation, or credentialed provider actions.
- Do not expose sensitive values in findings, tests, comments.
- Do not decide business acceptance; use `$ai-sdlc-ba` and `$ai-sdlc-qa`.
- Do not cite OWASP categories, ASVS controls, or standards versions from memory when current-source verification is required.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
