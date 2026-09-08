---
artifact_metadata:
  schema: ai-sdlc-artifact-metadata/v1
  feature: 024-skill-execution-reinforcement
  artifact: validation.md
  path: specs/024-skill-execution-reinforcement/validation.md
  workspace: implementation
  skill: ai-sdlc-sdd
  flow_mode: quick
  state_file: specs/024-skill-execution-reinforcement/_ai_sdlc/state.toon
  decision_log: specs/024-skill-execution-reinforcement/decision-log.md
  status: review
  owner: implementation agent
  created_at: 2026-09-08
  updated_at: 2026-09-08
  trace_ids: [AC-001, AC-002, AC-003, AC-004, AC-005]
  related_artifacts: [requirements.md, design.md, test-cases.md, qa.md, tasks.md, reinforcement-report.md]
  validation: []
  metatags: [ai-sdlc, implementation, ai-sdlc-sdd, validation, review]
---

# Validation evidence

## Scope and trust

AC-001 through AC-005 and TC-001 through TC-005. These are observed local
command outcomes, not authenticated CI, reviewer approval or release signoff.
Original console logs are session-local; their SHA-256 digests below identify
exact output. Durable deterministic eval receipts are linked separately.

## Executed checks

| Check | Command | Observed outcome | Console SHA-256 |
| --- | --- | --- | --- |
| Harness shared and per-skill suites | Pinned Python 3.11: `python -m unittest discover -s skills/ai-sdlc-shared-runtime/tests -p test*.py -v` | 195 tests, exit 0 | `1852b74378de4be53be3557457b0dca64c6dec3420daec314e01828449cdaeed` |
| Loop suite | From products/ai-sdlc-loop: `python3 -m unittest discover -s tests -v` | 79 tests, exit 0 | `35ef1d47cd369a5f2222d9b3c98b5b39199cb161846f88bcf7ff9a6dddca1196` |
| Harness docs suite | `/opt/homebrew/bin/python3.11 -m unittest discover -s docs/tests -v` | 47 tests, exit 0 | `785617d7c89b31d7a25b7d2d5fe698fddd2503b84d0e49650e62b419a9825dcf` |
| Harness source docs | `/opt/homebrew/bin/python3.11 docs/scripts/validate_docs.py` | 208 pages, 48 skills, 6 modules; exit 0 | `8f2aad01671493e3b2966779a80c3a2842e054276798a20c47f9585780021aef` |
| Harness strict build | `mkdocs build --strict` | exit 0 | `e623e28f6b0a39858be1c73cca40679720066dd495611bb9e2ccca91317bc7c8` |
| Harness rendered docs | `/opt/homebrew/bin/python3.11 docs/scripts/validate_rendered.py site` | 209 HTML pages, 5612 targets; exit 0 | `085ef87d3f8f8b43188c38f98c783595607ced0bcd55d630cc5151d6ab19ec7d` |
| Loop strict build | From Loop: `mkdocs build --strict` | exit 0 | `2ae9d86c97e72ead79d3144b68ee87866d345125348a36891aea5877b002b5c2` |
| Compatibility | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_compatibility.py --skip-git-audit --format toon` | compatible, exit 0 | `007afed07f6c74e0c171fb26ac33ad7c63adea93b86f59f0ba877658346cdb3e` |
| Project install | `python3 skills/ai-sdlc-shared-runtime/tests/install_smoke.py --mode emulated` | exit 0 | `85d8fab75e865b5e824db21ef17ed7dca3228951a59145ed361eab3ebb866d0c` |
| Selective install | Same smoke helper: `--mode emulated-selective` | exit 0 | `b2369bb0edbf5d4ad6fb76acc1927a7769075dab18881fd39817cc81f910d6b1` |
| Disposable global install | Same smoke helper: `--mode emulated-global` | exit 0 | `0b5a3cbe1e2060380c3b129ea01239137cd9e469343487fce8fc8f8bb7bd5ec9` |
| Final Loop graph negatives | From Loop: `python3 -m unittest tests.test_skill_graphs -v` | 4 tests; all 21 graph evaluations and native entrypoints pass | `92100ccef2d1137119d018624b2c3f455402cdaace2d65b1a0d76387b08dce4e` |

Additional executed checks: both generated catalog `--check` commands;
Loop source documentation validation (23 pages); Loop rendered validation
(785 targets); Python compilation of both skill trees with
`PYTHONPYCACHEPREFIX=/tmp/reinforcement-pycache`; clarify, checklist, analyze,
validate and plan-link gates for this spec; whitespace diff checks in both repos.

## Deterministic receipts

- [Harness: 432/432](./_ai_sdlc/eval-receipt.toon), 48 skills, nine scenarios each.
- [Loop: 179/179](./_ai_sdlc/loop-eval-receipt.toon), 16 semantic graphs with nine
  scenarios each and five compact graphs with seven applicable scenarios each.
- Compact Loop traversal additionally checks every declared entrypoint, not
  only the longest dependency closure. Both graph-generation check CLIs pass.

Reproduce Harness evals with `python3
skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_skill_eval.py --mode deterministic
--skills-root skills`. From Loop use its sibling shared-runtime script with
the same flags. Repeated selections/run plans and terminal replays are checked
inside the matrix; source and shared-reference mutations have negative tests.

## Pinned full-suite environment

The successful full Harness suite used `uv run` with Python 3.11,
`--with-requirements requirements-docs.lock`, and the exact parser package
versions declared in `.github/workflows/skills-ci.yml`:

```text
tree-sitter==0.25.2
tree-sitter-typescript==0.23.2
tree-sitter-python==0.25.0
tree-sitter-javascript==0.25.0
tree-sitter-java==0.23.5
tree-sitter-c-sharp==0.23.5
tree-sitter-php==0.24.1
tree-sitter-bash==0.25.1
tree-sitter-cpp==0.23.4
tree-sitter-go==0.25.0
tree-sitter-rust==0.24.2
tree-sitter-kotlin==1.1.0
tree-sitter-swift==0.7.3
```

## Failures found and repaired

Before correction, negative tests reproduced two inconsistent-completion
acceptances, an unvalidated handoff graph, three stale/tampered Loop evidence
acceptances and five routing errors. They now pass.

Early broad runs used an unsuitable Python 3.9 for the installer or lacked
AST packages under Python 3.11. The final pinned-environment run resolved those
environment failures. The newly added discovery schema contract marker and
outdated documentation script count were corrected without reverting existing
user changes. Initial SDD clarify/checklist failures were corrected through the
canonical section writer with explicit decision disposition and observable
Given/When/must acceptance criteria. The default Python bytecode cache was
sandbox-protected; compilation succeeded with its cache confined to /tmp.

## Remaining checks and limitations

No known unresolved regression remains in the executed checks. No remote
installer, live provider evaluation, hosted multi-OS CI, commit or publication
was performed. The successful local runtime suite includes pinned parser tests
and installation fixtures, but does not replace the cross-platform release CI
matrix. All existing dirty work and active branches remain intact.
