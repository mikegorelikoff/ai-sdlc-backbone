# Coach

## Entry

Session events and workflow history context are loaded into memory and verified against data minimization schemas. All required sequence numbers and timestamps are verified for monotonicity.

## Procedure

1. Derive behavioral signals across historical workflows: calculate skill coverage, evaluate handoff discoverability, and construct the transition graph.
2. Identify friction motifs including rework cycles (e.g. repeated implement-verify-fix sequences), gate timing deviations, evidence lag, and decision churn.
3. Compute context switches and detect ignored recommendations or capability gaps across recent sessions.
4. Synthesize prioritized advisory suggestions or generate human-readable analytical markdown reports.

## Exit

A canonical usage report, signal derivation dictionary, or prioritized suggestions list is produced and ready for presentation or handoff.
