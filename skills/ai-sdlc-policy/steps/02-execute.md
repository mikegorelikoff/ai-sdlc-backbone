# Execute — ai-sdlc-policy: Explainable Delivery Controls

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/policy-contract.md` before resolving or evaluating policy.
- Validate source layers with `references/policy-layer.schema.json`, waivers
  with `references/policy-waiver.schema.json`, and decisions with
  `references/policy-decision.schema.json`.
- Reuse organization profiles from `references/profiles/`.
- Use `scripts/policy.py` for resolution, evaluation, and explain output.

## Script Usage

```bash
python3 skills/ai-sdlc-policy/scripts/policy.py . --resolve --profile high-assurance --format toon
python3 skills/ai-sdlc-policy/scripts/policy.py . --evaluate change.apply --context policy-context.json --profile regulated --format toon
python3 skills/ai-sdlc-policy/scripts/policy.py . --explain release.publish --context release-context.json --waiver waiver.json --format markdown
```

## Purpose

Make delivery governance reproducible and inspectable while allowing bounded,
accountable, expiring exceptions without silently weakening organization rules.

## Inputs

- Versioned base, organization, project, and user policy layers.
- A stable action such as `change.apply`, `release.publish`, or
  `command.destructive` and a JSON context object.
- Optional waiver files tied to exact rule IDs, actions, subjects, constraints,
  owners, approvers, decisions, issue times, and expiry times.

## Steps

1. Load the built-in base and optional organization assurance profile.
2. Validate custom layers and merge them in base, organization, project, user order.
3. Reject any lower-layer change that weakens a protected effect, gate set,
   protected flag, or non-waivable boundary.
4. Match rules using only declared fields and deterministic operators.
5. Validate waivers against rule eligibility, action, subject, constraints,
   decision evidence, and the explicit evaluation time.
6. Combine unwaived rules with deny-first, require-second, allow-third precedence.
7. Inspect explain output and satisfy every required gate before acting.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
