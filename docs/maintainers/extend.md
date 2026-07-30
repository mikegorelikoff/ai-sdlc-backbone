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
- compatibility, source regeneration, deprecation, and rollback impact.

Use `ai-sdlc-sdd` for a medium or large change. Do not make a package because a
prompt is long; make it because a stable bounded capability needs portable
authority and validation.

## 2. Create or change a skill

A skill package uses:

```text
skills/ai-sdlc-<name>/
├── SKILL.md
├── steps/
│   ├── manifest.toon
│   ├── 01-prepare.md
│   ├── 02-context.md
│   ├── 02-execute.md
│   ├── 03-validate-and-handoff.md
│   └── 04-handoff.md
├── scripts/        # optional deterministic helpers
├── references/     # optional detailed contracts and schemas
└── tests/          # focused behavior and failure tests
```

`SKILL.md` is a concise router: frontmatter identity, a complete Skill Card, a
selector table linked to every declared step, and the progressive-disclosure
rules. Keep it below 120 lines. Put normative required inputs and routing in the
prepare node, context sufficiency in the context node, bounded work in action
nodes, proof in validation nodes, and ownership transfer in handoff nodes.

Every skill owns `steps/manifest.toon` with schema
`ai-sdlc-skill-steps/v2`. Each semantic node declares its contained Markdown
path, type, dependencies, entrypoints, role/action routing, load rule,
operation, capabilities, side-effect class, context selectors and mandatory
anchors, gates, outputs, attempts, commit boundary, idempotency, and failure
policy. Every skill has at least five meaningful nodes; flow owns six. Do not
copy detailed step content back into `SKILL.md`.

Validate a selector directly:

```bash
python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py \
  --root . --skills-root skills --skill ai-sdlc-<name> --phase execute \
  --role software-engineer --goal "bounded outcome" --format toon
```

The selector rejects missing manifests, unknown or cyclic dependencies,
unlinked/duplicate/escaping paths, symlinks, invalid operations, incomplete
context/gate/output contracts, unknown roles/phases, budget overflow, and
unmatched entrypoints. Its public guide is generated; never hand-edit
`docs/reference/skills/<skill>.md`.

Add an explicit selection boundary to `SKILL_SELECTION_BOUNDARIES`. Generation
must fail if the new skill lacks a concrete “use another capability instead”
case.

## 3. Add deterministic helpers

Use a helper for canonical TOON parsing, scaffolding, validation, indexing,
source regeneration, fingerprinting, routing, or reproducible reporting—not for hidden product
judgment.

Helpers should:

- have a module docstring and useful `--help`;
- validate types, schemas, paths, and mode conflicts;
- default to read/check/preview/emit behavior where practical;
- require explicit write/apply/execute modes for mutation;
- write atomically, fail closed, and return stable non-zero exits;
- avoid secrets and avoid network unless the owning contract requires it;
- emit complete canonical TOON for every structured machine result;
- use the shared codec instead of adding a local parser or serializer;
- emit Markdown only as a human review artifact;
- report exact outputs and recovery action;
- include positive, negative, and mutation tests.

If a helper imports shared code, resolve only the sibling
`ai-sdlc-shared-runtime/scripts` package and run the install smoke matrix.

## 4. Change shared runtime

Canonical shared source lives under
`skills/ai-sdlc-shared-runtime/scripts`. There is no second source or mirror.

!!! terminal "Run in terminal — source checkout"

    ```bash
    python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_test_suite.py --format toon
    python3 -m unittest discover -s skills/ai-sdlc-shared-runtime/tests -p 'test*.py' -v
    python3 skills/ai-sdlc-shared-runtime/tests/install_smoke.py --mode emulated
    python3 skills/ai-sdlc-shared-runtime/tests/install_smoke.py --mode emulated-selective
    python3 skills/ai-sdlc-shared-runtime/tests/install_smoke.py --mode emulated-global
    ```

Review runtime, consumer imports, install tests, and generated docs together.
The runtime suite also validates all step manifests, router budgets, and
instruction preservation.

## 5. Register a module

Create `modules/<id>/module.toon` using the versioned module schema. Declare a
stable ID, semantic version, kind, harness API range, dependencies,
description, and skill entries. Validation rejects duplicate IDs, missing
dependencies, incompatible API ranges, unknown skill paths, and traversal.

Optional modules must remain optional. Core navigation cannot acquire a hidden
dependency on a domain module.

## 6. Evolve schemas and representation

Prefer additive fields inside a compatible schema. A breaking change needs a
new version, compatibility decision, source-regeneration guidance, fixtures,
failure tests, and release notes. Runtime must reject an older schema rather
than carry a compatibility reader. Human delivery detail remains Markdown;
every structured machine artifact uses canonical TOON, including per-event
runtime journals.

Never add a lossy machine projection. Every field required for correct routing,
authority, or recovery must survive serialization.

For executable skills, treat `steps/manifest.toon` and referenced semantic step
documents as canonical. Each node needs a distinct condition, operation,
context contract, gates, outputs, side-effect class, retry policy, and recovery
boundary. Regenerate the concise `SKILL.md` router and fail drift checks instead
of hand-editing its selector table.

Every StepCard context contract must name mandatory anchors, relevant topology
or trace selectors, a token budget, and sufficiency rules. Tests must cover a
packed result, a missing-anchor direct read, low-savings direct read, exact
selected/skipped reasons, and byte-identical recompilation.

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
