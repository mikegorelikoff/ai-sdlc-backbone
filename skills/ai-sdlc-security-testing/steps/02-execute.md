# Execute — ai-sdlc-security-testing: Security Testing

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- Use `scripts/security_review_matrix.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/owasp-backend-checklist.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- Run `scripts/security_review_matrix.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-security-testing/scripts/security_review_matrix.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-security-testing/scripts/security_review_matrix.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Review AI SDLC diffs, endpoints, workflows, provider integrations, and configs for concrete security findings, abuse paths, trust-boundary failures, and missing security validation. When the output makes OWASP- or standards-based claims, verify them against current primary sources before presenting them as authoritative guidance.

## Inputs

- Collect the exact review target: diff, commit, branch, endpoint, workflow, subsystem, or file set.
- Run or read `git status --short` and `git diff --stat` for diff-based reviews.
- Read relevant spec files for medium or large work.
- Identify entry points, identity sources, roles, organizations, accounts, providers, assets, secrets, and state transitions.
- Read `references/owasp-backend-checklist.md` when the surface is broad or the user asks for OWASP-style coverage.
- When the request mentions OWASP, ASVS, API Top 10, or other standards-driven guidance, browse current primary sources before citing categories, versions, or remediation guidance.

## Steps

1. Define the protected asset and trust boundary.
2. Map externally controlled inputs, identity sources, and privileged operations.
3. Check authentication before business side effects.
4. Check authorization across organization, account, role, provider, and workflow boundaries.
5. Check input validation, normalization, decimal handling, output encoding, query construction, and command construction.
6. Check secret handling, logs, errors, test fixtures, docs, config defaults, and webhook material for leakage.
7. Check replay, idempotency, race windows, retry behavior, broken state transitions, and failure isolation.
8. If the output will map issues to OWASP or another security standard, verify the current standard text from primary sources first. Prefer official OWASP pages, ASVS, API Security Top 10, or equivalent authoritative documentation.
9. Separate local exploitability evidence from standards-backed interpretation. Do not present remembered OWASP categories or stale version assumptions as verified guidance.
10. Check whether `test-cases.md`, `qa.md`, automated tests, or validation commands cover the risky paths.
11. Report concrete findings first, ordered by severity.
12. Report no findings explicitly when none are found, then list validation gaps, blocked verification, or residual risk.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
