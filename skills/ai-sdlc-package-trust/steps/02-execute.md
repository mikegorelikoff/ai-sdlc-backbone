# Execute — ai-sdlc-package-trust: Trusted Packages And Private Metrics

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/trust-metrics-contract.md` before interpreting results.
- Validate manifests with `references/package.schema.toon`.
- Use `scripts/package_trust.py` for trust and `scripts/metrics.py` for aggregation.

## Script Usage

```bash
python3 skills/ai-sdlc-package-trust/scripts/package_trust.py . --package-root package --manifest package.toon --allowed-origin repository --allowed-capability filesystem.read --require-provenance --write
python3 skills/ai-sdlc-package-trust/scripts/metrics.py . --generate --write
```

## Steps

1. Validate manifest structure, safe inventory, origin, API range, and capabilities.
2. Rehash every declared regular file and the normalized inventory.
3. Validate required provenance fields without claiming cryptographic identity.
4. Emit an explainable allow or deny decision; never install the package.
5. Aggregate local run states and evidence coverage using counts and numeric budgets only.
6. Reject any metrics structure containing content-bearing field names.
7. Emit deterministic canonical TOON local metrics with explicit insufficient-data state.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
