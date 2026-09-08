# Validate — Discovery Quality

## Entry

A draft packet and its sources are available.

## Procedure

- Run `requirements_discovery.py validate` against the current context and
  draft, then `verify` after durable finalization. The helper rejects malformed
  fields, duplicate/dangling IDs, uncovered material gaps or candidate options,
  missing question owners/methods, unsupported outcome or decision records,
  source drift and report/projection tampering.
- Confirm the same inputs and explicit date yield stable output; never claim
  that serialization determinism makes the model's reasoning deterministic.

- Trace material claims to sources or explicit assumptions. Check that a past
  proposal is not labeled a successful implementation and absent history is
  disclosed rather than filled with invented examples.
- Check that alternatives differ in business behavior, respect confirmed
  constraints and explain precedent transfer limits and disqualifying evidence.
- Ensure every material contradiction or decision-changing gap has an owner
  role, priority and answer method. Each viable option has targeted questions.
- Check questions are neutral, specific and answerable, with the evidence
  location and decision consequence; remove questions already answered.
- Verify no unresolved choice is presented as approved, no proposed acceptance
  rule is asserted as fact, and no stakeholder communication has been sent
  merely because a question was drafted.
- For requested durable output, validate the product's format, contained route
  and source references. A structurally complete packet may still have open
  business decisions; report both states independently.

## Exit

Return quality findings, evidence limitations and remaining decision blockers.
