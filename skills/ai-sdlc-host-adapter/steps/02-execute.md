# Execute — ai-sdlc-host-adapter: Portable Host Negotiation

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/adapter-contract.md` before adding a mapping or fallback.
- Validate manifests and requests with the TOON schemas in `references/`.
- Validate emitted results with
  `references/capability-negotiation.schema.toon`.
- Use `scripts/adapter.py` for validation and negotiation.
- Read `references/effect-driver-contract.md` before effect execution.
- Use `scripts/effect_driver.py` only after a compatible negotiation exists.
- Use `references/fixtures/` only as contract conformance hosts, not claims about products.

## Script Usage

```bash
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.toon --validate
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.toon --negotiate --request request.toon --write
python3 skills/ai-sdlc-host-adapter/scripts/effect_driver.py . --negotiation _ai_sdlc/adapters/host/negotiation.toon --request effect-request.toon
```

## Purpose

Keep workflow meaning portable while making host limitations and fallbacks explicit.

## Steps

1. Validate manifest identity, API range, unique capabilities, mappings, and limits.
2. Validate the embedded context-ready StepCard and request limits.
3. Derive `step.<type>`, required capabilities, side-effect capability,
   evidence, gates, and idempotency from the StepCard.
4. Select only an equivalent native mapping.
5. Clamp concurrency and make unavailable isolation an explicit sequential
   fallback.
6. Fail incompatible when the operation or a required capability is missing.
7. Emit one canonical TOON negotiation before invoking host operations.
8. For execution, bind the request to the negotiation, StepCard and context
   fingerprints, exact native operation, capabilities, approval, and arguments.
9. Execute only `workspace.write-text` or `external.toon-post`; never execute a
   generic command or shell string.
10. Atomically persist one receipt per idempotency key and return that receipt
    unchanged on an identical replay.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
