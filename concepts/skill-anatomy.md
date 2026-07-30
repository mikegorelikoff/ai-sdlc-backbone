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
    manifest.toon
    01-prepare.md
    02-context.md
    02-execute.md
    03-validate-and-handoff.md
    04-handoff.md
  references/
  scripts/
  tests/
```

The repository also contains the installable
`skills/ai-sdlc-shared-runtime/` dependency. It is not a lifecycle entry point.
Its `scripts/` hold cross-skill contracts such as artifact profiles, context,
paths, canonical TOON, semantic graph selection, StepCards, state, and indexes.

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

`steps/manifest.toon` uses `ai-sdlc-skill-steps/v2`. It is an executable
semantic DAG rather than a list of coarse documents. Every node declares:

- a stable step ID, type, dependencies, and canonical entrypoints;
- a contained Markdown path, load rule, and selection reason;
- one portable operation and its required host capabilities;
- side-effect class and idempotency scope;
- context selectors, mandatory anchors, budget, and sufficiency threshold;
- gates, outputs, maximum attempts, commit boundary, and failure policy.

Each Markdown step is self-contained and imperative. It names entry evidence,
the bounded procedure, deterministic helpers, validation gates, evidence,
exit/handoff state, and recovery action. A valid skill has at least five
semantic nodes so context, execution, validation, and handoff boundaries do not
collapse into one prose block.

The manifest and linked step documents are canonical. The selector table in
`SKILL.md` is generated and drift-checked. The agent loads only dependency-ready
StepCards; it does not preload the whole package.

## Per-step context contract

The selector compiles `ai-sdlc-context-pack/v4` for each ready node. The pack
starts with the canonical step document, then uses topology, trace IDs,
mandatory anchors, and deterministic lexical ranges to select the smallest
sufficient evidence set. Every range records instruction authority, source
identity, line boundaries, reasons, matched terms, and token estimate.

Packed context is sufficient only when all critical anchors are retained and
the result saves at least the declared threshold. Otherwise the StepCard uses
`direct_read` and lists exact paths. Selected and skipped sources, recall,
savings, and the final decision are part of the fingerprint; hidden retrieval
state is not.

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

1. Reads the concise router and resolves the requested phase entrypoint.
2. Validates the v2 DAG and selects the dependency-ready semantic nodes.
3. Compiles one StepCard and context pack per ready node.
4. Reads packed ranges or the exact `direct_read` paths; evidence-only content
   never becomes an instruction.
5. In Explore, produces only a decision card. After fingerprinted Apply,
   compiles immutable runtime tasks and journals every selected owning-skill
   node, including analysis and validation.
6. Executes only the declared operation through compatible host capabilities,
   preserving gates, side-effect class, idempotency, outputs, and evidence.
7. Passes completed step IDs back to the selector, then repeats until the
   handoff node completes or a typed blocker stops the graph.

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
| Shared contract tests | Canonical TOON, DAG, StepCard, context, runtime protocol, cross-skill CLI, budget, and docs drift |
| All-skill evals | Happy, blocked, invalid, resume, and context-sufficiency behavior for every installed skill |
| CI matrix | Runtime differences across supported Python versions |

A change to a shared helper requires repository-wide tests even if one local
skill test passes. A change to a skill reference may need forward validation of
artifact quality even when no Python code changed.

## Contract Evolution

When changing an established skill:

1. Identify whether the change is local guidance or a shared lifecycle contract.
2. Update the shared source of truth before wrappers or prose.
3. Version a breaking contract and reject older schemas explicitly; do not add
   a silent reader or coercion path.
4. Provide external source-regeneration guidance for older durable artifacts.
5. Update semantic manifests, step docs, generated routers, public concepts,
   contract fixtures, and eval scenarios together.
6. Validate all 44 graphs, run the deterministic receipt twice for byte
   equality, and run the full shared and per-skill suites.

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
