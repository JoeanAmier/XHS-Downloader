from asyncio import CancelledError, Queue, QueueFull, create_task
from contextlib import suppress
from json import JSONDecodeError, loads
from typing import TYPE_CHECKING

from websockets import ConnectionClosed, serve
from websockets.typing import Origin

if TYPE_CHECKING:
    from ..application import XHS


class ScriptServer:
    ORIGINS = (
        Origin("https://www.xiaohongshu.com"),
        Origin("https://www.rednote.com"),
    )

    def __init__(
        self,
        core: "XHS",
        host="127.0.0.1",
        port=5558,
    ):
        self.core = core
        self.host = host
        self.port = port
        self.server = None
        self.queue = Queue(maxsize=100)
        self.worker = None

    async def handler(self, websocket):
        with suppress(ConnectionClosed):
            async for message in websocket:
                try:
                    task = loads(message)
                except (JSONDecodeError, TypeError):
                    continue
                if not (
                    isinstance(task, dict)
                    and set(task) == {"data", "index"}
                    and isinstance(task["data"], dict)
                    and (task["index"] is None or isinstance(task["index"], list))
                ):
                    continue
                try:
                    self.queue.put_nowait(task)
                except QueueFull:
                    await websocket.close(code=1008, reason="Task queue is full")
                    return

    async def worker_loop(self):
        while True:
            task = await self.queue.get()
            try:
                await self.core.process_script_task(**task)
            except Exception as exc:
                self.core.logging(f"Script task failed: {exc}")
            finally:
                self.queue.task_done()

    async def start(self):
        """启动服务器"""
        self.server = await serve(
            self.handler,
            self.host,
            self.port,
            origins=self.ORIGINS,
            max_size=1024 * 1024,
        )
        self.worker = create_task(self.worker_loop())

    async def stop(self):
        """停止服务器"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        if self.worker:
            self.worker.cancel()
            with suppress(CancelledError):
                await self.worker

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
