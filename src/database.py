"""
Database class 
Data struct in docs/db_struct.md
"""
from datetime import datetime, timedelta
from typing import Optional

import os
import aiosqlite

from src.dataclasses import User
from src.logger import Logger


db_log = Logger("db_log", "log/db.log")


@db_log.class_log
class DataBase:
    """DataBase class to work with telegram database"""

    def __init__(self, database_path: str = ":memory:"):
        """init DataBase class"""
        self.database_path: str = database_path
        self.develop: bool = True
        self.conn: aiosqlite.Connection

    @classmethod
    async def init(cls, database_path: str = ":memory:", test_data: bool = False):
        """init async client"""
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
        """clode Connection with database"""
        if self.conn:
            await self.conn.close()

    @classmethod
    async def _read_init_text(cls) -> str:
        """get init script for data"""
        with open("db_requests/init_db.sql", "r", encoding="utf-8") as init_db_req:
            return init_db_req.read()

    async def _init_data(self):
        """init data"""
        async with self.conn.cursor() as cursor:
            init_req = await DataBase._read_init_text()
            await cursor.executescript(init_req)

    async def _delete_data(self):
        """dalete data from database"""
        # TODO:
        pass

    async def _init_test_data(self):
        """init test data"""
        # TODO:
        pass

    # >>>>>>>>> user

    async def user_reg(self, tg_id: int, name: str, on_the_party: bool = False) -> bool:
        """user registration"""

        # checking for availability in the database
        if await self.get_user(tg_id):
            return True

        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO Users(telegram_id, name, on_the_party) VALUES(?, ?, ?)",
                (tg_id, name, on_the_party),
            )

        return True

    async def get_user(self, tg_id: int) -> Optional[User]:
        """get user from data base"""
        async with self.conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM Users WHERE telegram_id = ?", (tg_id,))
            result = await cursor.fetchone()

        if result is None:
            return None

        return User(*result)

    async def user_out(self, tg_id: int):
        """marks the user who left the party"""
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE Users SET on_the_party = 0 WHERE telegram_id = ?", (tg_id,)
            )

    async def user_in(self, tg_id: int):
        """marks the user who came to the party"""
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "UPDATE Users SET on_the_party = 1 WHERE telegram_id = ?", (tg_id,)
            )

    async def block_user(self, tg_id: int, delta: timedelta = timedelta(minutes=5)):
        """blocks the user"""
        duration_in_seconds = int(delta.total_seconds())  # Convert timedelta to seconds
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO Block(user_id, start, block_duration) VALUES (?, ?, ?)",
                (tg_id, datetime.now(), duration_in_seconds),
            )

    async def delete_block(self, tg_id: int):
        """removes the user's lock"""
        async with self.conn.cursor() as cursor:
            await cursor.execute("DELETE FROM Block WHERE user_id = ?", (tg_id,))

    async def is_block(self, tg_id: int):
        """checks if the user is blocked"""
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                "SELECT start, block_duration FROM Block WHERE user_id = ?", (tg_id,)
            )
            block = await cursor.fetchone()

            if block is None:
                return False

            start_time, duration_in_seconds = block

            # Convert the duration from string to integer if necessary
            if isinstance(duration_in_seconds, str):
                duration_in_seconds = int(duration_in_seconds)

            start_time = (
                datetime.fromisoformat(start_time)
                if isinstance(start_time, str)
                else start_time
            )

            duration = timedelta(seconds=duration_in_seconds)
            end_time = start_time + duration

            if datetime.now() >= end_time:
                await self.delete_block(tg_id)
                return False
            return True
