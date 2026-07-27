# Execute — ai-sdlc-release-slicing-and-backlog-readiness-review: Release Slicing And Backlog Readiness Review

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/release_slice_plan.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/release-and-readiness-structures.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/release_slice_plan.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-release-slicing-and-backlog-readiness-review/scripts/release_slice_plan.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-release-slicing-and-backlog-readiness-review/scripts/release_slice_plan.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Run the final planning gate on the backlog package before estimation, roadmap slicing, or execution planning.

## Use When

- The backlog structure and cross-functional tasks already exist.
- The team needs prioritization, slicing, sequencing, and readiness guidance.

## Do Not Use When

- The backlog is still missing core epics, stories, or task linkage.
- The planning gap review or decomposition work is incomplete.

## Workflow

1. Review dependencies, risks, priorities, and scope boundaries.
2. Separate MVP, stretch, post-MVP, and out-of-scope work.
3. Create release slices, sequencing, milestones, and spike needs.
4. Assess estimation readiness, Definition of Ready, and Definition of Done.
5. Build traceability from business goals to backlog items and provide a JIRA-ready view.
6. Assign a final backlog readiness score and state what blocks planning.

## Review Rules

- Be strict.
- Push back if MVP is overloaded.
- Push back if priorities ignore business value, risk reduction, or dependencies.
- Flag items that are too large to estimate or too vague to schedule.
- Keep blockers, open questions, and launch risks explicit.

## Structures

Use `references/release-and-readiness-structures.md`.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
