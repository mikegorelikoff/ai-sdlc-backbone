# Repository instructions

Keep existing engineering and release contracts in `CONTRIBUTING.md`, the
maintainer guides, skill instructions, and validation references.

## Documentation contract

- Product name: **AI SDLC Harness**.
- Ecosystem wording: **AI SDLC product family** and “Structure delivery.
  Control context. Measure adoption.”
- Public top-level navigation must remain, in order: Home; Start here; How it
  works; Guides; Reference; Project.
- README order is product name, outcome, badges, description, Why use it?,
  Quick start, expected result, workflow, scope, documentation paths, product
  family, security/privacy, status, contributing, license.
- Keep the primary install action in README, Home, and Start here to one shell
  command; put verification in a separate step.
- Use the guide template: Goal; When to use it; Prerequisites; Procedure;
  Verify; Troubleshooting; Next step.
- Canonical sources are Start here for first run, How it works for the mental
  model, Reference for exact contracts, and Project for status and governance.
- Do not duplicate canonical explanations. Link to them.
- Preserve the product-family block and
  `docs/assets/stylesheets/ai-sdlc.css`.
- Verify commands against source, CLI help, tests, or reproducible fixtures
  before publishing them.
- Keep generated catalogs generated; run their check command instead of
  editing generated output by hand.
- Preserve public paths. Record any unavoidable move in
  `docs/project/decision-log.md` and provide a redirect or legacy stub.
- Update `docs/project/decision-log.md` and `CHANGELOG.md` for material
  documentation changes.

## Build and validate

```bash
python3 -m pip install --require-hashes -r requirements-docs.lock
python3 docs/scripts/build_catalog.py --check
python3 docs/scripts/validate_docs.py
python3 -m unittest discover -s docs/tests -v
mkdocs build --strict
python3 docs/scripts/validate_rendered.py site
git diff --check
```
