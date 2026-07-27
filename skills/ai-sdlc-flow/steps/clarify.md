# Clarify — Guided Explore and Apply

> Selector: clarify

## Entry

Resolve only the material role, action, scope, or rigor ambiguity needed to produce a deterministic route.

## Procedure

### 0.1 Required Inputs

- Repository root and natural-language intent.
- Canonical `NNN-kebab-case` feature when durable feature work is expected.
- Optional explicit quick/full rigor.
- Optional `--role` and `--action` overrides plus bounded `--team` and `--user`
  configuration layers.

### 0.2.1 Flow Mode Flags

- `--quick-flow` requests quick rigor when risk and policy permit it.
- `--full-flow` requests full rigor and takes precedence.
- Explore explains every automatic choice or override.

## Role and Rigor Rule

Activate exactly one of Business Analyst, Product Manager, Software Architect,
Software Engineer, or QA Engineer. The selected action owner is active; an
explicit different role produces a transparent handoff rather than two active
roles. Each role reference declares its mission, ownership, entry signals,
boundaries, workflow, selectors, and handoffs. Recommend quick for bounded,
reversible work and full for cross-cutting, ambiguous, security, data, or
architecture work.

## Existing Phase Guidance

# Clarify

Present the deterministic action menu. Ask only for the role or action needed to resolve material ambiguity. Do not load feature context or mutate lifecycle state.

## Exit

Return one explicit role/action choice or a bounded deterministic menu; perform no mutation.
