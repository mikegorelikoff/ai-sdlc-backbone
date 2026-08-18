---
type: "ai-sdlc.security-review"
title: "Security Review"
description: "Security threats, controls, findings, and validation evidence."
tags:
  - "ai-sdlc"
  - "security"
  - "review"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-17T11:55:59Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "security-review.md"
  path: "specs/022-ai-sdlc-loop/security-review.md"
  workspace: "implementation"
  skill: "ai-sdlc-security-testing"
  flow_mode: "full"
  state_file: "specs/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs/022-ai-sdlc-loop/decision-log.md"
  status: "validated"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-08-17"
  trace_ids:
    - "TC-002"
    - "TC-009"
    - "TC-012"
    - "TC-013"
    - "TC-015"
    - "TC-026"
    - "TC-027"
    - "TC-028"
    - "TC-029"
  related_artifacts:
    - "specs/022-ai-sdlc-loop/branch-plan.md"
    - "specs/022-ai-sdlc-loop/decision-log.md"
    - "specs/022-ai-sdlc-loop/design.md"
    - "specs/022-ai-sdlc-loop/index.md"
    - "specs/022-ai-sdlc-loop/plan.md"
    - "specs/022-ai-sdlc-loop/qa.md"
    - "specs/022-ai-sdlc-loop/requirements.md"
    - "specs/022-ai-sdlc-loop/tasks.md"
    - "specs/022-ai-sdlc-loop/test-cases.md"
    - "specs/022-ai-sdlc-loop/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-security-testing"
    - "security-review"
    - "validated"
    - "ai-sdlc-loop"
---

# security-review.md

## Trust Boundaries
Protected assets are repository source, Git index and HEAD, explicit approval intent, verification evidence, the seventeen installed skill trees, and local TOON state. Externally controlled inputs are project root, feature, request, allowed paths, reviewer text, fingerprints, commands, commit message, profile/root, repository contents, and Git state. Privileged effects are skill installation, state/receipt/evidence writes, command execution, staging, commit, and promotion output. The original review found `.ai-sdlc-loop` and install-record ancestors could be symlinks to an external directory. The TOON/multi-skill review additionally found that tree digests followed linked files. Resolution: every state component rejects symlinks and resolved escape before reads or writes, and package verification now rejects any linked tree entry; dedicated TC-002, TC-003, and TC-009 abuse fixtures pass. Owner: developer. Impact: prevented out-of-project writes and external-file reads during verification. No unresolved critical or high trust-boundary finding remains.

## Authn/Authz
Loop does not authenticate identities and does not claim cryptographic reviewer identity. Authorization is an explicit local capability receipt containing action, decision, reviewer label, and exact current subject fingerprint. Implement and commit have separate receipts; rejected, absent, stale, or mismatched authority fails before protected effects. The skill explicitly forbids the agent from recording approval without the user's decision. Commit rechecks spec, evidence, change snapshot, and commit receipt before staging. Residual risk: a malicious local process with repository write access can forge receipts; this is documented as outside the local trust model. Owner: user/repository operator. Impact: use OS and repository access controls for adversarial multi-user hosts. Resolution: do not represent receipts as identity proofs.

## Input Validation
Feature slugs are bounded by an allowlist. Requests are non-empty and whitespace-normalized. Source and install paths reject absolute paths, traversal, NUL, Git/Loop metadata overlap, symlink ancestors, and resolved escape. Changed paths come from NUL-delimited argv-based Git commands and must be equal to or below approved paths. TOON roots, declared counts, duplicate keys, schema versions, feature identity, and fingerprints are checked before use. Subprocesses use argv with `shell=False`; Git arguments use explicit argv and `--` before paths. Installer profiles and the exact seventeen-member package are enumerated; only the generic profile accepts a project-relative root. Tests cover malformed TOON, traversal, symlink escape, linked package content, drift, invalid authority, helper loading, review output containment, and out-of-scope preservation. No unresolved input-validation finding remains.

## Secret Handling
Verification captures bounded trailing output and redacts case-insensitive authorization bearer, token, password, secret, and private-key-like material before persistence; argv evidence is redacted too. Synthetic TC-012 proves the raw value is absent. Runtime has no telemetry or network. Requests, reviewer labels, commit messages, and promoted artifacts can still contain user-supplied sensitive text because arbitrary semantic content cannot be safely classified. Owner: user and reviewer. Impact: accidental secrets in these fields can persist locally or in Git history. Resolution: skill and SECURITY.md prohibit secrets in those fields; use synthetic test values and inspect artifacts before promotion.

## Data Exposure
TOON install records contain profile, project-relative skills root, seventeen skill names, and digests. TOON specs contain request, allowed paths, trace IDs, and fingerprints. Requirements, QA, and release reviews contain user-supplied evidence text, validation summaries, gates, blockers, and residual risks. Evidence contains changed relative paths, file digests, command argv, bounded redacted output, exit status, and fingerprints. Approval receipts contain reviewer-supplied label and timestamp. TOON promotion deliberately copies supported fields. No file contents, environment dump, remote identity, telemetry, or credentials are intentionally collected. `.gitignore` excludes `.ai-sdlc-loop/`. Owner: repository operator. Impact: command output, review text, or request text may still be sensitive after imperfect heuristic redaction. Resolution: keep state local, choose narrow commands, review before retention/promotion, and report redaction bypasses privately.

## Abuse Cases
Covered abuse paths: traversal or absolute install/source scope; symlink escape through source, state, or install metadata; unmanaged target collision; managed drift overwrite; approval absence, rejection, mismatch, staleness, or replay after change drift; out-of-scope dirty work; failed/missing/timed-out verification; secret-bearing output; malformed or incompatible promotion; commit denial with HEAD/index equality. Commit failure restores the prior index tree. Residual release risk: the one-line installer trusts GitHub HTTPS and the selected release tag; a moved/compromised tag could change downloaded bytes. Owner: Loop maintainer. Impact: installer supply-chain compromise. Resolution: protect release administration, publish immutable signed release provenance when available, and pin Harness submodule to the validated commit; this residual risk blocks neither local candidate review nor exact submodule identity checks.

## Security Validation
Evidence: `python3 -m unittest discover -s tests -v` passes 37 tests including malformed/canonical TOON, exact namespaced skill inventory, manifests, delivery-control helper loading, review output containment, TC-002, TC-003, TC-009, TC-012, TC-013, TC-015, and TC-026 through TC-030; compile, `sh -n install.sh`, and `git diff --check` pass. Hosted run `32126939831` passes Linux, macOS, and Windows; `v0.1.1`, remote `main`, the successful remote installer fixture, and the parent gitlink resolve to `8ee8f5b8da9fccd83a277e9b684821d50755ccd2`. Manual source review inspected TOON decoding, install target/state containment, package symlinks, fingerprint construction, approval checks, changed-path enforcement, subprocess construction, helper dependency fallback, review path containment, fail-closed review readiness, redaction, atomic writes, promotion, and Git staging/commit rollback. Finding summary: the linked-tree digest, optional dependency, Windows encoding, and generated-bytecode scan gaps were fixed; no open critical or high finding remains. Remaining validation is the parent repository-required suite and TC-024 human UAT. Owner: maintainer. Impact: parent integration is provisional until those gates finish. Next step: execute parent checks and preserve explicit human signoff.
