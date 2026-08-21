import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.build_skill_package import REQUIRED_FILES, build_zip


class SkillPackageTests(unittest.TestCase):
    def test_default_package_preserves_codex_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "skill.zip"
            build_zip(output)
            with zipfile.ZipFile(output) as archive:
                skill_md = archive.read("SKILL.md").decode("utf-8")

        frontmatter = skill_md.split("---", 2)[1]
        self.assertNotIn("\nslug:", frontmatter)
        self.assertNotIn("\nversion:", frontmatter)

    def test_skillhub_package_promotes_required_metadata(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "skillhub.zip"
            build_zip(output, skillhub=True)
            with zipfile.ZipFile(output) as archive:
                skill_md = archive.read("SKILL.md").decode("utf-8")
                self.assertEqual(
                    set(archive.namelist()),
                    {path.as_posix() for path in REQUIRED_FILES},
                )

        frontmatter = skill_md.split("---", 2)[1]
        self.assertIn("\nslug: lynse-cli", frontmatter)
        self.assertIn("\ndisplayName: 灵光记 / Lynse CLI", frontmatter)
        self.assertIn("\nversion: 1.8.0", frontmatter)
        self.assertIn("\nsummary:", frontmatter)


if __name__ == "__main__":
    unittest.main()
