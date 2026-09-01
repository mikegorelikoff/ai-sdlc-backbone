---
type: "ai-sdlc.qa-plan"
title: "QA Plan"
description: "Acceptance, regression, risk, and manual validation plan."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-09-01T09:52:04Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "qa.md"
  path: "specs/022-ai-sdlc-loop/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-09-01"
  trace_ids:
    - "TC-032"
    - "TC-039"
  related_artifacts:
    - "specs/022-ai-sdlc-loop/branch-plan.md"
    - "specs/022-ai-sdlc-loop/code-review.md"
    - "specs/022-ai-sdlc-loop/commit-message.md"
    - "specs/022-ai-sdlc-loop/commit-readiness.md"
    - "specs/022-ai-sdlc-loop/decision-log.md"
    - "specs/022-ai-sdlc-loop/design.md"
    - "specs/022-ai-sdlc-loop/index.md"
    - "specs/022-ai-sdlc-loop/plan.md"
    - "specs/022-ai-sdlc-loop/requirements.md"
    - "specs/022-ai-sdlc-loop/security-review.md"
    - "specs/022-ai-sdlc-loop/tasks.md"
    - "specs/022-ai-sdlc-loop/test-cases.md"
    - "specs/022-ai-sdlc-loop/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "approved"
    - "engineering-quality-gate"
    - "ai-sdlc-loop"
---

# QA

## Change Summary
Add `ai-sdlc-engineering-quality-gate` to Harness core and an autonomous `ai-sdlc-loop-engineering-quality-gate` to Loop. Make the Loop gate mandatory between Implement and Verify, bind its canonical deterministic report to the current approved diff, and preserve independent invocation for any post-implementation review.

## Acceptance Scenarios
QA-001 through QA-014 retain existing Loop acceptance.
QA-015: every Loop install profile contains the quality gate; Harness default/core discovery contains its canonical counterpart; both selectors resolve prepare without hidden dependencies.
QA-016: a representative fixture yields a bounded repository profile, 2–5 useful examples when available, evidence-backed applicable patterns, sorted typed findings, and byte-identical output across repeated and absolute-path-varied runs.
QA-017: the gate identifies a seeded High or Medium defect, applies only the safe in-scope correction, preserves unrelated work, reruns relevant checks, and leaves Low or clarification-blocked findings documented.
QA-018: failed, not-run required, unavailable, or stale verification is reported truthfully; PASS is impossible when a required gate or blocking finding remains.
QA-019: Loop Verify rejects missing, non-ready, invalid, or stale quality evidence and proceeds only with a current ready report for the same change fingerprint.
QA-020: three realistic examples, the example report, schemas, generated Harness catalogs, Loop Reference, inventory counts, and changelogs agree with executable source.

## Regression Targets
Existing approval boundaries, allowed-path scope, unrelated dirty work, Git index/HEAD, TOON-only durable contracts, output redaction, installer atomicity, all public paths, top-level navigation order, primary install command, generated catalogs, and the current validation/code-review/security/commit stages. New regression targets are deterministic candidate/finding/check ordering, report path independence, current-diff binding, and mandatory Loop gate enforcement.

## Risk Notes
High: a stale or fabricated PASS could allow unreviewed code into Verify. High: remediation could escape approved paths or overwrite unrelated work. Medium: nondeterministic candidate ranking or report encoding could create irreproducible decisions. Medium: overlap with code review/validation could duplicate work or confuse ownership. Medium: mandatory enforcement is a workflow compatibility change. Mitigation is script-enforced schemas/fingerprints/readiness, atomic writes, explicit authority checks, stable tie-breakers, and focused integration tests.

## Validation Commands
Focused Harness: new skill unit tests, standard skill-script contract, step selector, module loader, managed inventory, flow routing, and generated catalog check. Focused Loop: new quality-gate tests plus install/docs/workflow suites. Then run complete Loop unittest/compile/shell/MkDocs/diff validation and the root AGENTS.md sequence: catalog check, docs validation/tests, strict MkDocs build, rendered validation, and diff hygiene. Record failed, blocked, unavailable, and skipped commands separately.

## Manual Checks
Invoke each namespaced skill on a disposable repository change with at least two nearby implementations. Confirm it reads repository instructions, selects useful comparisons, creates findings before edits, fixes only a seeded material issue, reruns checks, and produces the concise report. Change one reviewed file afterward and confirm Loop Verify rejects the stale report. Inspect that no absolute temp path, timestamp, duration, secret, or unrelated change enters the canonical fingerprinted output.

## Signoff
Status: passed for TC-032 through TC-039. Owner: maintainer. Deterministic
fixtures, adversarial remediation, current-diff and executable-mode staleness,
mandatory Loop enforcement, exact inventories, generated catalogs, and a
disposable repository forward fixture all pass. A fresh delegated provider run
was unavailable after exhausting its usage allowance and is recorded as such,
not as passing evidence. Pre-existing hosted/release UAT T006 remains separately
pending and does not weaken this change-specific gate.
