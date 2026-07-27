# Validate and Handoff — ai-sdlc-doctor: Diagnostics And Safe Upgrade Plans

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Doctor checks have stable codes, statuses, evidence, and remediation. Upgrade
plans contain exact hashes, schema transitions, backup destinations, rollback
actions, compatibility blockers, and deterministic identity.

## Scope Boundary

- Do not install dependencies or modify the installation.
- Do not execute remediation, backup, migration, apply, or rollback actions.
- Do not hide incompatible or destructive changes behind an aggregate status.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
