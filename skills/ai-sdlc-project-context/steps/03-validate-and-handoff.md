# Validate and Handoff — ai-sdlc-project-context: Evidence-Backed Repository Memory

> Selector: validate, handoff, or complete

## Entry

Enter after execution has produced the expected artifact, code, plan, decision, or diagnostic evidence.

## Procedure

## Output Spec

The TOON schema `ai-sdlc-project-context/v1` includes repository, revision,
fingerprint, drift status, stack, commands, architecture paths, and evidence
rows with exact `path`, `line`, `kind`, and `detail` fields.

The canonical TOON `ai-sdlc-context-pack/v3` record includes task identity,
typed presentation preferences, content authority, topology and revision
identity, deterministic budget use, selector outcomes, relevance-ranked source
ranges, exclusions, freshness warnings, sufficient-context status, targeted
next reads, and fingerprint.

Quality gate:

- Pass when both outputs share revision and fingerprint, every claim has a
  source anchor, secret paths are excluded, and `--check` reports current.
- Fail when context contains unsupported rules, leaks secret material, lacks
  drift identity, or presents stale evidence as current.

## Examples

Valid evidence:

```text
path=README.md line=32 kind=command detail=curl ... install.sh ... codex
```

Invalid counter-example:

```text
The project probably uses Kubernetes in production.
```

Reject unsupported inference without repository evidence.

## Edge Cases

- A repository without Git uses revision `unversioned`; fingerprint drift still
  works.
- An empty repository produces explicit not-detected values.
- Untracked high-signal files participate in the fingerprint when readable.
- Symlinked or secret-named sources are skipped.
- Credential-like assignment content is excluded even when its filename looks safe.
- Custom selectors that do not match remain visible with the failed condition.
- Budget exhaustion records skipped candidates instead of silently truncating
  the candidate list.
- A Git revision change without evidence-content change still reports revision
  drift so consumers can consciously accept regeneration.

## Scope Boundary

- Do not create feature requirements, architecture, tests, or tasks.
- Do not modify repository source or configuration.
- Do not read secret values or production credentials.
- Do not replace state, indexes, decisions, or validation evidence.
- Do not return secret-like content, follow symlinks, or exceed the requested
  task-pack budget.
- Use `$ai-sdlc-flow` Explore for downstream workflow selection.

## Exit

Report outcome, validation evidence, unresolved risks, and the next required or optional owner directly in the active response.
