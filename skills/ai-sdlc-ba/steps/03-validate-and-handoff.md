# Validate and Handoff — ai-sdlc-ba: Business Analysis

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

Use this format for visible BA output or requirements-ready notes:

```text
Business context:
- Goal: one sentence.
- Problem: one sentence.
- Actors: actor list.
- Current behavior: concrete observed behavior.
- Desired behavior: concrete target behavior.

Rules and constraints:
- Rule: When condition, the system must outcome.
- Constraint: limit, dependency, policy, or compatibility requirement.
- Assumption: unverified statement that must be validated or accepted.
- Out of scope: explicit exclusion.

Acceptance criteria:
- AC-001: Given setup, when action, then observable result.

Open questions:
- Question: decision needed, why it matters, owner if known.
```

Quality gate:

- Pass when BA, PM, QA, and Dev stakeholders can use the output without guessing actors, expected outcomes, exclusions, or acceptance criteria.
- Fail when the output contains vague goals such as "make it better", acceptance criteria without observable results, or assumptions mixed into facts.

## Examples

Before:

```text
Add better BitGo wallet support.
```

After:

```text
Business context:
- Goal: Let operations view BitGo enterprise wallet details before initiating transfers.
- Problem: Operators cannot verify wallet scope and enterprise linkage from the current setup screen.
- Actors: operations user, BitGo integration, AI SDLC API.
- Current behavior: The UI shows configured provider status without wallet-level enterprise details.
- Desired behavior: The UI shows enterprise-linked wallet details required for transfer readiness review.

Acceptance criteria:
- AC-001: Given an organization with BitGo configured, when an operations user opens custodian setup, then the response includes enterprise ID, wallet IDs, and display labels.
```

Invalid counter-example:

```text
Acceptance criteria:
- Works correctly.
```

Reject this because it has no actor, trigger, or observable result.

## Edge Cases

- Stop before implementation when acceptance criteria would require inventing product policy.
- Mark unknowns as assumptions or open questions; do not hide them inside requirements.
- Use `TODO(dm): exact question` in specs when a delivery-manager decision is required.
- Keep BA output out of solution architecture unless a business rule constrains design.
- Use `$ai-sdlc-sdd` after BA to update requirements, design, test cases, QA, and tasks.

## Scope Boundary

- Do not design APIs, schemas, data models, or package boundaries; use `$ai-sdlc-sdd` and architecture guidance for design.
- Do not write implementation tasks except when translating accepted BA output into requirements context.
- Do not claim assumptions are confirmed without evidence from the user, artifact, `specs-refiniment/<feature-name>/<file.md>`, code, or docs.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
