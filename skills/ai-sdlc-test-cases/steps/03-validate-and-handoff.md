# Validate and Handoff — ai-sdlc-test-cases: Test Cases For Implementation

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Use this format:

```text
Scope:
- In scope:
  - Behavior, contract, endpoint, workflow, or artifact covered.
- Out of scope:
  - Behavior, contract, endpoint, workflow, or artifact deliberately excluded.

Scenario matrix:
| ID | Requirement ref | Scenario | Setup | Trigger | Verifiable outcome | Layer | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-001 | AC-001, story ID, workflow, risk, or artifact section | Scenario name | Fixture/state | Action | Command, checklist, or before/after pair | unit/service/transport/integration/QA/manual | script path + invocation, CI step, or manual blocker |

Automation plan:
- TC-001: exact command or CI step, target file if new, expected pass condition.

Execution order:
1. Layer: run condition; blocks: later layer or release gate; failure action: stop, fix, rerun, or escalate.

Decisions required:
- Question: decision needed.
  Options:
  A. Option A
  B. Option B
  C. Option C
  Recommended default: option and reason.
  Owner: role or person.
  Blocking: yes | no.
```

Quality gate:

- Pass when every scenario has scope fit, requirement ref, setup, trigger, verifiable outcome, layer, concrete automation path, and execution-order placement.
- Pass when every manual scenario uses `Manual — automate by YYYY-MM-DD — blocker: reason`.
- Pass when every unresolved item is a structured decision with options and recommended default.
- Fail when any scenario lacks a spec ref, uses prose-only expected outcomes, says only `Manual review`, contains `TODO`, or leaves layer mapping as descriptive text instead of execution order.

## Examples

Valid executable scenario:

```text
Scenario matrix:
| ID | Requirement ref | Scenario | Setup | Trigger | Verifiable outcome | Layer | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-003 | AC-003 | Reject unsupported provider asset | BitGo wallet fixture contains BTC only | Submit a USDC transfer request | `GOCACHE=/tmp/ai-sdlc-go-cache go test ./internal/service -run TestRejectUnsupportedProviderAsset -count=1` exits 0 and asserts no transfer row is created | service | `skills/ai-sdlc-validation/scripts/validation_plan.py internal/service/transfer_service.go`; implement `TestRejectUnsupportedProviderAsset` |

Execution order:
1. Service tests: run after scenario matrix is approved; blocks transport tests; failure action: fix service validation and rerun focused service test.

Decisions required:
- Question: Should unsupported provider assets return 400 validation error or 409 conflict?
  Options:
  A. 400 validation error
  B. 409 conflict
  C. Provider-specific 502
  Recommended default: A, because the request is invalid before provider submission.
  Owner: Delivery Manager
  Blocking: yes
```

Invalid counter-example:

```text
| TC-003 |  | Test bad inputs | Existing tests | Run tests | Service rejects bad data | service | Manual review |
```

Reject this because it has no spec ref, the outcome is prose-only, and `Manual review` has no blocker or automation date.

## Edge Cases

- Mark expected behavior as a structured decision when the spec is silent and code behavior is inconsistent.
- Prefer lower-layer tests when they prove the behavior without full integration setup.
- Use integration tests only when provider adapters, HTTP contracts, migrations, or cross-package behavior must be exercised together.
- Mark flaky or external-service-dependent scenarios as manual only with `Manual — automate by YYYY-MM-DD — blocker: reason`.
- Do not invent provider responses; use documented fixtures, existing mocks, or a structured decision with a recommended default.
- Do not output `TODO`, `TBD`, `manual review`, or `needs confirmation` as a final gap.

## Scope Boundary

- Do not claim QA signoff; use `$ai-sdlc-qa`.
- Do not choose final validation command execution; use `$ai-sdlc-validation`.
- Do not implement production behavior from this skill alone; use `$ai-sdlc-sdd` and approved `tasks.md`.
- Do not add broad snapshot tests when focused assertions can prove the behavior.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
