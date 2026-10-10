import json
import tempfile
import unittest
from pathlib import Path

from tooling.validate import render_catalog, validate_repository


class RepositoryValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "registry").mkdir()
        (self.root / "skills" / "example-skill").mkdir(parents=True)
        (self.root / "skills" / "example-skill" / "SKILL.md").write_text(
            "---\nname: example-skill\ndescription: Reviews an example. Use for example reviews.\nlicense: Apache-2.0\n---\n\n# Example\n\nReview the example.\n",
            encoding="utf-8",
        )
        self.entry = {
            "id": "example-skill",
            "title": "Example Skill",
            "summary": "Review examples.",
            "category": "Testing",
            "path": "skills/example-skill",
            "version": "0.1.0",
            "license": "Apache-2.0",
        }
        self.write_registry([self.entry])
        (self.root / "CATALOG.md").write_text(render_catalog([self.entry]), encoding="utf-8")

    def write_registry(self, entries):
        (self.root / "registry" / "catalog.json").write_text(
            json.dumps({"schema_version": 1, "entries": entries}), encoding="utf-8"
        )

    def test_valid_repository(self):
        self.assertEqual(validate_repository(self.root), [])

    def test_duplicate_registry_id_is_rejected(self):
        self.write_registry([self.entry, dict(self.entry)])
        self.assertTrue(any("duplicate id" in error for error in validate_repository(self.root)))

    def test_path_traversal_is_rejected(self):
        self.write_registry([{**self.entry, "path": "../outside"}])
        self.assertTrue(any("path must be" in error for error in validate_repository(self.root)))

    def test_symlinked_skill_file_is_rejected(self):
        outside = self.root / "outside.md"
        outside.write_text("private", encoding="utf-8")
        skill_file = self.root / "skills" / "example-skill" / "SKILL.md"
        skill_file.unlink()
        skill_file.symlink_to(outside)
        self.assertTrue(any("symlinks are not allowed" in error for error in validate_repository(self.root)))

    def test_frontmatter_mismatch_is_rejected(self):
        skill_file = self.root / "skills" / "example-skill" / "SKILL.md"
        skill_file.write_text(skill_file.read_text(encoding="utf-8").replace("name: example-skill", "name: other-skill"), encoding="utf-8")
        self.assertTrue(any("name must match" in error for error in validate_repository(self.root)))

    def test_yaml_empty_description_is_rejected(self):
        skill_file = self.root / "skills" / "example-skill" / "SKILL.md"
        skill_file.write_text(skill_file.read_text(encoding="utf-8").replace(
            "description: Reviews an example. Use for example reviews.", 'description: ""'
        ), encoding="utf-8")
        self.assertTrue(any("description must be" in error for error in validate_repository(self.root)))

    def test_unlisted_skill_is_rejected(self):
        (self.root / "skills" / "hidden-skill").mkdir()
        self.assertTrue(any("unlisted skill" in error for error in validate_repository(self.root)))

    def test_stale_catalog_is_rejected(self):
        (self.root / "CATALOG.md").write_text("stale\n", encoding="utf-8")
        self.assertTrue(any("stale" in error for error in validate_repository(self.root)))

    def test_symlinked_catalog_is_rejected(self):
        outside = self.root / "outside.md"
        outside.write_text("private", encoding="utf-8")
        catalog = self.root / "CATALOG.md"
        catalog.unlink()
        catalog.symlink_to(outside)
        self.assertTrue(any("CATALOG.md: symlinks" in error for error in validate_repository(self.root)))

    def test_catalog_escapes_listing_markup(self):
        entry = {**self.entry, "title": "Review [Go]", "summary": "Check <unsafe> | text"}
        catalog = render_catalog([entry])
        self.assertIn("Review &#91;Go&#93;", catalog)
        self.assertIn("Check &lt;unsafe&gt; &#124; text", catalog)


if __name__ == "__main__":
    unittest.main()
