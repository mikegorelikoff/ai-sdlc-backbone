# Execute — ai-sdlc-shared-runtime: Portable Helper Dependency

> Selector: execute

## Entry

Enter only after the prepare step passes and this skill is the selected owner for the current lifecycle action.

## Procedure

## References

- `scripts/` is the canonical runtime source in repository and installed layouts.
- `references/` contains packaged configuration defaults and schema.
- `references/skill-steps.schema.json` defines the portable
  `ai-sdlc-skill-steps/v1` progressive-disclosure contract.
- Downstream scripts resolve only this sibling package; there is no mirror,
  synchronization step, or source-tree fallback.

## Script Usage

- Verify the canonical runtime in a harness source checkout:

  ```bash
  python3 -m unittest discover -s skills/ai-sdlc-shared-runtime/tests -p 'test*.py' -v
  ```

- Verify an installed downstream helper from a consumer repository:

  ```bash
  python3 .agents/skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py --help
  ```

- Validate all source or installed step manifests without loading their
  procedures:

  ```bash
  python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py \
    --validate-all --format toon
  ```

- Select one bounded procedure with `ai_sdlc_steps.py --skill <name>
  --phase <phase> [--role <canonical-role>] [--action <action>]`.
- A missing `ai-sdlc-shared-runtime/scripts/` directory, incomplete package, import
  traceback, or non-zero helper smoke result is a blocker.

## Purpose

Keep installed AI SDLC capabilities executable without assuming that the user
cloned the harness source repository. Skills CLI discovers folders containing
`SKILL.md`; this package makes the shared runtime part of that discovered
installation set.

## Inputs

- Resolve the current skill file and its sibling skills root.
- Locate `ai-sdlc-shared-runtime/scripts/` under that root.
- Select the smallest downstream helper that exercises the reported dependency.
- Preserve the consumer repository as the helper's working directory.

## Steps

1. Confirm the runtime package and the requested downstream skill share one
   installed skills root.
2. Run the downstream helper with `--help` before any mutating action.
3. For SDD installation verification, write and finalize only a disposable
   fixture specification in a temporary consumer repository.
4. Classify failures as missing package, incomplete runtime, Python incompatibility,
   invalid consumer root, or downstream contract failure.
5. Reinstall from the reviewed pinned source when package files are missing or
   inconsistent; do not patch installed files ad hoc.
6. Rerun the exact helper smoke command and return the owning workflow handoff.

## Exit

Stop after the bounded owning-skill action. Preserve evidence, decisions, and traceability needed by validation; do not silently start another skill.
