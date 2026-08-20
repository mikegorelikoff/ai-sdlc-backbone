# AI SDLC Backbone

Structure delivery. Control context. Measure adoption.

[![Documentation](https://github.com/mikegorelikoff/ai-sdlc-backbone/actions/workflows/pages.yml/badge.svg)](https://github.com/mikegorelikoff/ai-sdlc-backbone/actions/workflows/pages.yml)
[![License: Apache-2.0](https://img.shields.io/badge/Public%20content-Apache%202.0-blue.svg)](LICENSE)

AI SDLC Backbone is a licensed product for traceable, reviewable AI-assisted
software delivery. This public repository contains documentation, examples,
onboarding material, and the public installer. Product implementation is built
and released from a separate private repository.

## Why use it?

- Connect intent, requirements, decisions, implementation, tests, and evidence.
- Choose a lightweight or complete delivery flow based on change risk.
- Keep consequential scope and release decisions under human approval.
- Install without GitHub access to the private product repository.

## Quick start

Set `AI_SDLC_LICENSE_KEY` in your environment or enter it at the masked prompt,
then run the single public install action:

```bash
npx ai-sdlc-backbone
```

Verify the installed Backbone in a separate step using the command printed by
the installer for the selected agent profile.

## Expected result

The installer validates the license with the licensing service, downloads a
short-lived authorized artifact, verifies its SHA-256 checksum, and installs
the Backbone into the selected project. A failed validation or integrity check
stops installation.

## Workflow

```text
Request → Explore → Specify → Plan → Implement → Verify → Handoff
```

The canonical mental model is in [How it works](docs/how-it-works/index.md).

## Scope

This repository deliberately excludes skills, runtime logic, hooks, internal
templates, release tooling, and private tests. It does include the public
installer, safe examples, API contracts, and user documentation. The Backbone
does not replace product ownership, engineering judgment, code review, CI, or
deployment authority.

## Documentation paths

- [Start here](docs/start-here/index.md) for the canonical first run.
- [How it works](docs/how-it-works/index.md) for the canonical mental model.
- [Guides](docs/guides/index.md) for task-oriented procedures.
- [Reference](docs/reference/index.md) for exact public contracts.
- [Project](docs/project/index.md) for status and governance.

## AI SDLC product family

**Structure delivery. Control context. Measure adoption.**

- **AI SDLC Backbone — current:** structures AI-assisted software delivery.
- [Context Guard](https://github.com/mikegorelikoff/ai-sdlc-context) controls
  avoidable context growth while retaining local evidence.
- [AI SDLC Metrics](https://github.com/mikegorelikoff/ai-sdlc-metrics) measures
  local agent adoption from available evidence.

The products are complementary and independently installed.

## Security and privacy

License keys are sent only to the configured licensing API and should be
provided through the environment or masked prompt, never a command argument.
The installer receives neither GitHub credentials nor repository access. See
[Security and privacy](docs/project/security-privacy.md).

## Status

The licensed-distribution foundation is being prepared. The public installer
and API contract are present; production purchase, entitlement administration,
and the licensing service deployment remain controlled rollout activities.

## Contributing

Public contributions are limited to documentation, examples, and installer
portability/security. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Public repository content is licensed under [Apache License 2.0](LICENSE).
That license does not grant access to separately distributed private product
artifacts, which are governed by their commercial license.
