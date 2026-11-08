import importlib.util
import unittest
from pathlib import Path

from pydantic import ValidationError


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("xhs_models", ROOT / "source/module/model.py")
MODELS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODELS)


class ApiSecurityTests(unittest.TestCase):
    def test_request_cannot_supply_proxy(self):
        with self.assertRaises(ValidationError):
            MODELS.ExtractParams(url="https://www.xiaohongshu.com/explore/test", proxy="http://127.0.0.1:8080")

    def test_supported_request_fields_remain_available(self):
        params = MODELS.ExtractParams(url="https://www.xiaohongshu.com/explore/test", download=True)
        self.assertTrue(params.download)
        self.assertFalse(hasattr(params, "proxy"))


if __name__ == "__main__":
    unittest.main()
