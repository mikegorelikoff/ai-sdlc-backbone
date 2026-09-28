# Adaptive execution depth across the product family

Classify the requested delivery once with the sibling runtime's
`ai_sdlc_adaptive.py --request "<task>" --path <relevant-file>` and evidence-based
`--signal key=value` observations. This applies to every backbone and Loop skill;
a directly requested specialist still performs its own bounded job. FAST,
STANDARD and DEEP describe process depth, separately from quick/full interaction.
Full flow and protected repository policy can raise depth; uncertainty and new
risk can never lower it. Missing scope or confidence selects at least STANDARD.

| Depth | Required coordination | Evidence |
| --- | --- | --- |
| FAST | Context → implement → targeted verification | Request, classification reasons, relevant context, changed paths, executed checks, acceptance result |
| STANDARD | Context → compact plan → implement → affected tests and semantic verification | Same task record plus acceptance criteria, implementation decisions and test rationale |
| DEEP | Context → planning → readiness → SDD → implement → full risk strategy | Existing lifecycle artifacts, protected gates and applicable specialist evidence |

For a new adaptive delivery, do not invoke separate planning/readiness/full SDD
skills on FAST or STANDARD unless new risk warrants DEEP. Keep the compact plan
in the task record. A directly requested SDD package or an already governed
feature retains its owning artifact/state requirements; never mark an omitted
lifecycle stage complete. Existing mandatory approval and quality gates remain
in force in every mode. Loop's Specify is still its small scope receipt, not a
requirement to create a full Harness SDD package.

Reuse `context_pack` from the canonical adaptive task record. It contains task,
relevant file hashes and symbols, architecture, dependencies, constraints,
conventions, tests, change surface, assumptions and unresolved questions. Fill
semantic sections from evidence; empty sections are unknown, not assurances.
Use current StepCards or the existing context-cache graph for source excerpts.
Refresh changed/missing sources and add only needed paths. Do not rerun repository
discovery independently for planning, implementation and every review. On resume,
check source freshness; source hashes are evidence identity, not approval.

Record new risk immediately. Unexpected dependencies or failing assumptions raise
FAST to STANDARD; architecture, security, migration, material ambiguity or broad
scope raises depth to DEEP. Preserve completed work, context and retry counts;
perform only missing analysis, then reverify the affected changes. Scope expansion
still requires the owning scope/authorization check.

Prefer executed tests, compiler/type/lint/build/schema checks and diff inspection.
These are evidence, not proof of acceptance. Retain one semantic review of the
changed behavior. Activate doctor for installation/environment failures; bug
hunting for recurring unexplained defects; edge-case review for changed boundary
behavior; independent blind-case review for uncertain assumptions; specialized QA
for domain acceptance; hierarchical decomposition for DEEP uncertainty. These are
capabilities: use the available quality-lenses/review/QA owner, never invent a
missing skill. Assign each failure class once and reuse current evidence.

Only independent deterministic checks may run concurrently after implementation
settles. Shared caches, generated files, databases and tests that mutate the same
resources are dependencies. Do not overlap source mutation and final verification.
Keep existing scheduler/manifest concurrency and attempt limits.

Success requires the selected acceptance criteria, current required evidence and
no blocking findings. Allow initial verification plus at most two changed repair
attempts. Never retry/review the same unchanged source and check plan after a
failure; record changed environment evidence for a legitimate environment retry.
Stop on current passing evidence. Escalation does not reset budgets. Exhaustion,
conflicting material requirements or unavailable authority requires an explicit
blocked result and the exact missing input, not another agent review.

Record measured stage duration, invoked skills/checks, verification iterations,
escalations and outcome. Host model/tool calls and context tokens must be supplied
from actual host telemetry; unavailable values remain null. Token estimates are
labeled estimates. Distinguish source freshness reads from full rediscovery.
