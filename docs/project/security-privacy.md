# Security and privacy

The public installer never receives a GitHub token, GitHub App private key, or
private repository credential. Only the licensing backend may authenticate to
private release storage. A license key authorizes a backend decision; it is not
a repository credential.

Provide keys through a protected environment or the masked prompt. The
backend stores only a keyed fingerprint of each key, records auditable license
events without plaintext keys, and issues expiring one-time download grants.

The release pipeline uses an allowlist and produces a SHA-256. The installer
verifies that checksum before extraction and fails closed on any discrepancy.

Report vulnerabilities through the private channel in the repository
`SECURITY.md`. Do not include a license key or secret in a report.
