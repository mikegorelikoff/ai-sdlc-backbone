# Security policy

## Supported versions

Security fixes are considered for currently licensed releases and the current
public installer. Exact support terms are defined by the applicable product
agreement.

## Report a vulnerability

Do not include an exploit, license key, credential, confidential source,
private URL, or personal data in a public issue or AI prompt. Use GitHub's
private vulnerability-reporting flow under **Security → Advisories → Report a
vulnerability**. If it is unavailable, ask the repository owner for a private
channel before sharing details.

Include the affected release, operating system, agent host, reproduction
prerequisites, observed impact, and the smallest safe reproduction. Redact all
secrets and customer data.

## Security boundaries

The installer treats the licensing API as authoritative, accepts only a
same-origin short-lived download grant, verifies SHA-256 before extraction,
rejects unsafe archive members, and fails closed. It never receives private
GitHub credentials. See [Security and privacy](docs/project/security-privacy.md).
