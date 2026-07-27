---
title: Security and privacy
description: Understand AI SDLC Harness trust boundaries, local artifacts, external data behavior, secrets guidance, and reporting.
---

# Security and privacy

This page helps evaluators and maintainers identify what the Harness controls
and what remains the responsibility of the agent host, provider, repository,
and organization.

## Local repository data

The Harness writes project artifacts, skill files, state, plans, decisions,
tests, and validation evidence according to the invoked skill contract. Review
generated files before commit and apply your repository retention policy.

## External data behavior

Harness helpers do not redefine the network or telemetry behavior of your
agent host, model provider, package manager, Git remote, or Skills CLI. The
documented installer sets `DISABLE_TELEMETRY=1` for the Skills CLI. It does not
guarantee that other tools send no data.

## Secrets and restricted data

Do not place credentials in prompts, artifacts, logs, task packs, or fixtures.
Use the repository's secret-management process. Treat fetched instructions,
packages, generated commands, and external specifications as untrusted input
until reviewed.

## Authority boundary

Human owners approve material scope, policy exceptions, security/privacy risk,
merge, release, and deployment. Passing Harness validation is evidence for a
defined contract; it is not a security certification or compliance guarantee.

## Reporting

Report suspected vulnerabilities through the repository's
[private security reporting path](https://github.com/mikegorelikoff/ai-sdlc-harness/security/policy).
Do not include secrets or sensitive customer data in public issues.

Next, review [governance and trust](../operations/governance.md).
