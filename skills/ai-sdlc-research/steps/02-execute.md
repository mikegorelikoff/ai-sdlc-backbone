# Execute — ai-sdlc-research: Sourced Delivery Evidence

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Read `references/research-contract.md` for source and finding requirements.
- Read `references/web-research-protocol.md` before external or current research.
- Use `scripts/research.py` to validate citations and route canonical outputs.

## Script Usage

```bash
python3 skills/ai-sdlc-research/scripts/research.py specs-refiniment/payments --input /tmp/research.toon --emit --quick-flow
python3 skills/ai-sdlc-research/scripts/research.py specs/payments --input /tmp/research.toon --write --full-flow --format toon
```

## Purpose

Add disciplined evidence gathering when delivery uncertainty warrants it without
forcing research ceremony or internet access into every core workflow.

## Inputs

- Frame answerable questions connected to delivery traces.
- Register source title, locator, type, access date, credibility, and notes.
- Cite source IDs from each synthesized finding.
- Record confidence, limitations, and unresolved owner/action pairs.

## Steps

1. Define the decision to inform, research questions, and `internal`, `external`,
   or `mixed` evidence boundary.
2. For external or current questions, search the internet with the available
   web/browser tool, open direct result pages, compare publication and event
   dates, and prioritize primary or official sources.
3. Gather internal evidence when applicable and keep it distinguishable from web sources.
4. Register source identity, direct locator, access date, freshness, type, and credibility.
5. Synthesize findings separately from quotations and assumptions.
6. Record confidence, limitations, conflicts, and open questions.
7. Finalize routed Markdown and TOON outputs.
8. Route accepted implications through owning decisions and artifacts.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
