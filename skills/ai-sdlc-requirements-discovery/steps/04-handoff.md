# Handoff — Next Conversation and Owner

## Entry

The packet passes the discovery quality checks or clearly identifies remaining gaps.

## Procedure

- Include the helper validation result, report path/fingerprint and any source
  limitations. A structurally checked local report is not authenticated owner
  approval. Route accepted direction through existing product authority checks.

- Present the provisional recommendation and the highest-priority questions
  together with the roles that can answer them. Name the next concrete action
  and the expected evidence; use the user's language.
- Identify packet completion separately from business-decision acceptance.
  If answers are missing, the next step is elicitation or source collection.
  When replies arrive, cite them, update affected options/requirements, and keep
  rejected or superseded assumptions traceable.
- Send an accepted feature direction to `ai-sdlc-ba` for actors, rules and
  acceptance logic. For an initiative whose customer problem still needs a
  broader interview, suggest `ai-sdlc-working-backwards-discovery`.
- Suggest `ai-sdlc-research` only if installed and additional sourced research
  is needed. This assistant has no mandatory optional-module dependency.
- Emit `ai-sdlc-handoff/v2` with `result`, `blockers`, `next_required` and
  `next_optional`; each action supplies reason, command and expected_artifact.

## Exit

Return the packet and next owner. Do not start implementation or contact stakeholders
unless the user has authorized that further work.
