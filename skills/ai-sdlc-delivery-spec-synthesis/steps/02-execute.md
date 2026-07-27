# Execute — ai-sdlc-delivery-spec-synthesis: Delivery Spec Synthesis

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/delivery_spec_scaffold.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/spec-structures.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/delivery_spec_scaffold.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-delivery-spec-synthesis/scripts/delivery_spec_scaffold.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-delivery-spec-synthesis/scripts/delivery_spec_scaffold.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Convert the clarified package and story set into a structured delivery specification.

## Use When

- The gap review is complete.
- The story set is mature enough to serve as a reliable input.
- The team needs a delivery-oriented spec, not just narrative discovery.

## Do Not Use When

- Stories are still missing key actor behavior or acceptance logic.
- The team only needs a lightweight story list.

## Workflow

1. Start from the validated stories and upstream package.
2. Synthesize scope, roles, workflows, business rules, data needs, NFRs, and dependencies.
3. Keep assumptions and open questions explicit instead of smoothing them over.
4. Organize the document for delivery handoff rather than executive storytelling.

## Spec Rules

- Keep the spec consistent with the story set and MVP boundaries.
- Do not re-invent requirements that contradict the input package.
- Call out unresolved rules, missing owners, and dependency risks directly.
- Go deep enough for delivery planning, but do not drift into code design unless the business-level spec genuinely requires it.

## Structures

Use `references/spec-structures.md`.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
