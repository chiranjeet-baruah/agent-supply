import json
import tempfile
import unittest
from pathlib import Path

from tooling.package_plugins import check_files, expected_files
from tooling.validate import render_catalog


class MarketplacePackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "registry").mkdir()
        (self.root / "skills" / "example-skill").mkdir(parents=True)
        self.skill = self.root / "skills/example-skill/SKILL.md"
        self.skill.write_text(
            "---\nname: example-skill\ndescription: Reviews examples. Use for example reviews.\n"
            "license: Apache-2.0\n---\n\n# Example\n\nReview the example.\n",
            encoding="utf-8",
        )
        entry = {
            "id": "example-skill",
            "title": "Example Skill",
            "summary": "Review examples.",
            "category": "Testing",
            "path": "skills/example-skill",
            "version": "0.1.0",
            "license": "Apache-2.0",
        }
        (self.root / "registry/catalog.json").write_text(
            json.dumps({"schema_version": 1, "entries": [entry]}), encoding="utf-8"
        )
        (self.root / "CATALOG.md").write_text(render_catalog([entry]), encoding="utf-8")

    def write_expected(self):
        expected = expected_files(self.root)
        for relative, content in expected.items():
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        return expected

    def test_marketplaces_install_the_same_reviewed_skill(self):
        expected = self.write_expected()
        codex = json.loads(expected[Path(".agents/plugins/marketplace.json")])
        claude = json.loads(expected[Path(".claude-plugin/marketplace.json")])
        self.assertEqual([plugin["name"] for plugin in codex["plugins"]], ["example-skill"])
        self.assertEqual([plugin["name"] for plugin in claude["plugins"]], ["example-skill"])
        self.assertEqual(
            (self.root / "plugins/example-skill/skills/example-skill/SKILL.md").read_bytes(),
            self.skill.read_bytes(),
        )
        self.assertEqual(check_files(self.root, expected), [])

    def test_changed_or_unexpected_package_file_fails_check(self):
        expected = self.write_expected()
        packaged = self.root / "plugins/example-skill/skills/example-skill/SKILL.md"
        packaged.write_text("different instructions", encoding="utf-8")
        extra = self.root / "plugins/example-skill/extra.sh"
        extra.write_text("exit 0", encoding="utf-8")
        errors = check_files(self.root, expected)
        self.assertTrue(any("stale" in error for error in errors))
        self.assertTrue(any("unexpected generated file" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
