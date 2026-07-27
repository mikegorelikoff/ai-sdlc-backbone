# Execute — ai-sdlc-prfaq-package-synthesis: PRFAQ Package Synthesis

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/prfaq_outline.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/prfaq-package-structures.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/prfaq_outline.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-prfaq-package-synthesis/scripts/prfaq_outline.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-prfaq-package-synthesis/scripts/prfaq_outline.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Convert validated discovery notes into a decision-ready PRFAQ package and business requirements document.

## Use When

- Discovery minimums are met: target customer, problem, alternative, value proposition, business objective, MVP, success metrics, risks, and dependencies are materially captured.
- The user needs a PRFAQ, FAQ package, and BRD from clarified discovery inputs.
- The initiative is ready for narrative synthesis, not more interviewing.

## Do Not Use When

- Core discovery is still missing or contradictions remain unresolved.
- The user only needs a lightweight summary rather than a full PRFAQ package.
- The task is delivery decomposition or backlog planning rather than product definition.

## Workflow

1. Start from validated discovery notes and separate facts, assumptions, decisions made, and open questions.
2. Draft the press release in customer-facing language tied to the value proposition and MVP.
3. Build the FAQ package to address stakeholder, customer, business, operational, and launch questions.
4. Produce the BRD with business goals, scope boundaries, scenarios, requirements, and acceptance logic.
5. Keep unresolved items explicit instead of smoothing them into confident language.
6. Hand off to `ai-sdlc-requirements-readiness-review` when the package is complete.

## Synthesis Rules

- Do not invent customer pain, metrics, or business case details missing from discovery.
- Keep MVP boundaries consistent across the press release, FAQ, and BRD.
- Tie requirements to business value, actor intent, and observable outcomes.
- Mark assumptions and open questions clearly wherever certainty is still limited.
- Use testable acceptance logic rather than generic feature labels.

## Structures

Use `references/prfaq-package-structures.md` for document sections and output shape.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
