---
artifact_metadata:
  schema: ai-sdlc-artifact-metadata/v1
  feature: 023-requirements-discovery
  artifact: validation.md
  path: specs/023-requirements-discovery/validation.md
  workspace: implementation
  skill: ai-sdlc-sdd
  flow_mode: quick
  state_file: specs/023-requirements-discovery/_ai_sdlc/state.toon
  decision_log: specs/023-requirements-discovery/decision-log.md
  status: validated
  owner: implementation agent
  created_at: 2026-09-07
  updated_at: 2026-09-07
  trace_ids: [AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010]
  related_artifacts: [specs/023-requirements-discovery/requirements.md, specs/023-requirements-discovery/test-cases.md, specs/023-requirements-discovery/tasks.md]
  validation: [deterministic-helper-tests-passed, native-all-profiles-passed, focused-checks-passed, docs-builds-passed]
  metatags: [ai-sdlc, implementation, ai-sdlc-sdd, validation, validated]
---

# Validation evidence

Executed locally on 2026-09-07. This is a change-focused execution log, not
independent model evaluation, stakeholder acceptance or release authorization.

DEC-002 records the user's correction: the provisional instruction-only package
now includes actual deterministic helpers, strict TOON schemas and portable
fixtures in both products. Commit and release remain paused after the user's stop.

## Automated checks

Commands run from the Harness root unless the product column says Loop, whose
working directory is `products/ai-sdlc-loop`.

| Product | Check | Observed result |
| --- | --- | --- |
| Harness | `python3 skills/ai-sdlc-requirements-discovery/tests/test_scripts.py -v` | 20 behavior tests passed |
| Loop | Skill-local helper tests, included by `tests/test_requirements_discovery.py` | 20 behavior tests passed within the complete 71-test suite |
| Both | Byte comparison of helpers, typed schemas, example context/draft and behavior tests | Identical shared contract; report identity and output paths remain product-local |
| Harness | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py --root . --skills-root skills --validate-all --format toon` | Valid: 48 skills, 241 nodes |
| Harness | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_skill_graph.py --skills-root skills --skill ai-sdlc-requirements-discovery --check --format toon` | New router matches canonical generation |
| Harness | `python3 -m unittest discover -s skills/ai-sdlc-shared-runtime/tests -p test_steps.py -v` | 19 passed, including discovery selection for BA and PM |
| Harness | `python3 -m unittest discover -s skills/ai-sdlc-shared-runtime/tests -p test_modules.py -v` | 6 passed, including core discovery registration |
| Harness | `python3.11 -m unittest discover -s skills/ai-sdlc-shared-runtime/tests -p test_native_install.py -v` | 23 passed, no skips |
| Harness | `python3.11 -m unittest discover -s skills/ai-sdlc-shared-runtime/tests -p test_install_record.py -v` | 8 passed |
| Harness | `python3.11 -m unittest discover -s skills/ai-sdlc-shared-runtime/tests -p test_compatibility.py -v` | 10 passed |
| Harness | `python3.11 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_compatibility.py --skip-git-audit --format toon` | Compatible; existing API 4.1.0 preserved, inventory extended to 48 |
| Harness | `python3.11 skills/ai-sdlc-shared-runtime/tests/install_smoke.py --mode emulated` | Installed runtime, complete SDD gates and commit-readiness fixture passed; 48 skill directories |
| Harness | `python3.11 skills/ai-sdlc-shared-runtime/tests/install_smoke.py --mode native --profile codex-project` | Installed discovery prepare/scaffold/validate/finalize/verify, runtime, SDD gates and commit-readiness fixture passed; 47 default directories |
| Harness | Same native smoke with `--profile claude-code-project`, and with `--profile agent-project --skills-root .agent/skills` | Both passed, including the complete installed discovery CLI workflow |
| Harness | Seven targeted `ScriptContractTests` in `test_all_skill_scripts.py`: CLI help/state flags; skill state/metadata/index/routing/runtime-path contracts | All 7 passed; the standard per-skill CI runner automatically discovers the new helper tests |
| Loop | `python3 -m unittest discover -s tests -v` | 71 passed, including actual installed helper prepare/scaffold and discovery selection in all three profiles, plus Doctor inventory |
| Both | `python3 docs/scripts/build_catalog.py --check` | Current source catalogs |
| Both | `python3 docs/scripts/validate_docs.py` | Harness 208 public pages; Loop 23 pages |
| Harness | `python3 -m unittest discover -s docs/tests -v` | 47 passed |
| Both | `mkdocs build --strict` | Both sites built |
| Both | `python3 docs/scripts/validate_rendered.py site` | Harness 209 HTML pages / 5612 local targets; Loop 785 internal targets |
| Both | Skill Creator `quick_validate.py` on each new package | Both valid |
| Harness | `check_clarify.py`, `check_checklist.py`, `plan_links.py --check`, `analyze_spec.py`, `validate_spec.py` for spec 023 in quick flow | All gates passed; all six implementation tasks complete |
| Both | `git diff --check` | Passed in both work trees |

