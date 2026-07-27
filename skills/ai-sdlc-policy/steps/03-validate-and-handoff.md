# Validate and Handoff — ai-sdlc-policy: Explainable Delivery Controls

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Complete TOON/JSON resolution records contain normalized rules, provenance, source hashes,
protected rule IDs, and a deterministic fingerprint. Decision records contain
the exact action and context fingerprint, matched and waived rules, gates,
reasons, result, evaluation time, and policy fingerprint.

Quality gate:

- Pass when all layers are valid, protected rules remain at least as strict,
  each waiver is current and authorized, and the action result plus gates are
  understood.
- Fail closed on invalid policy, unknown action, protected weakening, malformed
  or expired waiver, and missing context required by a predicate.

## Examples

A high-assurance profile may add `security-review` and `fresh-evidence` gates to
`change.apply`. A project layer can add more gates. A user layer cannot remove
those gates or turn a protected `require` into `allow`.

## Edge Cases

- Non-matching rules remain visible in explain output only when requested.
- Multiple matching deny rules remain deny even if another rule allows.
- A valid waiver suppresses only its named waivable rule, never an entire action.
- Expiry is evaluated at explicit `--as-of` time for reproducible decisions.

## Scope Boundary

- Do not edit source policy, issue waivers, record approvals, or satisfy gates.
- Do not treat `allow` as authorization outside the evaluated action and context.
- Do not let user or project layers weaken protected organization minimums.
- Do not execute the evaluated action; return the decision to its owning workflow.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
