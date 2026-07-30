# Execute — ai-sdlc-architecture: Traceable System Design

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/architecture-contract.md` for the input schema and design gates.
- Use `scripts/architecture.py` to validate and route canonical outputs.

## Script Usage

```bash
python3 skills/ai-sdlc-architecture/scripts/architecture.py specs/payments --input /tmp/architecture.toon --emit --quick-flow
python3 skills/ai-sdlc-architecture/scripts/architecture.py specs/payments --input /tmp/architecture.toon --write --full-flow --format toon
```

## Purpose

Add architecture depth when a feature needs it without making architecture
ceremony or the optional module a dependency of every core workflow.

## Inputs

- Capture design context and constraints before components.
- Trace interfaces and decisions to durable requirement or decision IDs.
- Give risks an owner and mitigation.
- Provide executable or inspectable validation evidence.

## Steps

1. Read requirements, decisions, project context, state, and relevant quality findings.
2. Define boundaries, constraints, components, and interfaces.
3. Compare alternatives and record decisions plus consequences.
4. Identify architecture risks, owners, and mitigations.
5. Define validation checks for the design claims.
6. Finalize canonical outputs with the deterministic script.
7. Route implementation changes through SDD tasks and validation.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
