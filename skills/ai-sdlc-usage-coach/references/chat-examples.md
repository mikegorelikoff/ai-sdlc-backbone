# Chat examples

Simulated source facts; output-format PASS never authorizes a downstream action.

## happy

| Status | Decision | Evidence |
| --- | --- | --- |
| PASS | Observed workflow patterns and derived 1 recommendation | session-journal:3 |

| Suggestion ID | Pattern | Evidence | Suggestion | Value rationale |
| --- | --- | --- | --- | --- |
| SUG-001 | Rework Cycle | 3 sessions | Run quality checks in smaller increments | Reduces verification cycles |

| Signal | Meaning | Impact | Action |
| --- | --- | --- | --- |
| rework-cycle | Repeated implement -> gate -> implement | 3 extra cycles | Run engineering-quality-gate earlier |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Developer | Run localized quality checks | Passing gate receipt |

## warning

| Status | Decision | Evidence |
| --- | --- | --- |
| WARNING | Evidence lag detected between implementation and verification | session-journal:2 |

| Suggestion ID | Pattern | Evidence | Suggestion | Value rationale |
| --- | --- | --- | --- | --- |
| SUG-002 | Evidence Lag | 4 steps lag | Run verify immediately after editing | Catches errors earlier |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Developer | Run verify command | Passing verification evidence |

## blocked

| Status | Decision | Evidence |
| --- | --- | --- |
| BLOCKED | Session journals are missing or unreadable | .ai-sdlc-loop/usage/sessions:empty |

| Command | Status | Blocker | Evidence | Required action |
| --- | --- | --- | --- | --- |
| report | BLOCKED | No sessions found | .ai-sdlc-loop/usage/sessions:empty | Execute at least one Loop skill |

| Owner | Next action | Expected evidence |
| --- | --- | --- |
| Developer | Run any Loop command | Active session journal |
