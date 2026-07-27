# AI SDLC Harness

Turn a software request into traceable, reviewable delivery artifacts,
implementation, evidence, and handoff.

[![Skills CI](https://github.com/mikegorelikoff/ai-sdlc-harness/actions/workflows/skills-ci.yml/badge.svg)](https://github.com/mikegorelikoff/ai-sdlc-harness/actions/workflows/skills-ci.yml)
[![Documentation](https://github.com/mikegorelikoff/ai-sdlc-harness/actions/workflows/pages.yml/badge.svg)](https://github.com/mikegorelikoff/ai-sdlc-harness/actions/workflows/pages.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

AI SDLC Harness gives people and AI agents a repository-native path from intent
to verified delivery. Skills guide each stage, deterministic helpers maintain
artifacts and state, and human approval remains explicit at consequential
decisions.

## Why use it?

- Keep requirements, decisions, tasks, tests, and evidence connected.
- Choose lightweight or complete rigor based on change risk.
- Resume work across sessions and agent hosts from repository artifacts.
- Preserve human authority over scope, trade-offs, exceptions, and release.

## Quick start

From the project that will use the Harness, install every skill for one agent
with one command:

```bash
curl -fsSL https://raw.githubusercontent.com/mikegorelikoff/ai-sdlc-harness/main/install.sh | sh -s -- codex
```

Then verify the project-scoped installation:

```bash
DISABLE_TELEMETRY=1 npx -y skills@1.5.19 list --json
```

Prerequisites are Git, Node.js `>=22.20.0`, npm, Python `3.10+`, and a
supported AI agent host. Replace `codex` with your Skills CLI agent identifier.
Review remote scripts before running them.

## Expected first result

The installer adds project-scoped Harness skills for the named agent. The
verification command returns a JSON inventory that includes the installed
`ai-sdlc-*` skills. Start with a read-only Explore request:

```text
Use ai-sdlc-flow to Explore this request. Show the route, evidence, rigor,
roles, blockers, planned writes, and next checkpoint. Do not Apply until I
approve the card.

Request: add a health endpoint to this service.
```

## Product workflow

```text
Request → Explore → Specify → Plan → Implement → Verify → Handoff
```

Use `ai-sdlc-flow` as the recommended entry point. Choose `--quick-flow` for a
bounded, low-risk change, `--full-flow` for complete predecessor checks and
traceability, or invoke a known owning skill directly when you already
understand its contract.

## What it does and does not do

The Harness structures delivery with skills, Markdown artifacts, compact
machine state, deterministic helpers, validation evidence, and explicit
handoffs. It does not replace product ownership, engineering judgment, code
review, security review, CI, deployment authority, or proof of business
impact. Repository tests verify mechanisms; they do not prove ROI, faster
delivery, lower cost, or better quality in your environment.

## Documentation paths

- [Start here](docs/start-here/index.md) for installation and a first Explore
  request.
- [How it works](https://mikegorelikoff.github.io/ai-sdlc-harness/how-it-works/)
  for the workflow, paths, artifacts, and authority model.
- [Guides](https://mikegorelikoff.github.io/ai-sdlc-harness/guides/) for first
  features, existing projects, roles, adoption, and operations.
- [Pilot and adoption](docs/adoption/index.md) for a bounded evaluation with
  explicit evidence and stop criteria.
- [Reference](https://mikegorelikoff.github.io/ai-sdlc-harness/reference/) for
  exact skill, script, schema, flag, and compatibility contracts.
- [Project](https://mikegorelikoff.github.io/ai-sdlc-harness/project/) for
  maturity, limitations, security, releases, audits, and maintenance.

## AI SDLC product family

**Structure delivery. Control context. Measure adoption.**

- **AI SDLC Harness — current:** structures AI-assisted software delivery.
- [Context Guard](https://github.com/mikegorelikoff/ai-sdlc-context) controls
  avoidable context growth while retaining full local evidence.
- [AI SDLC Metrics](https://github.com/mikegorelikoff/ai-sdlc-metrics)
  measures local Codex CLI and Claude Code adoption from available evidence.

The products are complementary and independently installed. This repository
does not claim a built-in technical integration with the other two.

## Security and privacy

Treat agent instructions, generated commands, packages, and external content
as untrusted until reviewed. The installer disables Skills CLI telemetry, but
that does not change the data behavior of your agent host or model provider.
Do not send secrets or restricted data unless your organization permits it.
Report vulnerabilities privately through [SECURITY.md](SECURITY.md).

## Project status

The documentation currently targets release candidate `v3.0.0-rc.2`; the
previous stable release is `v2.1.0`. Review
[compatibility](docs/reference/compatibility.md), [limitations](docs/explanation/maturity-limitations.md),
and the [3.0 migration guide](docs/how-to/migrate-3.0.md) before adoption.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and the
[maintainer guide](docs/maintainers/index.md). Validate documentation with:

```bash
python3 docs/scripts/validate_docs.py
python3 -m unittest discover -s docs/tests -v
mkdocs build --strict
```

## License

Licensed under the [Apache License 2.0](LICENSE). Third-party source review and
attribution records are maintained in `docs/_data/content_sources.yml`.
