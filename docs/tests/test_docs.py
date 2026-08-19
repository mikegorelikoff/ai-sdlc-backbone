import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class DocumentationContractTest(unittest.TestCase):
    def test_source_validator(self):
        result = subprocess.run(
            [sys.executable, "docs/scripts/validate_docs.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_guide_template(self):
        guide = (ROOT / "docs/guides/install.md").read_text(encoding="utf-8")
        headings = ["## Goal", "## When to use it", "## Prerequisites", "## Procedure", "## Verify", "## Troubleshooting", "## Next step"]
        positions = [guide.find(heading) for heading in headings]
        self.assertNotIn(-1, positions)
        self.assertEqual(positions, sorted(positions))


if __name__ == "__main__":
    unittest.main()
