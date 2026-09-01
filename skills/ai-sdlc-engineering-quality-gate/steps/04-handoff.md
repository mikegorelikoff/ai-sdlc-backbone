# Handoff — ai-sdlc-engineering-quality-gate

> Executable checkpoint: handoff

## Entry

Enter only after the selected procedure and validation nodes have terminal
evidence in the current Apply run. Do not infer completion from a draft,
pre-fix check, prior context window, or unverified report.

## Procedure

Assemble an `ai-sdlc-handoff/v2` result from the owning step journal. Name the
completed step IDs, canonical context and report paths, context/report
fingerprints, fixed and remaining finding counts, exact verification status,
change scope, residual risks, current owner, and the single next required
action. Keep optional follow-up separate from required work.

Set the next required action to verification/delivery only when the canonical
report is current and `ready_for_next_stage` is true. On `FAIL`, name the failed
invariant, contained recovery action, retry boundary, and owner. Preserve graph,
StepCard, context, and result fingerprints so another session can resume
without reconstructing evidence from prose.

Never activate another skill, broaden permissions, mark an unexecuted check as
passed, conceal an unresolved blocking finding, stage or commit changes, or
hide a required product decision inside the summary.

## Exit

Return the evidence-backed quality report and handoff directly in the active
response. The report must make readiness, blockers, next owner, and next action
unambiguous without performing that next stage.
