# Shared execution decisions

Read once at preflight for the selected skill. Its own required inputs, artifact
profile, semantic manifest and validator define the task-specific contract.
This reference supplies common decisions; it does not grant new authority.

## Resolve inputs

| Input class | Resolution |
| --- | --- |
| Required | Resolve the owning step's named inputs before dependent work. A review target or requested outcome cannot be invented. |
| Discoverable | Read the selected feature index, exact artifact/trace, Git diff, installed manifest or helper output before asking the user. Follow only references needed for the current decision. |
| Inherited | Reuse the user's goal, scope, authorization, selected flow mode and current source-bound artifacts. Revalidate hashes/state on resume; conversation alone cannot prove freshness or completion. |
| Optional | Preserve explicit choices. If absent, omit or label a reversible assumption; do not turn optional context into a prerequisite. |

Missing actors, business choices or acceptance outcomes are questions for their
owner when they affect the result. Missing repository facts are retrieval work.
Conflicting authoritative requirements block only dependent synthesis. Preserve
both sources and identify the decision; do not resolve by whichever was read last.

## Flow mode

`--full-flow` takes precedence when both flags are supplied. `--quick-flow`
permits recorded, reversible assumptions and focused checks. It does not waive
artifact validity, authorization, required evidence or material product decisions.
`--full-flow` requires the owning skill's upstream/downstream, traceability and
validation gates. Neither flag expands a single-stage request into a cascade.
Without a flag, use the owning helper's default; disclose that mode rather than
silently upgrading it. Reuse authorization already present in the session.

## Execute and verify

Resolve the declared entrypoint and its dependency closure. A completed-node
set must include every completed node's dependencies. A selector's `complete`
means only that its requested closure is exhausted, not that the feature passed.
After an Apply run, runtime journal evidence is required before marking work done.
Read-only standalone analysis returns evidence directly without creating a run.

Use the owning parser/scaffold/validator for deterministic work. Use judgment
for interpretation, alternatives and semantic coverage, with source references.
Do not load all steps, templates or repository files to decide one checkpoint.
Direct reading is an explicit strategy when packing loses mandatory evidence or
costs more than it saves. Never describe a context-pack fingerprint as approval.

Validate output separately from drafting: execute the owning validator, inspect
required fields and source/requirement coverage, then record actual results.
For changed behavior or executable logic, update regression checks; if automation
is infeasible, name the uncovered behavior, reason and manual evidence.
Planned, unavailable, skipped and failed checks are not passes.

## Failure and bounded repair

Return failures in the existing result/handoff, using `code`, `gate`, `evidence`,
`recommended_action`, `owner`, `attempts_used` and `attempt_limit`. Do not create
a second lifecycle state file for this record.

| Code / condition | Action |
| --- | --- |
| MISSING_INPUT | Retrieve a discoverable input; otherwise request the exact material fact and pause dependent work. |
| AMBIGUOUS_SCOPE | Preserve competing interpretations and request the material scope decision. |
| INVALID_INPUT / ARTIFACT_INVALID | Report the parser/validator error and exact source; repair only an owned, derivable field. |
| STALE_EVIDENCE | Refresh through the producer, rerun affected checks and invalidate downstream readiness. |
| REPOSITORY_ERROR / TOOL_FAILURE | Report command, exit and affected path; retry only after a changed condition and inside existing authority. |
| VERIFICATION_FAILURE | Classify the failing criterion, repair the bounded cause, then rerun affected gates. |
| UNSUPPORTED_CASE | Return the unmet capability and owning alternative; do not emulate unsupported guarantees. |

The manifest's `max_attempts` and `on_failure` govern runtime node retries.
Never reset attempts by creating another run. For synthesis outside a runtime
retry, allow at most two repair cycles for the same output and unchanged scope;
after that return the unresolved failure. A schema repair does not authorize
replaying an external/destructive action. Check durable effects before any retry.

## Complete and hand off

Complete only when the required outputs exist, applicable validators pass,
source fingerprints are current and no blocking finding remains. A valid
negative review is a completed review with a blocked downstream decision;
it is not a ready feature. Name artifacts, validation, blockers, residual risk,
owner and one next required action; keep optional actions separate.

The owning skill returns its handoff. A coordinator may continue only the
already requested lifecycle/cascade after consuming that evidence and checking
the next prerequisites. A standalone skill must not silently expand scope.
Respect separate commit/publication and product-specific approval gates.

## Registered Harness lifecycle stages

This section applies only when the owning preflight names a registered feature
stage. Resolve `skills/` to the installed sibling skill root before commands.
Use `state_machine.py check --feature <feature> --skill <skill> --workspace
<refinement|implementation>` with the active flow flag before durable work.
Use `begin` when work starts and `complete --artifacts <path>` only after the
artifact validator and required evidence pass. Keep the stage feature-scoped.

Full flow blocks on incomplete predecessors, active conflicting work or blockers.
A quick-flow predecessor skip requires a low-risk recorded `--assumption` or
`--decision-ref DEC-###`, also recorded in the feature decision log. Inspect
`state_machine.py status --feature <feature> --workspace <workspace> --format
toon` for the next stage. Utility skills do not acquire lifecycle authority.

## Harness Markdown artifact metadata

For canonical Harness artifacts, let the owning writer maintain the leading
`artifact_metadata` block with schema `ai-sdlc-artifact-metadata/v1`: `feature`,
`artifact`, `path`, `workspace`, `skill`, `flow_mode`, `state_file`, `decision_log`,
`status`, `owner`, `created_at`, `updated_at`, `trace_ids`, `related_artifacts`,
`validation`, `metatags`. Tags include `ai-sdlc`, workspace, skill, artifact type
and current status. Refresh metadata after changes to status, paths, source or
validation; assumptions stay visible in quick flow and blockers stay visible in
full flow. Metadata and indexes never replace source bodies, decisions or state.
