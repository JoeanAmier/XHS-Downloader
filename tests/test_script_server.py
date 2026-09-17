import asyncio
import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "source/module/script.py"
spec = importlib.util.spec_from_file_location("script_server", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
ScriptServer = module.ScriptServer


class FakeSocket:
    def __init__(self, messages):
        self.messages = messages
        self.closed = None

    def __aiter__(self):
        self.iterator = iter(self.messages)
        return self

    async def __anext__(self):
        try:
            return next(self.iterator)
        except StopIteration:
            raise StopAsyncIteration

    async def close(self, code, reason):
        self.closed = (code, reason)


class ScriptServerTests(unittest.IsolatedAsyncioTestCase):
    async def test_rejects_malformed_tasks(self):
        server = ScriptServer(None)
        socket = FakeSocket(
            ['not-json', '[]', '{"data": {}, "index": null, "extra": 1}',
             '{"data": {}, "index": {}}', '{"data": {}, "index": null}']
        )
        await server.handler(socket)
        self.assertEqual(server.queue.qsize(), 1)
        self.assertEqual(server.queue.get_nowait(), {"data": {}, "index": None})

    async def test_full_queue_closes_connection(self):
        server = ScriptServer(None)
        for _ in range(100):
            server.queue.put_nowait({"data": {}, "index": None})
        socket = FakeSocket(['{"data": {}, "index": null}'])
        await server.handler(socket)
        self.assertEqual(socket.closed[0], 1008)
        self.assertEqual(server.queue.qsize(), 100)

    def test_localhost_default(self):
        self.assertEqual(ScriptServer(None).host, "127.0.0.1")


if __name__ == "__main__":
    unittest.main()
