# Context cache contract

## Authority

The database is a disposable projection. Repository bytes, accepted artifacts,
Git state, and human approvals remain authoritative. A cache hit is useful only
while its document hash matches the current regular file.

## Storage

Use a project-contained SQLite database with normalized metadata, documents,
chunks, FTS5 content, files, qualified symbols, occurrences, hubs, and typed
edges. Compute the logical index fingerprint
from sorted semantic rows; SQLite page layout and timestamps are not identity.
Build through a temporary database and atomically replace the accepted file.

## Retrieval

Normalize query terms without accepting caller-supplied FTS syntax. Use FTS5
only to select candidates, then compute stable integer relevance from term
occurrences and structural evidence. Break ties by path, start line, and chunk
ID. Expand graph neighbors breadth-first in sorted order with explicit depth and
node caps. Every expanded result carries its edge path and distance.

## AST completeness

Graph mode supports exactly TypeScript, Python, JavaScript, Java, C#, PHP,
Shell, C++, Go, Rust, Kotlin, and Swift through the versions and macOS arm64
wheel hashes in `parser-lock.toon`. Each selected-language file is parsed in a
bounded subprocess with runtime network denied. Missing grammars, native
crashes, timeouts, real parse errors, or extraction bounds make
`graph_complete` false. Regex and heuristic extraction never claim AST
completeness. Kotlin's grammar-reported hidden implicit separator is accepted
only when there is no explicit error node; malformed Kotlin still fails.

Trace IDs are represented by one hub plus bounded membership edges. Definitions,
references, imports, and calls come from AST nodes; a cross-symbol relation is
emitted only when the local name resolves to one exact graph target.

## Freshness and fallback

Before query or pack output, compare every indexed document hash with current
repository bytes. Missing, changed, unsafe, corrupt, or incompatible state is
not repaired implicitly. Emit an explained `direct_read` outcome and candidate
paths. A subsequent explicit `build` may refresh the projection.

## Context economics

Always load the owning step document from its validated skill manifest before
cache evidence. Count every declared critical anchor against that mandatory
document and require 100 percent recall. Pack at most one best cache range per
source path so `ai-sdlc-context-pack/v4` identity remains unambiguous. Apply
the explicit token budget after mandatory context, report raw candidate tokens,
packed tokens, savings, and skipped evidence, and select direct reads whenever
the pack is incomplete, stale, over budget, or below its configured net-savings
gate. The production AST graph gate is 25 percent; legacy lexical policy may
retain its existing 15 percent floor.

## Evaluation

Golden benchmark cases are TOON and name expected paths, expected content
anchors, the owning skill and step, the token budget, and the expected packed
or direct-read strategy. Compare lexical-only seeds with bounded graph-enhanced
results, require 100 percent mandatory and expected-anchor recall, and require
at least 25 percent savings for every production graph case that expects packed
context. Keep
wall-clock latency in a separate observational tier so deterministic receipts
remain byte-identical across repeated runs.

## Security

Do not follow symlinks, leave the repository root, make network calls, load
extensions, execute retrieved text, or persist credentials. Bind SQLite values
with parameters. Construct FTS expressions only from normalized terms. Confine
purge to a regular `.sqlite3` file under `.ai-sdlc/cache/` unless a separately
validated project-local path was explicitly supplied.

## Offline installation

Populate a wheelhouse from the exact filenames in `parser-lock.toon`, verify
every SHA-256, then install with pip `--no-index --find-links` into a dedicated
CPython 3.11 environment. Run `tests/install_graph_smoke.py --offline` with the
same lock and wheelhouse. A host without the verified graph environment retains
lexical/direct behavior and cannot claim graph completeness.
