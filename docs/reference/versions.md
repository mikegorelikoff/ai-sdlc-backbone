# Supported versions

The licensing API authorizes the exact product version available to a license.

| Component | Current stable version | Distribution |
| --- | --- | --- |
| AI SDLC Backbone | `5.0.1` | Licensed release authorized by the licensing API. |
| Public installer | `1.0.1` | `npx ai-sdlc-backbone` from npm. |

The product and installer use independent version lines. The release manifest
declares the minimum supported installer version, and the installer fails
closed when that requirement is not met. Historical versions and public
release notes are retained in
[CHANGELOG.md](https://github.com/mikegorelikoff/ai-sdlc-backbone/blob/main/CHANGELOG.md).
