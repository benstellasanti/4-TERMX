"""Pruebas de regresión del generador de documentación."""
import unittest

from update_readme_tree import build_tree_markdown, description, file_type
from pathlib import Path


class RepositoryTreeTests(unittest.TestCase):
    def test_tree_preserves_directory_hierarchy(self):
        files = [
            ("README.md", 10),
            (".github/workflows/update-tree.yml", 20),
            ("docs/architecture.md", 30),
            ("scripts/bajada", 40),
        ]
        tree = build_tree_markdown(files)
        self.assertIn("├── .github/", tree)
        self.assertIn("│   └── workflows/", tree)
        self.assertIn("│       └── update-tree.yml", tree)
        self.assertIn("├── docs/", tree)
        self.assertIn("│   └── architecture.md", tree)
        self.assertIn("├── scripts/", tree)
        self.assertIn("│   └── bajada", tree)
        self.assertIn("└── README.md", tree)
        self.assertIn("```text", tree)

    def test_known_files_have_specific_descriptions(self):
        self.assertIn("componentes principales", description("docs/architecture.md"))
        self.assertIn("Formulario guiado", description(".github/ISSUE_TEMPLATE/bug_report.yml"))
        self.assertIn("Lista de comprobación", description(".github/PULL_REQUEST_TEMPLATE.md"))

    def test_github_templates_have_accurate_types(self):
        self.assertEqual(file_type(Path(".github/ISSUE_TEMPLATE/bug_report.yml")), "Plantilla de Issue")
        self.assertEqual(file_type(Path(".github/PULL_REQUEST_TEMPLATE.md")), "Plantilla de Pull Request")


if __name__ == "__main__":
    unittest.main()
