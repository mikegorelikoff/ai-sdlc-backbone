# Execute — ai-sdlc-working-backwards-discovery: Working Backwards Discovery

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/discovery_interview_plan.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/interview-framework.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/discovery_interview_plan.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-working-backwards-discovery/scripts/discovery_interview_plan.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-working-backwards-discovery/scripts/discovery_interview_plan.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Run the discovery interview that turns an initiative idea into a structured, business-grounded definition.

## Use When

- The user wants a PRFAQ but the initiative is still fuzzy.
- The user needs help clarifying customer pain, target audience, business goals, requirements, and risks.
- The user wants a critical product partner who will challenge vague statements.

## Do Not Use When

- The initiative already has a validated, clear requirements package and only needs final document drafting.
- The task is technical implementation planning without business discovery.

## Workflow

1. Start at Stage 1 initiative context.
2. Ask a maximum of 5 to 7 questions at a time.
3. After every answer, summarize facts, assumptions, contradictions, and open questions.
4. Challenge vague wording until it becomes measurable, observable, or testable.
5. Stay in the current stage until the clarity bar is met.
6. Do not hand off to synthesis until the discovery minimums are present.

## Interview Rules

- Ask for real examples and current workarounds.
- Separate facts from assumptions and hypotheses.
- Keep decisions made distinct from decisions still needed.
- Push back if the MVP becomes a disguised full roadmap.
- Capture risks, dependencies, and out-of-scope items as they appear.

## Framework

Use `references/interview-framework.md` for the staged question structure.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
