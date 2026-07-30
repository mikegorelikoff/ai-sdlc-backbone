# Handoff — ai-sdlc-delivery-graph

> Executable checkpoint: handoff

## Entry

Enter only after the selected procedure and validation nodes have terminal
evidence in the current Apply run. Read-only work still needs a recorded result.
Do not infer completion from a plan, partial output, or an earlier context
window.

## Procedure

Assemble an `ai-sdlc-handoff/v2` result from the owning step journal. Name the
completed step IDs, produced artifacts or evidence, validation status,
unresolved blockers, residual risks, current owner, and the single next
required action. Optional follow-up must remain separate from required work.

Preserve graph, StepCard, context, and result fingerprints so another session
can resume without reconstructing history from prose. When execution is
blocked, include the failed gate, safe recovery action, retry limit, and owner.
Never activate another skill, broaden permissions, mark unexecuted checks as
passed, or hide a required decision inside a summary.

## Exit

Return the evidence-backed handoff directly in the active response. The result
must make the next owner and action unambiguous and must not perform that next
skill automatically.
