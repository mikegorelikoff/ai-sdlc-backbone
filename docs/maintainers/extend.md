---
title: Extend skills and modules
description: Add or change skills, helpers, references, schemas, modules, catalogs, and compatibility without creating hidden runtime or documentation contracts.
---

# Extend skills and modules

Extend the smallest authority surface that owns the behavior. A skill owns one
bounded agent workflow. A module registers a coherent capability group. Shared
runtime owns reusable deterministic mechanics. Public docs translate these
contracts but do not replace them.

## 1. Define the contract

Before files, state:

- user and problem;
- use and non-use situations;
- required inputs and source authority;
- accountable and supporting roles;
- allowed reads/writes and protected actions;
- quick/full behavior;
- artifact paths, schemas, state/index effects, and handoff;
- deterministic helper need, failure semantics, and recovery;
- compatibility, migration, deprecation, and rollback impact.

Use `ai-sdlc-sdd` for a medium or large change. Do not make a package because a
prompt is long; make it because a stable bounded capability needs portable
authority and validation.

## 2. Create or change a skill

A skill package uses:

```text
skills/ai-sdlc-<name>/
├── SKILL.md
├── steps/
│   ├── manifest.json
│   ├── 01-prepare.md
│   ├── 02-execute.md
│   └── 03-validate-and-handoff.md
├── scripts/        # optional deterministic helpers
├── references/     # optional detailed contracts and schemas
└── tests/          # focused behavior and failure tests
```

`SKILL.md` is a concise router: frontmatter identity, a complete Skill Card, a
selector table linked to every declared step, and the progressive-disclosure
rules. Keep it below 120 lines. Put normative required inputs, clarification,
flow flags, routing, state, and metadata rules in the required prepare step;
put task execution and helper usage in the execute step; put success gates,
edge cases, scope, validation, and handoff in the completion step.

Every skill owns `steps/manifest.json` with schema
`ai-sdlc-skill-steps/v1`. Each selector declares its contained Markdown path,
phases, canonical roles, optional actions, load rule, token cap, and reason.
Use additional domain-specific steps when three phases are insufficient; flow,
for example, owns six distinct phases. Do not copy detailed step content back
into `SKILL.md`.

Validate a selector directly:

```bash
python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py \
  --skill ai-sdlc-<name> --phase execute \
  --role software-engineer --format toon
```

The selector rejects missing manifests, unlinked or duplicate paths, traversal,
symlinks, unknown roles/phases, token overflow, and unmatched selectors. Its
public guide is generated; never hand-edit
`docs/reference/skills/<skill>.md`.

Add an explicit selection boundary to `SKILL_SELECTION_BOUNDARIES`. Generation
must fail if the new skill lacks a concrete “use another capability instead”
case.

## 3. Add deterministic helpers

Use a helper for parsing, scaffolding, validation, indexing, migration,
fingerprinting, routing, or reproducible reporting—not for hidden product
judgment.

Helpers should:

- have a module docstring and useful `--help`;
- validate types, schemas, paths, and mode conflicts;
- default to read/check/preview/emit behavior where practical;
- require explicit write/apply/execute modes for mutation;
- write atomically, fail closed, and return stable non-zero exits;
- avoid secrets and avoid network unless the owning contract requires it;
- emit complete TOON for agent control-plane state;
- keep JSON at schema/interoperability/recovery boundaries;
- report exact outputs and recovery action;
- include positive, negative, and mutation tests.

If a helper imports shared code, resolve only the sibling
`ai-sdlc-shared-runtime/scripts` package and run the install smoke matrix.

## 4. Change shared runtime

Canonical shared source lives under
`skills/ai-sdlc-shared-runtime/scripts`. There is no second source or mirror.

!!! terminal "Run in terminal — source checkout"

    ```bash
    python3 -m unittest discover -s skills/ai-sdlc-shared-runtime/tests -p 'test*.py' -v
    python3 skills/ai-sdlc-shared-runtime/tests/install_smoke.py --mode emulated
    python3 skills/ai-sdlc-shared-runtime/tests/install_smoke.py --mode emulated-selective
    python3 skills/ai-sdlc-shared-runtime/tests/install_smoke.py --mode emulated-global
    ```

Review runtime, consumer imports, install tests, and generated docs together.
The runtime suite also validates all step manifests, router budgets, and
instruction preservation.

## 5. Register a module

Create `modules/<id>/module.json` using the versioned module schema. Declare a
stable ID, semantic version, kind, harness API range, dependencies,
description, and skill entries. Validation rejects duplicate IDs, missing
dependencies, incompatible API ranges, unknown skill paths, and traversal.

Optional modules must remain optional. Core navigation cannot acquire a hidden
dependency on a domain module.

## 6. Evolve schemas and representation

Prefer additive fields inside a compatible schema. A breaking change needs a
new version, migration, compatibility decision, fixtures, failure tests, and
release notes. Human delivery detail remains Markdown; complete agent state and
indexes are TOON-first. JSON is valid for JSON Schema, external
interoperability, exact recovery, and JSONL journals.

Never add a lossy machine projection. Every field required for correct routing,
authority, or recovery must survive serialization.

## 7. Regenerate and validate discovery

!!! terminal "Run in terminal — source checkout"

    ```bash
    python3 docs/scripts/build_catalog.py
    python3 docs/scripts/build_catalog.py --check
    python3 -m unittest docs.tests.test_docs
    python3 docs/scripts/validate_docs.py
    ```

The generator must close the complete skill, module, and script inventories.
Review guide semantics, not only counts. Update MkDocs navigation when adding a
hand-authored public page.

## 8. Compatibility and deprecation

Run compatibility against the accepted baseline. Preserve stable skill names,
flow flags, artifact routes, handoff shape, configuration, module ranges, and
task-to-commit rules unless an approved major change says otherwise.

Deprecation needs:

- replacement and migration path;
- first deprecated release and planned removal boundary;
- warnings in source, docs, compatibility, and release notes;
- fixtures for old and new forms;
- rollback and support statement;
- explicit owner and decision record.

Deleting a capability without inventory, migration, compatibility, and docs
updates is not a deprecation process.
