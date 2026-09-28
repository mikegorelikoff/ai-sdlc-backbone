---
title: Flow flags
description: Stable execution-mode flags and their precedence rules across AI SDLC skills and helper scripts.
---

| Flag | Contract |
| --- | --- |
| `--quick-flow` | Make evidence-backed assumptions for low-risk gaps, run focused checks, and keep assumptions visible. |
| `--full-flow` | Stop on missing material decisions or predecessors and run stricter end-to-end gates. |
| Both flags | Full flow takes precedence. |
| Neither flag | Use the skill’s least-risky default or an explainable adaptive policy when supported. |

## Common output modes

Human-facing commands may return Markdown. Deterministic control-plane helpers
default to complete `--format toon` output for token-efficient agent
consumption. Machine output must preserve every logical field as well as the
same result, blocker, and trace meaning as the human view.

## Precedence

Explicit full flow cannot be downgraded by automatic classification. An
organization minimum is effective only when supplied to the rigor helper or
required by an enforced policy decision; presentation configuration does not
set it. Unknown risk inputs cannot reduce rigor.

## Adaptive execution depth

Process depth follows change risk and uncertainty. FAST covers local, understood,
reversible work; STANDARD adds a compact implementation plan; DEEP retains full
planning/readiness/SDD and applicable specialist review. The existing quick/full
flags still control interaction and owning-stage rigor. Full flow and protected
policy can raise execution depth. A directly requested stage retains its contract.

Classify an observed change surface without writing state:

```bash
python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_adaptive.py \
  --request "Fix a tiny bug" --path src/parser.py \
  --signal familiar=true --signal covered=true --signal confident=true
```

Without known scope/confidence the default is STANDARD. Architecture, security,
migration, irreversible production behavior, material ambiguity or broad changes
require DEEP. Risk observations can raise the mode during work without resetting
context, completed work or attempt history. Prompt length is not a classifier.

For an authorized adaptive delivery, persist one task evidence record with
`--task-file specs/<feature>/_ai_sdlc/task.toon --write`, add relevant source paths
with `--context-file`, and add compact decisions with `--plan-step`. Required
legacy lifecycle artifacts remain authoritative when that lifecycle is selected.
An adaptive task record cannot approve work or mark a registered stage complete.

Every backbone skill shares the context and execution contract. Use the existing
StepCard/context-cache mechanisms for excerpts, not repeated broad discovery.
Context records distinguish file freshness reads from repeated discovery, retain
constraints and questions, and expand incrementally. A separate read-only routing
decision gets a fresh source cache; Apply still revalidates fingerprints.

Loop also records this evidence in its existing `state.toon` under `execution`.
Its `specify` command automatically classifies; `--mode` sets a minimum and
`--signal` supplies observations. `adapt` records plans/context/escalation;
`next` selects missing work. Specify, implementation authority, the Engineering
Quality Gate, current verification and separate commit approval remain enforced.

Verification uses targeted deterministic checks and one acceptance review.
Doctor, quality lenses and specialized QA activate for their relevant failure
class. Loop permits concurrent checks only with `verify --jobs N --independent`
and still rejects source drift. Three attempts permit initial verification and
two changed repairs; unchanged failures stop, and unchanged successes reuse
current evidence. Explicit changed-environment evidence can justify a retry.

Run metrics include elapsed stages, selected depth, invoked skills/checks,
verification iterations, escalations and outcome. Host model/tool/token counters
are null unless reported; token estimates are labeled. These helpers do not call
models themselves, so helper benchmarks cannot establish end-to-end model speed.
