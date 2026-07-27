# Validate and Handoff — ai-sdlc-package-trust: Trusted Packages And Private Metrics

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Trust decisions report each control, evidence, reason, and fingerprint. Metrics
report only aggregate counts, statuses, retries, tokens, coverage, freshness,
and input fingerprints; they never include paths, source, prompts, commands, or diffs.

## Scope Boundary

- Do not install, execute, publish, sign, approve, or delete packages.
- Do not upload metrics or collect content-bearing fields.
- Do not weaken allowed origins, capabilities, or provenance policy.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
