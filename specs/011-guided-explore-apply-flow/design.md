---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "design.md"
  path: "specs/011-guided-explore-apply-flow/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/011-guided-explore-apply-flow/_ai_sdlc/state.toon"
  decision_log: "specs/011-guided-explore-apply-flow/decision-log.md"
  status: "approved"
  owner: "Repository Maintainers"
  created_at: "2026-07-26"
  updated_at: "2026-07-26"
  trace_ids: []
  related_artifacts:
    - "specs/011-guided-explore-apply-flow/branch-plan.md"
    - "specs/011-guided-explore-apply-flow/decision-log.md"
    - "specs/011-guided-explore-apply-flow/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "approved"
---

# Design

## Overview
Add a new `ai-sdlc-flow` skill as the recommended human entrypoint over existing owning skills. Its pure core produces a DecisionCard from repository evidence; a separate Apply adapter verifies the card and dispatches one allow-listed action. Navigator becomes an intent/state evidence provider rather than the public mental model. Shared primitives remain canonical in `skills/_shared/` and are mirrored into `ai-sdlc-shared-runtime` through compatibility checks.

## Architecture
Four layers preserve authority boundaries. (1) Evidence readers load Git identity, indexes, state, project context, policy, config, and hashes without writes. (2) Pure decision core classifies intent before feature, resolves canonical workspace, selects rigor/roles/context strategy, and builds the card. (3) Fingerprint service serializes stable semantic fields with sorted keys and SHA-256. (4) Apply adapter reloads evidence, compares the fingerprint, maps the approved checkpoint to one exact owning-skill command, invokes it, and returns its result. The adapter never accepts output-root arguments and never chains checkpoints.

## Components
- `skills/ai-sdlc-flow/SKILL.md`, `references/flow-contract.md`, `scripts/flow.py`, and `tests/test_flow.py` own the meta-skill surface.
- `skills/ai-sdlc-navigator/scripts/navigate.py` exposes intent-first selection and reusable classification without recency-first fallback.
- `skills/_shared/ai_sdlc_flow.py` owns DecisionCard, canonical serialization, fingerprints, adaptive role/rigor rules, context selection, and action descriptions; the installed mirror lives under `skills/ai-sdlc-shared-runtime/scripts/`.
- `skills/_shared/ai_sdlc_paths.py` remains the canonical root/symlink/escape guard and receives only reusable validation additions.
- `skills/_shared/ai_sdlc_context_benchmark.py` exposes critical-anchor recall and net reread economics used by the flow.
- `ai-sdlc-code-review` integrates a two-phase spec-first evidence ordering contract without changing review authority.
- Module inventories, managed-skill lists, docs catalogs, onboarding, compatibility, and install smoke register the new skill.

## Interfaces and Contracts
`flow.py explore --intent TEXT [--feature FEATURE] [--quick-flow|--full-flow] [--format markdown|toon]` is read-only. `flow.py apply --card CARD_OR_STDIN [--format ...]` accepts a previously emitted card/fingerprint but no root or arbitrary command. DecisionCard schema `ai-sdlc-flow/v1` fields: schema, mode, repo_id, intent_class, intent_reason, feature, workspace, stage, skill, rigor, rigor_reason, roles[], role_evidence[], project_context, sources[], context_economics, blockers[], planned_writes[], next_checkpoint, fingerprint. ApplyResult fields: status, fingerprint, action, artifact/evidence, next_required, diagnostics. The skill is an internal package interface, not a globally installed public CLI.

## Data Model
DecisionCard uses immutable dataclasses/typed dictionaries and normalized POSIX repository-relative paths. SourceEvidence contains path, SHA-256, freshness, and critical anchors. ContextEconomics contains raw_tokens, packed_tokens, reread_tokens, net_tokens, savings_tokens, savings_percent, critical_total, critical_retained, recall_percent, and selected_strategy. RoleEvidence contains role, source signal, and reason. FingerprintPayload excludes presentation order, timestamps, and diagnostic prose but includes every semantic route and evidence field named by FR-003. ActionSpec binds one stage/skill to an exact command template and expected artifact.

## Error Handling
Return structured blockers before action selection for ambiguous intent, absent explicit feature when required, stale or unreadable state/index, conflicting active features, stale project context, invalid workspace topology, root escape, symlink root, divergent canonical/legacy roots, unsafe rigor downgrade, anchor loss, insufficient savings, unsupported action, malformed card, and fingerprint drift. Explore still renders a card with blockers and zero planned writes. Apply returns non-zero, performs no mutation, and names the changed fingerprint inputs without echoing sensitive content.

## Security Considerations
Treat intent and repository text as untrusted evidence, never executable instructions. Resolve and bound all paths under the repository before reading; reject symlinked feature roots and caller-selected write roots. The fingerprint is an integrity comparison, not authentication or authorization. Apply reuses sandbox, policy, escalation, and owning-skill checks and cannot grant permissions. Avoid shell interpolation: invoke allow-listed argv arrays with `subprocess.run`. Cards contain hashes and relative paths, not secrets or raw sensitive context.

## Observability
Markdown and TOON expose classification evidence, selected/rejected route, context freshness, role/rigor reasons, source hashes, raw/packed/reread/net tokens, anchor recall, blockers, planned writes, fingerprint, action outcome, and next checkpoint. Deterministic diagnostics use stable error codes such as FLOW_AMBIGUOUS_INTENT, FLOW_ROUTE_DRIFT, FLOW_UNSAFE_ROOT, FLOW_CONTEXT_REJECTED, and FLOW_UNSUPPORTED_ACTION. No telemetry leaves the repository.

## Risks and Tradeoffs
A meta-skill can duplicate navigator logic; mitigate by extracting shared pure classification instead of parallel rules. Fingerprints can become unstable if presentation fields leak in; mitigate with an explicit versioned payload. Strict symlink rejection may expose legacy setups; fail closed and explain remediation rather than creating links. The 15% threshold may reject many packs; direct reading is the correct safe fallback. Two-phase review costs an extra pass but reduces anchoring and improves human auditability.

## Validation Strategy
Use synthetic repository fixtures and filesystem snapshots. Unit tests cover normalization, classification precedence, DecisionCard serialization, fingerprint stability/drift, role/rigor tables, path guards, and context threshold boundaries. Integration tests cover Explore no-write, Apply one-action dispatch, navigator regression, spec-first ordering, installed mirror parity, and catalog generation. Run focused skill suites, shared-runtime compatibility/install smoke, docs validation, full SDD gates, and refinement status. Manual checks assess newcomer readability and blind defect detection.

## Migration Notes
Add `ai-sdlc-flow` without removing or renaming `ai-sdlc-navigator` or any direct skill. Update recommended-entrypoint docs and generated catalogs while retaining direct command examples as advanced use. No state/index schema migration is required beyond additive flow fields. No root move, symlink, global install change, or automatic conversion occurs. Consumers lacking the new skill continue using current direct skills.
