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


if __name__ == "__main__":
    unittest.main()
