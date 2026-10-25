import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TLSVerificationTests(unittest.TestCase):
    def test_http_clients_do_not_disable_certificate_verification(self):
        for relative_path in (
            "source/module/manager.py",
            "source/application/request.py",
        ):
            with self.subTest(file=relative_path):
                tree = ast.parse((ROOT / relative_path).read_text(encoding="utf-8"))
                for call in (node for node in ast.walk(tree) if isinstance(node, ast.Call)):
                    if not isinstance(call.func, ast.Name):
                        continue
                    if call.func.id not in {"AsyncSession", "get"}:
                        continue
                    for keyword in call.keywords:
                        self.assertFalse(
                            keyword.arg == "verify"
                            and isinstance(keyword.value, ast.Constant)
                            and keyword.value.value is False,
                            f"{relative_path} disables TLS certificate verification",
                        )


if __name__ == "__main__":
    unittest.main()
