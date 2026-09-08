# Handoff — ai-sdlc-delivery-package-gap-review

> Executable checkpoint: handoff

## Entry

Enter after the selected procedure and validation have terminal evidence.
Use the current journal for Apply work; standalone read-only work returns its
result directly and does not create a run merely to record analysis.
Do not infer completion from a plan, partial output, or an earlier context
window.

## Procedure

Assemble an `ai-sdlc-handoff/v2` result from the owning step evidence. Name the
completed step IDs, produced artifacts or evidence, validation status,
unresolved blockers, residual risks, current owner, and the single next
required action. Optional follow-up must remain separate from required work.

Preserve graph, StepCard, context, and result fingerprints so another session
can resume without reconstructing history from prose. When execution is
blocked, include the failed gate, safe recovery action, retry limit, and owner.
Never broaden permissions, mark unexecuted checks as passed, or hide a
required decision inside a summary. Use the shared failure codes and bounded
repair rules; report a failed review as completed review work with blocked
downstream readiness.

## Exit

Return the evidence-backed handoff directly in the active response. The result
must make the next owner and action unambiguous and returns control to the
coordinator. Continue an explicitly requested cascade only after its next gate
passes; a standalone skill does not expand into a cascade.
