# Prepare — ai-sdlc-engineering-quality-gate

> Selector: prepare, clarify, or route

## Entry

Confirm the requested change, exact review target, repository root, authority,
flow mode, artifact routes, and verification constraints before reading broadly
or changing code.

## Procedure

### 0.1 Required Inputs

- A concise requested change or an accepted specification.
- A Git repository and current implementation diff, or an explicit base
  revision that resolves inside it. `context` defaults the base to `HEAD`.
- Repository instructions and any requirements, design, tasks, tests, or
  acceptance evidence that define the expected behavior.
- The write boundary for fixes and the host authority needed to edit files and
  execute repository commands.

Block when the request or review target is missing. Do not manufacture a diff,
acceptance criterion, permission, comparison, or verification result. If the
working tree includes unrelated changes, inventory them and preserve their
bytes, index state, and ownership.

### 0.2 Clarification Rules

- Ask only when the request, review target, acceptance boundary, fix authority,
  or required verification cannot be recovered from repository evidence.
- Keep confirmed facts, assumptions, and blockers distinct. Product ambiguity
  becomes a remaining finding; it is not permission to guess.
- A missing optional comparison is not a blocker when the bounded search and
  shortfall reason are explicit.

### 0.2.1 Flow Mode Flags

- Support mutually exclusive `--quick-flow` and `--full-flow` modes; reject an
  invocation that supplies both.
- Quick flow uses the smallest relevant diff, the highest-ranked local
  comparisons, focused checks, and visible reversible assumptions. Ask only
  when continuing could cause material correctness, security, data-loss,
  compatibility, or authority risk.
- Full flow verifies every available trace artifact, inspects all applicable
  review dimensions, and runs the justified repository gates required for
  delivery confidence. Stop on material ambiguity rather than guessing.
- Both modes require findings before mutation, the same severity/fix policy,
  current post-fix evidence, and the same readiness invariants.

### 0.3 Output Rules

- Return context/report paths and fingerprints, finding counts, exact command
  statuses, readiness, blockers, and next action directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v2` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone prose
  summary. Durable machine evidence is canonical TOON; the concise YAML final
  projection is presentation only.

### 0.3.1 Authority And Scope

- Treat the skill as independently callable after any implementation step; do
  not require a particular language, framework, or earlier AI SDLC skill.
- A direct request to run this full gate, or an enclosing authorized
  implementation workflow, authorizes safe localized corrections within the
  already declared changed/allowed paths unless the user narrows the run to
  review-only. A generic review request alone authorizes inspection and belongs
  with `$ai-sdlc-code-review`; it does not authorize mutation or broader paths.
- When `--feature` is used in an AI SDLC Loop workspace, require the current
  specification and matching Implement approval that the helper validates.
  The feature flag does not broaden its allowed paths.
- Do not commit, stage, deploy, contact external services, install dependencies,
  weaken configuration, or request broader permissions as a side effect.

### 0.4 Artifact Routing

- Resolve `skills/` as a logical skill root and verify that this skill and
  `ai-sdlc-shared-runtime` exist in the chosen source or installed layout.
- Use repository-relative, contained `.toon` paths for durable context, draft,
  and report artifacts. Use an owning feature `_ai_sdlc` directory when one is
  already canonical; otherwise make the output path explicit.
- Reject absolute output paths, parent traversal, symlink escape, and
  non-TOON durable machine output. Never persist secrets, raw unbounded command
  output, timestamps, durations, or absolute temporary paths in signed data.
- Durable schemas are `ai-sdlc-engineering-quality-gate-context/v1`,
  `ai-sdlc-engineering-quality-gate-draft/v1`, and
  `ai-sdlc-engineering-quality-gate/v1`.

### 0.4.1 Runtime Path Resolution

- In a Harness source checkout use `skills/`; in a project-scoped consumer
  installation resolve `.agents/skills/`, `.claude/skills/`, or the custom root
  recorded by the installer. Block with the missing path when the selected root
  does not contain both this skill and `ai-sdlc-shared-runtime`.

## 0.5 Feature State Machine

- The gate does not advance lifecycle state by itself. Read an existing
  feature `_ai_sdlc/state.toon` to confirm the implementation stage and owner.
- Do not create a state file merely for standalone invocation. In AI SDLC Loop,
  `--feature` validates the current specification and Implement approval and
  writes only the requested quality artifacts; it does not imply approval.
- Route lifecycle completion through the owning workflow after this report is
  current and ready.

## 0.6 Artifact Metadata And Metatags

- This skill creates TOON by default, so `artifact_metadata` Markdown
  frontmatter is not added to the canonical context or report.
- If the user explicitly requests a durable Markdown companion, use the shared
  `artifact_metadata` contract and include `metatags` for `ai-sdlc`,
  `implementation`, `engineering-quality-gate`, and current status. The
  Markdown remains a projection; it cannot replace the TOON report.

## 0.7 Specs Index

- Before broad feature reads, inspect `specs/_ai_sdlc/specs-index.toon` for
  implementation work and the feature-local `index.md` for human traceability.
- Refresh an owning workspace index only when repository policy registers the
  quality report there. Never use `specs-index.toon` or `index.md` as a
  substitute for the selected requirement, source, test, or report evidence.

### Adjacent Capability Boundary

- Use `$ai-sdlc-code-review` for a read-only findings review that must not fix
  code or make a delivery decision.
- Use `$ai-sdlc-validation` when command selection and execution evidence are
  the only requested outcome.
- Use `$ai-sdlc-security-testing` when exploitability, abuse cases, or security
  boundaries are the primary scope. This gate still records evidence-backed
  security and reliability findings relevant to the changed behavior.

## Exit

Proceed only when request, target, authority, output containment, unrelated
work, and verification constraints are explicit. Otherwise return a precise
blocker without mutation.
