# Validate and Handoff — ai-sdlc-research: Sourced Delivery Evidence

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

`ai-sdlc-research/v1` contains topic, questions, sources, findings, source IDs,
confidence, limitations, trace targets, and owned open questions.

Quality gate:

- Pass when source IDs resolve, findings have confidence plus limitations, and
  delivery traces explain why the evidence matters.
- Full flow fails without two sources, two source types, or any open question owner.

## Examples

A valid finding cites `SRC-001/SRC-003`, states medium confidence, names data
freshness limitations, and traces to `DEC-022`. “Competitors all do this” is
invalid without registered sources, boundary, or confidence.

## Edge Cases

- A source may support and contradict different findings; keep both links.
- A blocked source remains registered only if its unavailability matters.
- Time-sensitive sources include an explicit access date and freshness limitation.
- Full flow source diversity counts distinct `type` values, not duplicate URLs.
- If internet access is unavailable for external scope, report a blocker and do
  not present cached model knowledge as completed research.

## Scope Boundary

- Do not fabricate sources, quotes, dates, or research participants.
- Do not turn findings into accepted decisions or requirements automatically.
- Do not provide legal or regulatory conclusions without qualified review.
- Do not hide conflicting or low-confidence evidence.
- Use `$ai-sdlc-change-impact` when accepted research changes downstream artifacts.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
