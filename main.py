from asyncio import run
from asyncio.exceptions import CancelledError
from contextlib import suppress
from sys import argv

from source import Settings
from source import XHS
from source import XHSDownloader
from source import cli


async def app():
    async with XHSDownloader() as xhs:
        await xhs.run_async()


async def api_server(
    host="0.0.0.0",
    port=5556,
    log_level="info",
):
    async with XHS(**Settings().run()) as xhs:
        await xhs.run_api_server(
            host,
            port,
            log_level,
        )


async def mcp_server(
    transport="streamable-http",
    host="0.0.0.0",
    port=5556,
    log_level="INFO",
):
    async with XHS(**Settings().run()) as xhs:
        await xhs.run_mcp_server(
            transport=transport,
            host=host,
            port=port,
            log_level=log_level,
        )


if __name__ == "__main__":
    with suppress(
        KeyboardInterrupt,
        CancelledError,
    ):
        # TODO: 重构优化
        if len(argv) == 1:
            run(app())
        elif argv[1].upper() == "API":
            run(api_server())
        elif argv[1].upper() == "MCP":
            run(mcp_server())
            # run(mcp_server("stdio"))
        else:
            cli()
