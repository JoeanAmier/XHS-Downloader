from aiosqlite import connect

from source.module import Manager

__all__ = ["IDRecorder"]


class IDRecorder:
    def __init__(self, manager: Manager):
        self.file = manager.root.joinpath("XHS-Downloader.db")
        self.database = None
        self.cursor = None

    async def __connect_database(self):
        self.database = await connect(self.file)
        self.cursor = await self.database.cursor()
        await self.database.execute("CREATE TABLE IF NOT EXISTS explore_ids (ID TEXT PRIMARY KEY);")
        await self.database.commit()

    async def select(self, id_: str):
        await self.cursor.execute("SELECT ID FROM explore_ids WHERE ID=?", (id_,))
        return await self.cursor.fetchone()

    async def add(self, id_: str) -> None:
        await self.database.execute("REPLACE INTO explore_ids VALUES (?);", (id_,))
        await self.database.commit()

    async def delete(self, id_: str) -> None:
        if id_:
            await self.database.execute("DELETE FROM explore_ids WHERE ID=?", (id_,))
            await self.database.commit()

    async def delete_many(self, ids: list | tuple):
        [await self.delete(i) for i in ids]

    async def all(self):
        await self.cursor.execute("SELECT ID FROM explore_ids")
        return [i[0] for i in await self.cursor.fetchmany()]

    async def __aenter__(self):
        await self.__connect_database()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.cursor.close()
        await self.database.close()
