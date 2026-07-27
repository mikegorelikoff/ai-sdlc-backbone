# Execute — ai-sdlc-test-case-and-suite-synthesis: Test Case And Suite Synthesis

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/suite_outline.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/test-case-structures.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/suite_outline.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-test-case-and-suite-synthesis/scripts/suite_outline.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-test-case-and-suite-synthesis/scripts/suite_outline.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Generate the detailed QA artifacts used for structured execution.

## Use When

- Requirements are clear enough to test.
- Scope and strategy decisions are already defined.
- The team needs detailed cases and explicit suite groupings.

## Do Not Use When

- Core expected behavior is still unclear.
- Strategy and risk priorities are not yet defined.

## Workflow

1. Create detailed cases only for relevant product surfaces.
2. Cover positive, negative, boundary, permission, workflow, and data conditions as applicable.
3. Add API, UI, integration, notification, state, security, privacy, and non-functional cases only where the system actually has those surfaces.
4. Produce separate smoke, regression, and UAT groupings.
5. Keep each case tied to a requirement, role, workflow, rule, or risk.

## Case Rules

- Steps must be explicit and executable.
- Expected results must be specific.
- Every case should be traceable to a requirement, workflow, role, or risk.
- Do not create generic cases that could apply to any system.
- Mark automation candidacy explicitly.

## Structures

Use `references/test-case-structures.md`.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
