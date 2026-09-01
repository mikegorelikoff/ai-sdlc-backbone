# Validate and Handoff — ai-sdlc-engineering-quality-gate

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced a post-fix context, complete findings,
verification evidence, and a draft decision.

## Procedure

## Output Spec

Validate and return one canonical `ai-sdlc-engineering-quality-gate/v1` TOON
report plus a concise YAML presentation and `ai-sdlc-handoff/v2`. The report is
the durable authority; presentation and handoff must agree with its readiness.

### Evidence gate

Validate all of the following before completion:

- The context and report parse as TOON, use supported schemas, contain only
  repository-relative paths, and bind to the current change fingerprint.
- The repository profile cites 2–5 representative examples where practical,
  or records an evidence-based shortfall, and every applicable pattern has
  repository evidence.
- Findings were captured before mutation, IDs are unique, ordering is
  canonical, severities are not inflated, and fixed versus remaining state is
  truthful.
- High findings and safe localized Medium findings were fixed when authorized;
  every unfixed material item states why it could not be resolved safely.
- Verification commands use argv, focused checks precede broader checks,
  post-fix results exist after fixes, and each status reflects an actual
  `pass`, `fail`, `not_run`, or `unavailable` outcome.
- Change-scope counts match the post-fix diff, new dependencies and public API
  changes are explicit, and unrelated modifications made by the gate are zero.
- `finalize` succeeded atomically and `verify --root . --report <path>` succeeds
  against the unchanged repository state.

### Decision rules

- `PASS`: `ready_for_next_stage: true`, no remaining finding, no verification
  gap, and every required available deterministic check passes.
- `PASS_WITH_FINDINGS`: `ready_for_next_stage: true`, no unresolved High or
  blocking Medium finding, every required available check passes, and only
  explicit non-blocking Low/Medium findings or optional/unavailable checks
  remain.
- `FAIL`: readiness is false because a High or blocking Medium remains, an
  available required check failed or was not run, required evidence is absent,
  the report is invalid/stale, or status and decision disagree.

Treat an applicable repository command that cannot execute because of the
environment as `not_run`, with a reason; do not relabel it `unavailable`.
`unavailable` means the repository exposes no applicable command or source for
that optional verification kind. A required `unavailable` check is blocking.
If verification fails, final status cannot be `PASS`.

### Human presentation

Keep the durable report in canonical TOON. Present a concise YAML projection in
the active response using, where practical:

```yaml
status: PASS | PASS_WITH_FINDINGS | FAIL
summary: evidence-based assessment
repository_profile:
  representative_examples: []
  applicable_rules: []
findings_fixed: []
remaining_findings: []
verification: []
change_scope:
  files_changed: 0
  lines_added: 0
  lines_removed: 0
  new_dependencies: []
  unrelated_changes: []
quality_evidence:
  repository_consistency: []
  correctness: []
  testing: []
  simplicity: []
final_decision:
  ready_for_next_stage: false
  blocking_reasons: []
```

Scores are optional. Never include a score without concrete evidence for that
dimension.

## Edge Cases

- If no credible comparison exists, state the bounded search and continue only
  with other repository evidence; do not invent a local convention.
- If there are no findings, retain explicit empty finding arrays and actual
  verification evidence.
- If authority is review-only, leave safe material fixes documented and set
  readiness according to their blocking state.
- If a command cannot run, preserve its exact status and reason. Never claim a
  stale, skipped, blocked, unavailable, or inferred result passed.
- If finalization or current-report verification fails, leave no partial output
  and report `FAIL` with the recovery action.

## Scope Boundary

- Do not treat this gate as product approval, security penetration testing,
  broad architecture redesign, release verification, staging, commit, or
  deployment.
- Do not overwrite unrelated tracked, staged, unstaged, or untracked work.
- Do not claim semantic correctness from helper validation alone; retain the
  repository evidence that supports the decision.

## Exit

Return the current report path and fingerprint, concise quality projection,
verification outcomes, residual risk, blockers, and unambiguous readiness.
