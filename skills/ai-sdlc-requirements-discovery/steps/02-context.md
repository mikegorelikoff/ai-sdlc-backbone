# Context — Sources and Precedents

## Entry

The raw request and source boundary are known.

## Procedure

- Start with provided notes, selected requirements, decision logs, previous
  tickets and relevant workflow documentation. Use indexes when available;
  search by actors, business outcome, constraint and failure mode.
- Run `scripts/requirements_discovery.py prepare` with the bounded request
  and source paths. Reuse its path-derived source IDs and exact digests; do not
  invent or renumber source IDs. Record original URL, date, section or ticket
  provenance inside any external source snapshot. Stdin is a fixed snapshot,
  not a claim of live access to the conversation.
- For past solutions, inspect the original decision and observed result if
  available. Separate "implemented", "proposed" and "outcome measured"; code
  alone does not prove customer benefit or business success.
- Record why each precedent transfers and where it differs: users, scale,
  business rules, incentives, operating context and constraints. Include failed
  or rejected approaches when supported by the evidence.
- External examples require checking primary/direct sources through available
  host tools. Verify current claims and distinguish sourced facts from inference.
  Never put private raw requirements into external searches.
- If history or browsing is unavailable, state what was searched and what is
  missing; offer general patterns as hypotheses, never as observed past success.
  Continue the options analysis and propose where to collect the missing evidence.

The context step uses stdout and makes no durable writes. Repeat preparation
with `--write` in the execute step only when persistence is in scope.

## Exit

Return a bounded source inventory, relevant precedents and explicit evidence limits.
