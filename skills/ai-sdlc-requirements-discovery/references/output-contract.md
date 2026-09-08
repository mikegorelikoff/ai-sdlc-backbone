# Discovery packet contract

Scale detail to the task. Keep stable IDs so replies can update the packet.

| Part | Required content |
| --- | --- |
| Problem brief | Raw request, current process, actors, outcome, constraints, proposed scope and candidate success measures |
| Sources | SRC ID, locator, relevant claim, authority/status, access/date limits |
| Observations | REQ/GAP ID, fact/assumption/contradiction/unknown/proposal, source IDs and affected workflow/rule |
| Precedents | PRE ID, source IDs, past decision, actual outcome or outcome unknown, applicability and differences |
| Business options | OPT ID, beneficiary/value, workflow/rules, evidence or hypothetical pattern, dependencies, risks, reversibility, cost assumptions, unknowns and tradeoffs |
| Elicitation | Q ID, gap/option IDs, stakeholder, exact question, purpose/decision consequence, priority, evidence location and method, response status |
| Recommendation | Conditional preferred option, selection criteria, disqualifying evidence, unresolved choices and accountable owner |
| Handoff | Packet completion, separate decision status, next action/owner and expected evidence |

Use descriptive priorities such as "before option selection", "before
implementation" and "later validation". State confidence in terms of evidence
and missing checks rather than an unexplained numeric score.

## Compact example

Illustrative inputs, not real historical evidence:

- SRC-1: current ticket asks to "reduce approval waiting time using bulk approval".
- SRC-2: a previous pilot record says "batch review was introduced, impact was
  not measured, and high-value cases retained individual approval".
- SRC-3: the current stakeholder note says "all cases need individual approval".

Separate reducing waiting time (need) from bulk approval (suggested solution).
Treat SRC-2/SRC-3 as a potentially different policy or context, not permission
to generalize the pilot. Viable proposals might be improving triage and
assignment without changing approval policy (OPT-1), or a limited low-risk
batch pilot subject to policy confirmation (OPT-2). Do not label either faster
without measurements.

| Question | Target / method and location | Links / decision consequence |
| --- | --- | --- |
| Which approvals must be individual, and what policy defines permitted exceptions? | Process/policy owner; inspect the current policy and compare it with the pilot record | GAP-1, OPT-1/OPT-2; before option selection; an absolute rule rules out batch approval |
| Where does waiting accumulate: assignment, reviewer availability, or the review itself? | Operations lead and analyst; inspect timestamps from a representative recent sample and observe one review session | GAP-2, OPT-1/OPT-2; before option selection; distinguishes routing problems from review effort |
| If a batch pilot is permitted, what makes a case eligible and how must exceptions be reviewed? | Process owner with QA; walk through anonymized ordinary and exception cases | GAP-3, OPT-2; before implementation; defines pilot scope and candidate acceptance cases |

If there is no SRC-2, say no verified precedent was found and propose locating
past pilot decisions or support tickets. Do not invent a previous project's
results. End with a conditional recommendation and the unresolved policy
decision; drafting these questions does not send them.
## Deterministic helper contract

`scripts/requirements_discovery.py` owns preparation, scaffolding, validation,
finalization and freshness checks. [The machine schema](discovery.schema.toon)
defines exact field types, enums and ID formats. Unknown fields fail rather than
being dropped. Use [the example context](example-context.toon) and
[example draft](example-draft.toon) to understand the schema; they are illustrative
fixtures, not evidence for a new feature.

The draft includes `evidence_limits` and an explicit `as_of` date. Source IDs
are generated from source kind and relative path. Observation, precedent,
option and question IDs are author-maintained stable references checked for
format and uniqueness. Canonical serialization sorts record collections by ID
and string sets lexically; describe ordered business workflows in prose.

Only `finalize` produces the complete report: product identity, feature,
flow mode, packet status, independent decision status, the full source
`context`, complete draft `analysis`, trust disclosure and fingerprint.
Hashes bind exact source content and detect local drift. They are not signatures,
proof of stakeholder identity or proof that a cited source supports a claim.

`prepare` accepts files or a fixed stdin request snapshot. `scaffold` writes
an intentionally incomplete template. `validate` checks types, source/option/
question links, material-gap and option coverage, and recorded acceptance.
`verify` repeats those checks against current file bytes and checks fingerprints;
Harness also checks the generated Markdown projection. A stdin snapshot can be
checked for internal integrity but cannot be checked against a live conversation.

No clock, network or model call participates in the helper. File sources are
limited to 64 KiB each, 16 sources and 256 KiB total; machine artifacts and
generated projections are limited to 2 MiB. Narrow oversized input explicitly;
nothing is silently truncated. Symlinks, escaping paths and self-referential
outputs are rejected. Reads/checks do not mutate; writes are explicit, atomic
per file, and the Harness output pair rolls back on process errors. Identical
writes are no-ops; different existing output requires reviewed `--replace`.

The compatibility flag `--state-check` only checks that an existing canonical
state file is readable and belongs to the same feature. It confers no readiness
or approval. `--begin-state` and `--complete-state` are rejected because this
optional assistant owns no lifecycle stage.
