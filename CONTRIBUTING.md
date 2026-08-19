# Contributing

This public repository accepts changes to documentation, examples, community
metadata, and the public installer. Product skills, runtime logic, internal
templates, release packaging, and implementation tests belong in the private
core repository.

For documentation changes, preserve public paths, the top-level navigation
order, the product-family block, and the guide template. Material changes must
update `docs/project/decision-log.md` and `CHANGELOG.md`.

Validate a contribution with:

```bash
python3 docs/scripts/build_catalog.py --check
python3 docs/scripts/validate_docs.py
python3 -m unittest discover -s docs/tests -v
python3 -m unittest discover -s tests -v
mkdocs build --strict
python3 docs/scripts/validate_rendered.py site
git diff --check
```

Installer changes additionally require:

```bash
cd installer
npm test
```
