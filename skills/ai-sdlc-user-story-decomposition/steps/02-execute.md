# Execute — ai-sdlc-user-story-decomposition: User Story Decomposition

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/story_map.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/story-structures.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/story_map.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-user-story-decomposition/scripts/story_map.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-user-story-decomposition/scripts/story_map.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Turn a clarified delivery package into implementable, actor-based user stories with acceptance logic and scenario coverage.

## Use When

- The upstream package is clear enough to decompose.
- The user needs stories, acceptance criteria, and scenario coverage for delivery planning.

## Do Not Use When

- The input package still has blocking gaps.
- The task only needs a high-level product narrative rather than delivery artifacts.

## Workflow

1. Identify actors, goals, and outcomes.
2. Group related work into epics or capability areas when useful.
3. Write stories in actor-value form.
4. Add acceptance criteria and negative or edge scenarios where they materially affect delivery.
5. Capture dependencies, assumptions, open questions, and priority for each story cluster.

## Story Rules

- Every story must name a concrete actor.
- Every story must state the user or business outcome it supports.
- Do not accept stories that are only UI elements or technical tasks without user/business value.
- Add failure, edge, and exception scenarios where omission would create delivery risk.
- Keep priorities tied to MVP scope, not personal preference.

## Structures

Use `references/story-structures.md`.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
