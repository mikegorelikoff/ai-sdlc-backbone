# Execute — ai-sdlc-ux: Traceable Experience Specification

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/ux-contract.md` for actor, journey, state, and accessibility fields.
- Use `scripts/ux.py` to validate and route the canonical artifact pair.

## Script Usage

```bash
python3 skills/ai-sdlc-ux/scripts/ux.py specs-refiniment/onboarding --input /tmp/ux.json --emit --quick-flow
python3 skills/ai-sdlc-ux/scripts/ux.py specs/onboarding --input /tmp/ux.json --write --full-flow --format toon
```

## Purpose

Add explicit experience behavior where it creates value without forcing visual
design work into every delivery path or reducing UX to generic acceptance prose.

## Inputs

- Define stable actor IDs, goals, and needs.
- Trace every journey, state, and accessibility check.
- Make steps ordered and acceptance outcomes observable.
- Cover recovery from failure and blocked user states.

## Steps

1. Read customer/problem evidence, requirements, actors, and constraints.
2. Define actors and their goals without inventing research claims.
3. Map end-to-end journeys with ordered steps and acceptance outcomes.
4. Specify loading, empty, error, permission, success, and recovery states.
5. Define accessibility requirements and evidence status.
6. Finalize routed Markdown and TOON outputs.
7. Route behavior changes to BA/SDD and test cases.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
