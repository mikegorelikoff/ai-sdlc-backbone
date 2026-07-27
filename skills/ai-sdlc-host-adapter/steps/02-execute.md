# Execute — ai-sdlc-host-adapter: Portable Host Negotiation

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/adapter-contract.md` before adding a mapping or fallback.
- Validate manifests and requests with the JSON schemas in `references/`.
- Use `scripts/adapter.py` for validation and negotiation.
- Use `references/fixtures/` only as contract conformance hosts, not claims about products.

## Script Usage

```bash
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.json --validate
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.json --negotiate --request request.json --write
```

## Purpose

Keep workflow meaning portable while making host limitations and fallbacks explicit.

## Steps

1. Validate manifest identity, API range, unique capabilities, mappings, and limits.
2. Validate the exact capability request.
3. Prefer equivalent native mappings.
4. Use only registered deterministic fallbacks whose prerequisites are supported.
5. Reduce concurrency or isolation to sequential execution with exact reasons.
6. Fail incompatible when a required operation or capability has no safe mapping.
7. Emit a complete TOON-first negotiation without invoking host operations.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
