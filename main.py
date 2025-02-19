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


async def server(
        host="0.0.0.0",
        port=6666,
        log_level="info",
):
    async with XHS(**Settings().run()) as xhs:
        await xhs.run_server(
            host,
            port,
            log_level,
        )


if __name__ == "__main__":
    with suppress(
            KeyboardInterrupt,
            CancelledError,
    ):
        if len(argv) == 1:
            run(app())
        elif argv[1] == "server":
            run(server())
        else:
            cli()
