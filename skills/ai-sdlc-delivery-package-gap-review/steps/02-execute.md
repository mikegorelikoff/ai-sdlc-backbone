# Execute — ai-sdlc-delivery-package-gap-review: Delivery Package Gap Review

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/delivery_gap_scan.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/gap-review-framework.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/delivery_gap_scan.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-delivery-package-gap-review/scripts/delivery_gap_scan.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-delivery-package-gap-review/scripts/delivery_gap_scan.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Review an upstream discovery package and decide whether it is specific enough to decompose into delivery artifacts.

## Use When

- The user already has a PRFAQ, BRD, discovery notes, or similar package.
- The next task is user stories, acceptance criteria, or a delivery specification.
- There is a risk that the input package is strong narratively but still weak operationally.

## Do Not Use When

- No meaningful discovery package exists yet.
- The task is to do original customer/problem discovery rather than downstream delivery clarification.

## Workflow

1. Inspect the input package and identify what is present versus missing.
2. Separate facts from assumptions and open questions.
3. Identify missing delivery-critical detail such as business rules, role behavior, failure paths, dependencies, and scope boundaries.
4. Ask only the clarifying questions needed, in small batches.
5. Do not move to story decomposition until the minimum delivery bar is met.

## Review Rules

- Do not assume a polished PRFAQ equals delivery readiness.
- Call out contradictions between customer narrative, MVP, metrics, and proposed scope.
- Flag missing ownership, unresolved dependencies, and ambiguous workflows directly.
- Capture what can remain open versus what blocks decomposition.

## Framework

Use `references/gap-review-framework.md`.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
