# Validate and Handoff — ai-sdlc-sdd: Specification-Driven Development

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Use this completion report:

```text
SDD compliance:
- Spec: specs/NNN-feature-name
- Change size: small | medium | large
- Requirements: updated | unchanged with reason
- Design: updated | unchanged with reason
- Test cases: updated | unchanged with reason
- QA: updated | unchanged with reason
- Tasks: completed task numbers and remaining task numbers
- Plan: `_ai_sdlc/plan.toon` and `plan.md` updated | unchanged with reason
- Validation: command -> outcome
- Scope control: no drift | drift and spec update
- Residual risk: none | concrete issue
```

Quality gate:

- Pass when the SDD package exists, required sections are populated, `_ai_sdlc/plan.toon` links AC/TC/TASK/DEC status and dependencies, `plan.md` reflects those links for humans, tasks match implementation, and the validator passes.
- Fail when code starts before missing spec artifacts are created, when implementation exceeds `tasks.md`, when the clarify/checklist/analyze gates fail, or when task checkboxes are marked complete without evidence.

## Examples

Spec folder shape:

```text
specs/177-skill-instruction-upgrade/
  requirements.md
  design.md
  test-cases.md
  qa.md
  tasks.md
  _ai_sdlc/plan.toon
  plan.md
```

Completion report sample:

```text
SDD compliance:
- Spec: specs/177-skill-instruction-upgrade
- Change size: medium
- Requirements: updated
- Design: updated
- Test cases: updated
- QA: updated
- Tasks: 1-10 completed
- Plan: _ai_sdlc/plan.toon and plan.md updated
- Validation: python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/177-skill-instruction-upgrade -> passed
- Scope control: no drift
- Residual risk: none
```

Invalid counter-example:

```text
Implemented feature; will write spec later.
```

Reject this for medium and large work because the spec is the source of truth.

## Edge Cases

- Reuse an existing active spec when its requirements clearly match the user request.
- Create a new spec when an existing completed or archived spec is only historically related.
- Add `TODO(dm): exact question` when a required decision cannot be discovered and guessing would affect scope, contract, security, or rollout.
- Use `Assumptions`, `Open Questions`, and `Decision Status` sections in `requirements.md` for clarify-gate evidence.
- Update the spec first when code and spec conflict during an active change.
- Treat unlisted historical numbered specs as `unclassified` until `specs/spec-registry.md` says otherwise.
- Do not treat scaffolded historical `qa.md` or `test-cases.md` files with unresolved TODOs as validated evidence.
- Treat missing `_ai_sdlc/plan.toon` or `plan.md` as a structural SDD failure, even in quick flow.
- When `tasks.md`, `_ai_sdlc/plan.toon`, and `plan.md` disagree, trust the
  reviewed checkbox state in `tasks.md` and regenerate both projections with
  `plan_links.py --write`. Investigate unexpected drift before continuing.
- In full flow, treat missing upstream refinement delivery or QA readiness as a blocker unless the predecessor is explicitly skipped with a decision reference.

## Scope Boundary

- Do not replace BA, test-case, QA, review, security, validation, or commit-prep skills; route to them when their phase is needed.
- Do not implement major features without requirements, design, test cases, QA, tasks, and plan.
- Do not run broad validation by default; use `$ai-sdlc-validation` for command selection.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
