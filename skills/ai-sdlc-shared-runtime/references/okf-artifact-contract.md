# OKF Artifact Contract

Use this reference whenever a skill writes durable Markdown. Analysis printed to
stdout and authored repository documentation are outside this contract.

## Required write sequence

1. Select an explicit concept profile from `ai_sdlc_okf.py`; never infer `type`
   from arbitrary content.
2. Render portable OKF v0.2 fields through the shared runtime and keep
   `artifact_metadata` or other producer data as extension blocks.
3. Resolve `generated.by` from `--generated-by`, then a valid existing actor,
   then `process:ai-sdlc`.
4. Update `generated.at` only for a meaningful content or source change.
5. Remove stale verification when content or sources change. Lifecycle status
   does not imply verification; `verified` requires actor, time, and evidence.
6. Write atomically, then refresh the owning bundle's progressive indexes.

## Bundle boundaries

- `specs/<feature>/` and `specs-refiniment/<feature>/` are feature bundles.
- `changes/<change-id>/` is a change bundle.
- `_ai_sdlc/` is the repository runtime bundle.
- Root `index.md` frontmatter contains only `okf_version: "0.2"`.
- Nested `index.md` files have no frontmatter. `index.md` and `log.md` are
  reserved and are never rendered as concepts.
- `_ai_sdlc/specs-index.toon` is the compact cross-feature router. Do not
  generate a workspace `specs-index.md`.

## Supported paths

- Project context: `_ai_sdlc/context/project-context.md`
- Module catalog: `_ai_sdlc/modules.md`
- There is no runtime reader, writer, copy, symlink, or fallback for root
  `project-context.md` or workspace `specs-index.md`.

## Legacy first write

Untouched legacy features remain readable. Before the first durable write,
preflight every Markdown concept in the feature. Apply the complete migration
only after all profiles and frontmatter are conflict-free; otherwise leave the
original tree byte-identical.

Validate with:

```bash
python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_okf.py --check <bundle>
```
