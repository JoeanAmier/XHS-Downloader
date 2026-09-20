from asyncio import CancelledError, Queue, create_task
from contextlib import suppress
from json import dumps, loads
from typing import TYPE_CHECKING

from websockets import ConnectionClosed, serve
from websockets.typing import Origin

from ..translation import _
from .auth import verify_auth_token

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
        host="0.0.0.0",
        port=5558,
    ):
        self.core = core
        self.host = host
        self.port = port
        self.server = None
        self.queue = Queue()
        self.worker = None

    async def handler(self, websocket):
        with suppress(ConnectionClosed):
            async for message in websocket:
                try:
                    data = loads(message)
                except (TypeError, ValueError):
                    await websocket.send(
                        dumps({"status": "error", "message": _("非法数据")})
                    )
                    continue
                if not isinstance(data, dict):
                    await websocket.send(
                        dumps({"status": "error", "message": _("非法数据")})
                    )
                    continue
                if not verify_auth_token(data.pop("auth_token", None)):
                    await websocket.send(
                        dumps(
                            {
                                "status": "error",
                                "message": _("鉴权令牌无效或已过期"),
                            }
                        )
                    )
                    continue
                self.queue.put_nowait(data)
                await websocket.send(
                    dumps(
                        {
                            "status": "accepted",
                            "message": _("下载任务已接收"),
                        }
                    )
                )

    async def worker_loop(self):
        while True:
            await self.core.process_script_task(**await self.queue.get())

    async def start(self):
        """启动服务器"""
        self.server = await serve(
            self.handler,
            self.host,
            self.port,
            origins=self.ORIGINS,
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
