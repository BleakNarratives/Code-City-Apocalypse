#!/usr/bin/env python3
"""Dependency-light acceptance tests for the Code City scanner boundary."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from backend.core.scanner import CodebaseScanner


class CodeCityScannerContractTests(unittest.TestCase):
    def test_scanner_returns_city_contract_for_supported_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "sample.py"
            source.write_text(
                "def short():\n    return 1\n",
                encoding="utf-8",
            )

            city = CodebaseScanner().scan_codebase(str(root))

        self.assertEqual(city["total_files"], 1)
        self.assertEqual(city["total_errors"], 0)
        self.assertEqual(city["root_path"], str(root))
        self.assertEqual(len(city["buildings"]), 1)
        self.assertEqual(city["buildings"][0]["path"], "sample.py")
        self.assertEqual(city["buildings"][0]["type"], "py")
        self.assertIn("syntax_insights", city["buildings"][0])
        self.assertIn("bloat_report", city["buildings"][0])

    def test_scanner_reports_python_syntax_errors_as_monsters(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "broken.py").write_text(
                "def broken(:\n    pass\n",
                encoding="utf-8",
            )

            city = CodebaseScanner().scan_codebase(str(root))

        self.assertEqual(city["total_files"], 1)
        self.assertEqual(city["total_errors"], 1)
        self.assertEqual(city["monsters"][0]["type"], "syntax_error")
        self.assertEqual(city["monsters"][0]["line"], 1)


if __name__ == "__main__":
    unittest.main()
