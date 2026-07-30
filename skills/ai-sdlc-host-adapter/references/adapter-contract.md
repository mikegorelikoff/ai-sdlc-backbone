# Host Adapter Contract

An adapter manifest is a capability claim, not authority. Native mappings must
declare equivalent semantics for portable `step.analysis`, `step.context`,
`step.action`, `step.validation`, and `step.handoff` operations. A capability
request embeds one complete, context-ready StepCard; required capabilities,
side-effect controls, gates, evidence outputs, and idempotency scope are derived
from that card rather than restated by the caller.

Concurrency is clamped to the adapter limit. A request for unavailable
isolation produces an explicit sequential-isolation fallback and effective
concurrency one; it never guesses a host sandbox. A missing step operation or
required capability makes the result incompatible.

Fixtures describe conformance classes only and make no product-version claims.
