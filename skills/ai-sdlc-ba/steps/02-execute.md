# Execute — ai-sdlc-ba: Business Analysis

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/ba_context_scaffold.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/business-context-template.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/ba_context_scaffold.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-ba/scripts/ba_context_scaffold.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-ba/scripts/ba_context_scaffold.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Convert a vague AI SDLC feature, refactor, or workflow request into requirements-ready business context with actors, rules, assumptions, exclusions, and measurable acceptance criteria.

## Inputs

- Collect the user request and any explicit business goal, pain point, asset, provider, endpoint, role, or workflow name.
- Read the matching requirements document, delivery artifact, or `specs-refiniment/<feature-name>/<file.md>` package when one exists.
- Read `references/business-context-template.md` when the request needs a reusable intake structure.
- Collect current behavior from code or docs only when the desired business behavior depends on existing workflow semantics.

## Steps

1. State the business goal in one sentence.
2. State the problem in one sentence that names the current failure, missing capability, or decision gap.
3. List actors and systems that initiate, approve, observe, or are affected by the change.
4. Describe current behavior and desired behavior as separate bullets.
5. Extract business rules using deterministic language: `When X, the system must Y`.
6. List assumptions separately from confirmed facts.
7. List out-of-scope items so implementation does not expand silently.
8. Write acceptance criteria as observable pass/fail statements.
9. Write open questions only for decisions that materially affect scope, design, validation, or rollout.
10. Return requirements-ready BA notes and write them under `specs-refiniment/<feature-name>/<file.md>` when file output is requested.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
