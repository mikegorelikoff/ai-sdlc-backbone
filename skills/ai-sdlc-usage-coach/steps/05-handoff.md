# Handoff

## Entry

Coaching evidence is validated.

## Procedure

Present prioritized suggestions or behavioral reports to the contributor.
Record user feedback (accepted, rejected, deferred) into the append-only journal when requested.

## Exit

The contributor has actionable, evidence-backed workflow insights without blocking execution.

## Chat presentation

Present the result using the owning `SKILL.md` Chat Output Contract and local [chat schema](../references/chat-output.toon). The machine handoff remains native; show its decision, evidence and owned action without dumping the journal.

## Examples

### Usage report example

```text
# AI SDLC Usage & Behavioral Report

- Total Scanned Sessions: 3
- Total Recorded Events: 18
- Scanned At: 2026-09-28T20:30:00Z

## 1. Skill Coverage & Invocations
- **ai-sdlc-sdd**: 3 invocations (last used: 2026-09-28T20:15:00Z) [completed:3]
- **ai-sdlc-engineering-quality-gate**: 4 invocations (last used: 2026-09-28T20:25:00Z) [completed:3, failed:1]

## 2. Common Transitions & Workflow Motifs
- ai-sdlc-sdd -> ai-sdlc-engineering-quality-gate: 3 occurrences

## 3. Rework & Friction Motifs
- 1 rework cycle detected (quality gate failure followed by immediate re-invocation)
```
