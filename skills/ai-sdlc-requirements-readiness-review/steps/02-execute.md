# Execute — ai-sdlc-requirements-readiness-review: Requirements Readiness Review

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/requirements_readiness_score.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/readiness-checklist.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/requirements_readiness_score.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-requirements-readiness-review/scripts/requirements_readiness_score.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-requirements-readiness-review/scripts/requirements_readiness_score.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Run the final gate on a PRFAQ package and business requirements document before they are treated as ready for alignment or handoff.

## Use When

- Discovery and synthesis are complete enough to review as a package.
- The user needs an explicit judgment about quality, risk, and remaining gaps.

## Do Not Use When

- Core discovery is still missing.
- The PRFAQ or BRD has not been created yet.

## Workflow

1. Review the package against the quality checklist.
2. Flag unclear customer value, weak business case, oversized MVP, or non-testable requirements directly.
3. Identify contradictions, missing dependencies, and unresolved questions.
4. Assign a readiness score from 1 to 10.
5. Explain what is strong, what is weak, what must be clarified next, and what should happen before design or development.

## Review Rules

- Be strict.
- Do not let assumptions pass as facts.
- Do not allow feature lists without customer pain or business value.
- Do not allow PRFAQ finalization if target customer, problem, alternative, value proposition, business objective, MVP, success metrics, risks, or dependencies remain too unclear.

## Checklist

Use `references/readiness-checklist.md`.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
