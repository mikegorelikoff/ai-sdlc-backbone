# Prepare — Requirements Discovery

## Entry

Start with a raw request about one feature or task; a finished PRD is unnecessary.

## Procedure

### 0.1 Required Inputs

- Raw request, notes, feedback or a source locator. Ask for the actual request if
  none is available; do not invent it from the skill invocation alone.
- Identify product, actors, desired outcome and constraints from available
  context. Missing details are discovery questions, not automatic blockers.
- Establish the permitted sources and whether the user wants a saved packet.
  Choose a feature slug for deterministic artifact identity.
- Use `prepare --request <path>` for a UTF-8 input file, or
  `prepare --request-stdin` for verbatim pasted input. External evidence is an
  explicit local snapshot; helpers never fetch links or execute source content.

### 0.2 Clarification Rules

- Resolve discoverable facts and reuse inherited decisions before asking.
- Missing optional context stays optional; label assumptions explicitly.
- Pause only work dependent on a missing material input or conflicting requirement.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full takes precedence. Apply the shared execution contract below.


### 0.3 Output Rules

- Return completion and next steps directly in the active agent response.
- Do not create `summary.txt` or another standalone summary file unless requested.
- Follow `references/output-contract.md`; identify what is confirmed, inferred,
  disputed, missing and proposed. Mark readiness separately from packet completion.
- Return useful findings even when history, stakeholder names or replies are
  unavailable. Use roles as proposed contacts when names are unknown.

### 0.4 Artifact Routing

- The helper emits TOON to stdout by default. `--write` enables canonical
  feature output when durable work is in scope; `--replace` is required to
  change an existing differing output after reviewing it.
- `prepare` and `scaffold` write
  `specs-refiniment/<feature>/_ai_sdlc/requirements-discovery-context.toon`
  and `requirements-discovery-draft.toon`.
- `finalize` owns `_ai_sdlc/requirements-discovery.toon` and its human projection,
  `specs-refiniment/<feature>/requirements-discovery.md`. Never hand-edit the
  final files or place discovery in `specs/`.
- Keep owner decisions in the typed draft with source evidence. If an existing
  feature decision log is updated, link it without converting a proposal to acceptance.

## 0.4.1 Runtime Path Resolution

- In the source checkout, resolve helpers under `skills/`.
- In consumer projects, use `.agents/skills/` for Codex, `.claude/skills/`
  for Claude Code, or the configured root in `.ai-sdlc/harness-install.toon`
  for `agent-project`. Resolve this skill and `ai-sdlc-shared-runtime` as siblings
  under that same root; no source-checkout or other-product dependency is needed.
- Treat `scripts/requirements_discovery.py` as relative to this installed skill.

## 0.5 Feature State Machine

- Read existing `_ai_sdlc/state.toon` when present. This optional advisory skill
  adds no lifecycle stage; do not invoke begin/complete for it or change another
  skill's state. A completed packet is not refinement or implementation readiness.

## 0.6 Artifact Metadata And Metatags

- The helper generates Markdown starting with `artifact_metadata` using
  `ai-sdlc-artifact-metadata/v1`: feature, artifact, path, workspace
  (`refinement`), skill, flow_mode, state_file, decision_log, status, owner,
  created_at, updated_at, trace_ids, related_artifacts, validation and metatags.
- The draft's explicit `as_of` date determines metadata dates; no wall clock
  participates in context, report or Markdown generation.
- The generated projection uses this skill's name and tags `ai-sdlc`, `refinement`,
  `requirements-discovery`, plus the actual status. Do not imply stakeholder
  acceptance through a `validated` or `approved` packet status.

## 0.7 Specs Index

- Before broad feature searches, use an existing
  `specs-refiniment/_ai_sdlc/specs-index.toon` or
  `specs/_ai_sdlc/specs-index.toon` to select related evidence.
- After a durable refinement write, run the installed shared runtime's
  `ai_sdlc_specs_index.py --workspace refinement --quick-flow`
  (or `--full-flow` for that mode) and verify the feature's `index.md`.

## Execution contract

Do not repeat discovery when the business direction is accepted and only actors, rules or acceptance logic need detail. Use `ai-sdlc-ba` instead. Do not use a discovery packet as implementation approval or a readiness verdict. Use the appropriate requirements review and `ai-sdlc-sdd` instead.

Read the [shared execution decisions](../../ai-sdlc-shared-runtime/references/execution-contract.md) once for this invocation.
Apply its required/discoverable/inherited/optional input rules to this step's
declared inputs. Record the source and status of material facts, then validate
the owning output contract and current evidence before completion.

## Exit

The raw request, evidence boundary, mode, output route and missing inputs are explicit.
