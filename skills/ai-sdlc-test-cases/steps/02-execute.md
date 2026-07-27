# Execute — ai-sdlc-test-cases: Test Cases For Implementation

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/case_matrix.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/test-case-template.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/case_matrix.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-test-cases/scripts/case_matrix.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-test-cases/scripts/case_matrix.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Derive executable AI SDLC test scenarios from requirements or delivery context. Link each scenario to a requirement, story, workflow, risk, or acceptance criterion and define verifiable outcomes, automation commands, execution order, and human decisions without leaving open TODOs.

## Inputs

- Read the provided requirements, delivery spec, stories, workflows, risks, and existing test cases.
- Read existing QA notes from `specs-refiniment/<feature-name>/<file.md>` when acceptance or manual validation already exists.
- Collect the changed behavior, contract, bug, regression risk, endpoint, provider, asset, or workflow under test.
- Collect existing test files for the affected package when implementing tests.
- Read `references/test-case-template.md` when the scenario matrix needs reusable wording.
- Collect known fixtures, mocks, seeded data, and unavailable dependencies.

## Steps

1. Write `In scope` and `Out of scope` before generating scenarios.
2. Check every proposed test case against `Out of scope`; delete any test case that tests excluded behavior.
3. Define the behavior under test in one sentence.
4. Identify the requirement, story, workflow, risk, or acceptance criterion each scenario proves.
5. Create scenario IDs using `TC-001`, `TC-002`, and continuing sequence.
6. Include happy path, boundary values, null or missing inputs, negative validation, authorization, state-transition, retry, idempotency, concurrency, and provider-failure cases when relevant.
7. Map each scenario to exactly one primary layer: unit, service, transport, integration, QA/manual, or not automated.
8. Write a verifiable outcome for every scenario using one of these forms:
   - shell command whose exit code proves the outcome
   - numbered checklist of observable facts a human can tick without interpretation
   - before/after diff or data pair that proves the behavior changed correctly
9. Write an automation path for every scenario using one of these forms:
   - script path plus exact invocation
   - CI step name
   - `Manual — automate by YYYY-MM-DD — blocker: concrete blocker`
10. Replace open TODOs with `Decisions required`; each decision must include Question, Options A/B/C, Recommended default, Owner, and Blocking yes/no.
11. Replace decorative layer descriptions with `Execution order`; each layer must include run condition, what it blocks, and failure action.
12. Write or update the scenario matrix under `specs-refiniment/<feature-name>/<file.md>` when file output is requested.
13. Implement tests only after the scenario matrix contains requirement refs, verifiable outcomes, automation paths, execution order, and structured decisions.
14. Name tests so a reviewer can trace each test back to a scenario ID or spec reference.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
