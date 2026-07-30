# Declarative Workflow Contract

Workflow definitions are immutable planner inputs. Every node names one
installed skill, canonical phase entrypoint, optional role/action routing
evidence, dependencies, bounded condition, and optional approval owner.
Conditions are data comparisons, not expressions or code.

An unapproved node with an approval owner is blocked. Eligible nodes compile
their canonical skill subplans; node IDs prefix task IDs, and dependency-node
terminal tasks become downstream dependencies. Waves are deterministic views
bounded by requested concurrency. The emitted run plan remains sequentially
safe and executable only when every node is eligible or explicitly skipped.

`workflow-plan.toon` records decisions, waves, approvals, derived capabilities,
side effects, fingerprints, and the embedded run plan. `run-plan.toon` is the
runtime input. Markdown is a human projection only.