The Python 3.11 runs prepend `/opt/homebrew/opt/python@3.11/libexec/bin` to
`PATH` so subprocesses also use a supported interpreter. The first native
installer suite run on the system Python 3.9 correctly hit the Python 3.10
minimum; the supported-interpreter rerun passed. Documentation token checking
downloaded the actual tokenizer table through an approved network retry; no
token estimate or skipped Learn gate was used.

The installer unit, compatibility and emulated-smoke rows retain the earlier
packaging-validation evidence. The new helper behavior, native smoke in all three
profiles, complete Loop suite and documentation checks ran after DEC-002.

## Deterministic behavior evidence

- Repeated runs, reordered source arguments and draft records, and relocated
  project roots produce identical bytes and fingerprints. Source IDs remain
  stable when the file content changes; the context fingerprint changes.
- Context captures exact bounded UTF-8 source content and hashes. Stdin is an
  explicit fixed snapshot, with no live-conversation freshness claim. Sources
  containing shell or HTML text are treated as data.
- Scaffold requires a canonical explicit date and leaves business fields
  incomplete. Finalization rejects that scaffold until the analyst fills the
  required facts, options, questions, evidence limitations and next actions.
- Twenty-three malformed draft mutations exercise schema/type errors, duplicate
  and dangling IDs, missing stakeholder/evidence fields, uncovered gaps/options,
  unsupported historical outcome claims and invalid decisions. They fail without
  writing a final report. Contradictions within one source document are supported.
- Acceptance needs a recorded owner, candidate, dated evidence and answered
  selection blockers. Local references and hashes do not authenticate a person
  or establish the truth of a business claim.
- Source changes, altered context/report data and modified Harness Markdown fail
  read-only verification. Full analysis and evidence survive canonical TOON and
  the escaped Markdown projection, including Cyrillic and multiline text.
- Writes are explicit and idempotent. Different existing content requires
  `--replace`; traversal, symlinks, invalid UTF-8 and oversized sources fail.
  Simulated partial replacement restores prior bytes and file modes.
- `--full-flow` takes precedence. Optional state checking verifies existing feature
  identity without writing state; begin/complete lifecycle transitions are rejected.

## Instruction walkthrough

TC-002/TC-003 were reviewed against both product-local procedures and the
illustrative bulk-approval example in each `references/output-contract.md`.
This is a static scenario walkthrough, not a fresh agent execution benchmark.

- The business need is reducing approval wait; bulk approval is a proposed
  mechanism. Triage/assignment improvement and a policy-dependent batch pilot
  change different business workflows.
- A prior pilot without outcome measurement cannot establish a speed benefit.
  A conflicting individual-approval policy remains a GAP requiring an owner.
- The policy-owner question determines whether batch approval is viable. The
  analyst's timestamp/sample audit distinguishes assignment delay from review
  effort. Pilot eligibility and exception questions become candidate acceptance
  criteria only after their rules are confirmed.
- With no verified history, the packet records the search limitation and labels
  alternatives hypothetical. With no stakeholder replies, it remains awaiting
  answers, even when the elicitation packet is complete. No message is sent and
  no implementation approval is created.

## Existing limitation and scope

The additional all-router generation check (`ai_sdlc_skill_graph.py
--skills-root skills --check --format toon`) reports a stale
`ai-sdlc-engineering-quality-gate` router. Reconstructing that router from
`git show HEAD:skills/ai-sdlc-engineering-quality-gate/SKILL.md` confirmed the
same discrepancy existed before this task. Its files were left unchanged.
The new Harness router passes its targeted generation check, and every Harness
manifest passes the selector validator. Loop uses its existing product-local
router convention.

Remote publication, live host/model evaluation, a full unrelated runtime suite
and stakeholder interviews were outside this bounded addition. Both work trees
remain uncommitted on task branches; Loop is a separate Git submodule and its
contents require a separate commit if publication is later requested.
