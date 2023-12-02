from dataclasses import dataclass
from datetime import time
import aiosqlite, os


from dataclasses import dataclass
from typing import Optional

from src.dataclasses import User


class DataBase:
    def __init__(self, database_path: str = ":memory:"):
        self.database_path: str = database_path
        self.develop: bool = True
        self.conn: aiosqlite.Connection

    @classmethod
    async def init(cls, database_path: str = ":memory:", test_data: bool = False):
        instance = cls()
        instance.conn = await aiosqlite.connect(database_path)

        if instance.develop:
            if os.path.exists(database_path):
                await instance._delete_data()
            await instance._init_data()

            if test_data:
                await instance._init_test_data()
        return instance

    async def close(self):
        if self.conn:
            await self.conn.close()

    @classmethod
    async def _read_init_text(cls) -> str:
        with open("db_requests/init_db.sql", "r") as init_db_req:
            return init_db_req.read()

    async def _init_data(self):
        async with self.conn.cursor() as cursor:
            init_req = await DataBase._read_init_text()
            await cursor.executescript(init_req)

    async def _delete_data(self):
        pass

    async def _init_test_data(self):
        pass

    # >>>>>>>>> user

    async def user_reg(self, tg_id: int, name: str, on_the_party: bool = False) -> bool:
        if await self.get_user(tg_id):
            return True

        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO Users(telegram_id, name, on_the_party) VALUES(?, ?, ?)",
                (tg_id, name, on_the_party),
            )

        return True

    async def get_user(self, tg_id: int) -> Optional[User]:
        async with self.conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM Users WHERE telegram_id = ?", (tg_id,))
            result = await cursor.fetchone()

        if result is None:
            return None

        return User(*result)

    async def user_out(self, tg_id: int):
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE Users SET on_the_party = 0 WHERE telegram_id = ?", (tg_id,)
            )

    async def user_in(self, tg_id: int):
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE Users SET on_the_party = 1 WHERE telegram_id = ?", (tg_id,)
            )

    async def block_user(self, tg_id: int, delta: time):
        pass
