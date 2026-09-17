import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "source/expansion/cleaner.py"
spec = importlib.util.spec_from_file_location("cleaner", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Cleaner = module.Cleaner


class PathSafetyTests(unittest.TestCase):
    def setUp(self):
        self.cleaner = Cleaner()

    def test_author_id_cannot_escape_folder(self):
        name = self.cleaner.filter_name("../../private\\secrets")
        self.assertNotIn("/", name)
        self.assertNotIn("\\", name)
        self.assertNotIn("..", name)
        self.assertTrue(name)

    def test_fallback_is_also_sanitized(self):
        name = self.cleaner.filter_name("", default="../../outside\\file")
        self.assertNotIn("/", name)
        self.assertNotIn("\\", name)
        self.assertNotIn("..", name)
        self.assertTrue(name)

    def test_custom_rule_cannot_restore_separator(self):
        self.cleaner.set_rule({"x": "../"})
        self.assertEqual(self.cleaner.filter_name("xname"), "name")

    def test_repeated_dots_are_collapsed(self):
        self.assertEqual(self.cleaner.filter_name("a....b"), "a.b")


if __name__ == "__main__":
    unittest.main()
