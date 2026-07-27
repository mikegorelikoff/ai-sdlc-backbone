# Validate and Handoff — ai-sdlc-conventional-commit: Conventional Commit Message

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Return a complete commit message, not a paragraph about the message:

````text
type(scope): imperative summary


Spec: specs/NNN-feature-name
Task: TNNN

Business context:
One or two sentences explaining why the change matters to product, operations, risk, clients, QA, or delivery governance.

Implementation details:
- Concrete code, contract, doc, workflow, provider, schema, or validation changes.
- Important compatibility, rollout, or failure-mode decisions.

Change flow:
```text
Actor or trigger -> changed AI SDLC path -> business-visible outcome
```

How to test:
1. Reviewer-visible happy path or documentation path.
2. Important permission, failure, boundary, regression, or governance path.

Validation:
- command -> outcome
````

Quality gate:

- Pass when the subject is Conventional Commit compliant, required Spec/Task
  traceability is present, validation commands are exact, and every required
  body section contains concrete project-specific content.
- Fail when the message uses placeholders, omits required traceability, hides failed validation, or describes implementation in vague terms such as "updated stuff" or "improved docs".

## Examples

Valid medium-change message:

````text
docs(skill): upgrade repo-local skill instructions


Spec: specs/177-skill-instruction-upgrade
Task: T001, T002

Business context:
This makes AI skill usage deterministic for future AI SDLC work and reduces reviewer effort caused by vague skill outputs.

Implementation details:
- Rewrote every repo-local skill with Purpose, Inputs, Steps, Output spec, Examples, Edge cases, and Scope boundary.
- Added a skill index that maps each workflow phase to the correct skill.

Change flow:
```text
Skill audit -> normalized SKILL.md files -> consistent AI assistant behavior
```

How to test:
1. Read a cold skill and confirm it contains a complete execution contract.
2. Run skill and spec validators for the updated files.

Validation:
- PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-harness-pycache python3 -m py_compile skills/ai-sdlc-validation/scripts/validation_plan.py -> passed
- git diff --check -> passed
````

Invalid counter-example:

```text
updates

Made skills better.
```

Reject this because the subject is not Conventional Commit syntax, traceability is absent, and validation evidence is missing.

## Edge Cases

- Include `BREAKING CHANGE:` even for documentation-only commits when the documented workflow intentionally retires a previously required control.
- Use `revert: ...` only when the commit actually reverts a previous commit; include the reverted hash in the body.
- Stop and fix the message when the validator fails; do not commit with an invalid message.
- State failed or skipped validation honestly in the `Validation` section with the residual risk.

## Scope Boundary

- Do not stage files or create commits; use `$ai-sdlc-commit-prep` for staging and commit execution.
- Do not invent validation results; use `$ai-sdlc-validation` to choose and run checks.
- Do not use this skill to summarize a diff unless the output is a commit message.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
