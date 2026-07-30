# Change Set Contract

The input is a UTF-8 TOON object using schema `ai-sdlc-change-set/v1` with a
non-empty `changes` array. Every change requires:

- unique `id`, such as `CHG-001`;
- stable `changed_ref`, such as `AC-004` or `DEC-012`;
- `source.path`, relative to the feature root without `..` traversal;
- positive integer `source.line` containing the exact changed reference;
- non-empty `source.detail` describing what changed.

Example:

```toon
changes[1]:
  - changed_ref: AC-004
    id: CHG-001
    source:
      detail: Retry behavior is now mandatory.
      line: 121
      path: requirements.md
schema: ai-sdlc-change-set/v1
```
