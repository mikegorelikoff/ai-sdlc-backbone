# AI SDLC Harness Installer

```bash
export AI_SDLC_LICENSE_KEY="ASDL-..."
npx @ai-sdlc/install
```

The key is sent only to the configured licensing API. The installer accepts no license-key CLI argument, verifies SHA256 before extraction, rejects unsafe archive members, and never receives GitHub credentials.
