<!-- public-docs-canonical: ../docs/index.md -->

> **Internal, non-canonical design note.** The maintained public documentation starts at [AI SDLC Harness docs](../docs/index.md). This file is retained for repository history and maintainer context only.

# Skill Anatomy

Each skill is a self-contained instruction folder that an AI assistant reads to
decide when to act, what evidence to collect, which script to run, where to
write outputs, and how to preserve traceability.

A skill combines judgment and deterministic machinery. `SKILL.md` tells the
agent how to reason and when to use resources; scripts own contracts that should
not vary between agent sessions.

## Folder Shape

```text
skills/<skill-name>/
  SKILL.md
  steps/
    manifest.json
    01-prepare.md
    02-execute.md
    03-validate-and-handoff.md
  references/
  scripts/
  tests/
```

The repository also contains the installable
`skills/ai-sdlc-shared-runtime/` dependency. It is not a lifecycle entry point.
Its `scripts/` hold cross-skill contracts such as artifact profiles, context,
paths, migration, state, and indexes.

## `SKILL.md`

`SKILL.md` is the concise AI entry point. It contains:

- when to use the skill;
- the Skill Card;
- the step selector table;
- the progressive-disclosure contract.

Detailed operational rules belong in selected `steps/`, while domain examples,
checklists, and schemas belong in `references/`. A router stays below 120 lines
and never duplicates its step bodies.

### Frontmatter And Triggering

The frontmatter contains `name` and `description`. The description is the
trigger contract: it states what the skill does and the user situations in
which it should activate. Workflow detail belongs in the body because the body
is loaded only after triggering.

Names use lowercase kebab-case and match the folder. Changing a skill name is a
lifecycle migration because state, metadata, profiles, tests, and documentation
may reference it.

### Router Body

The body tells the agent which procedure to read and when. It requires prepare
before commands or writes, execute only for the selected action, and
validation/handoff before completion. A selector failure blocks work rather
than permitting a broad package read.

## `steps/`

`steps/manifest.json` uses `ai-sdlc-skill-steps/v1`. Every selector declares a
contained Markdown path, phases, canonical roles, optional actions, load rule,
token cap, and selection reason.

Each Markdown step is self-contained and imperative:

- `Entry` names prerequisites and evidence;
- `Procedure` contains the complete phase-specific contract;
- `Exit` defines the stop or handoff boundary.

Most skills use prepare, execute, and validate/handoff. A skill may use more
specific phases when they materially improve selection. The agent loads only a
matching step; it does not preload all procedures.

## `references/`

References hold deeper domain guidance:

- templates;
- checklists;
- review frameworks;
- examples;
- anti-patterns;
- quality bars.

The AI loads only the reference files needed for the current task.

A reference is authoritative guidance for content depth, not a generated
artifact template owned by runtime. When a skill says to read its reference
before writing, the agent must use its table columns, review dimensions, and
examples in addition to the compact scaffold.

## `scripts/`

Scripts handle deterministic work that would otherwise waste prompt tokens:

- compact artifact analysis;
- scaffold generation;
- validation gates;
- readiness checks;
- format checks;
- state and index maintenance.

Scripts must be useful for the specific skill, not generic filler.

Refinement profile wrappers intentionally stay thin. Their domain keywords and
prompts are local, while canonical output names, sections, predecessors, tables,
and budgets come from the shared profile registry. This prevents 18 wrappers
from evolving incompatible lifecycle contracts.

## AI Execution Behavior

When a task triggers a skill, the AI:

1. Reads the router and resolves the matching step manifest selector.
2. Loads the required prepare step and resolves the active flow mode.
3. Checks `specs-index.toon` and `state.toon` when feature context exists.
4. Loads the selected execute step and runs the skill script when deterministic scaffolding, compression, validation,
   or indexing is useful.
5. Reads only the references named by the selected procedure.
6. Sends each content-only section body to the script on stdin with `--section`.
7. Loads the validation/handoff step and runs `--finalize`; the script writes the routed artifact, metadata, decision
   log, state changes requested by flags, and specs index.

The AI does not create a temporary content Markdown file and does not directly
edit an artifact owned by a scaffold script.

## AI Production Behavior

A skill output is complete only when the AI has produced the visible answer and,
when file output is requested or implied, the durable supporting records:

- routed Markdown artifact;
- artifact metadata;
- decision-log updates;
- state updates when lifecycle progress changed;
- specs-index refresh;
- validation or residual-risk note.

The visible response and durable output are different channels. Progress,
validation, blockers, and final summaries belong in the agent response.
Canonical Markdown, decisions, state, plans, and indexes belong in their routed
files. A standalone `summary.txt` is not part of the contract unless the user
explicitly requests one.

## `tests/`

Every skill directory should include `tests/test_scripts.py`.

Tests verify that skill scripts:

- compile;
- expose `--help`;
- accept the expected flow flags;
- preserve the shared script contract;
- perform the skill-specific behavior they own.

Repository-wide runtime tests live under
`skills/ai-sdlc-shared-runtime/tests/`.

### Validation Layers

| Layer | What it catches |
| --- | --- |
| Skill quick validation | Invalid frontmatter, name, or required skill shape |
| Per-skill tests | Local script behavior and flags |
| Shared contract tests | Cross-skill CLI, routing, context, budget, and docs drift |
| Migration/E2E tests | Legacy conflicts and strict 18-stage package behavior |
| CI matrix | Runtime differences across supported Python versions |

A change to a shared helper requires repository-wide tests even if one local
skill test passes. A change to a skill reference may need forward validation of
artifact quality even when no Python code changed.

## Contract Evolution

When changing an established skill:

1. Identify whether the change is local guidance or a shared lifecycle contract.
2. Update the shared source of truth before wrappers or prose.
3. Preserve read compatibility when existing feature packages would otherwise
   break.
4. Add migration behavior for renamed durable files.
5. Update concept/skill documentation and contract tests together.
6. Validate every affected skill folder and run the full shared suite.

Do not fix contract drift by copying a new rule into every skill while leaving
the runtime unchanged.

## AI Failure Modes

The AI must not:

- treat `SKILL.md` as a generic essay and ignore script/reference instructions;
- broad-load every step instead of resolving the current selector;
- load all references by default;
- create artifacts outside the routing rules;
- skip tests for new or changed scripts;
- update a skill script without keeping the per-skill and shared tests aligned.
