import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = {
    "skills", "modules", "config", "compatibility", "specs", "specs-refiniment",
    "runtime", "hooks", "templates", "install.py", "install.sh",
}


class PublicLeakageTest(unittest.TestCase):
    def test_private_paths_are_absent_from_worktree(self):
        present = sorted(name for name in FORBIDDEN if (ROOT / name).exists())
        self.assertEqual(present, [])

    def test_private_paths_are_not_tracked(self):
        result = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True
        )
        tracked = result.stdout.splitlines()
        leaked = [path for path in tracked if path.split("/", 1)[0] in FORBIDDEN]
        self.assertEqual(leaked, [])

    def test_required_public_surfaces_exist(self):
        for relative in ["README.md", "docs/index.md", "examples", "installer/package.json", "mkdocs.yml"]:
            self.assertTrue((ROOT / relative).exists(), relative)

    def test_active_product_identity_is_backbone(self):
        active = [
            "README.md",
            "mkdocs.yml",
            "docs/index.md",
            "docs/start-here/index.md",
            "docs/guides/install.md",
            "docs/reference/licensing-api.yaml",
            "installer/package.json",
            "installer/src/cli.js",
        ]
        for relative in active:
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn("AI SDLC Harness", text, relative)
            self.assertNotIn("ai-sdlc-harness", text, relative)
        package = (ROOT / "installer/package.json").read_text(encoding="utf-8")
        self.assertIn('"name": "ai-sdlc-backbone"', package)
        self.assertIn('"ai-sdlc-backbone": "src/cli.js"', package)


if __name__ == "__main__":
    unittest.main()
