# Execute — ai-sdlc-qa-requirements-gap-review: QA Requirements Gap Review

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/qa_gap_scan.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/qa-gap-review-framework.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/qa_gap_scan.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-qa-requirements-gap-review/scripts/qa_gap_scan.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-qa-requirements-gap-review/scripts/qa_gap_scan.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Review the incoming delivery package and determine whether it is specific enough to support rigorous test design.

## Use When

- The team already has stories, specs, APIs, workflows, or equivalent artifacts.
- The next task is defining test scope, strategy, and detailed test cases.
- There is a risk that the package is good for product or delivery discussions but still weak for QA execution.

## Do Not Use When

- No meaningful requirements artifacts exist yet.
- The task is original product discovery rather than downstream QA design.

## Workflow

1. Inspect the available artifacts and identify what is present versus missing.
2. Check whether requirements are testable, specific, measurable, and role-aware.
3. Identify missing acceptance criteria, business rules, failure behavior, scope boundaries, permissions, dependencies, and data rules.
4. Ask only the clarifying questions needed, in small batches.
5. Do not move to strategy or test-case synthesis until the minimum QA bar is met.

## Review Rules

- Do not treat polished prose as proof of testability.
- Call out vague phrases like "it should work", "admin has access", or "system validates input" directly.
- Separate facts from assumptions and open questions.
- Flag what blocks QA execution versus what can be deferred.

## Framework

Use `references/qa-gap-review-framework.md`.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
