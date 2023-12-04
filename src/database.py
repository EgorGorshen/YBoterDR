"""
Database class 
Data struct in docs/db_struct.md
"""
from datetime import datetime, timedelta
from typing import Optional
import os
import sqlite3

from src.dataclasses import Track, User
from src.logger import Logger

db_log = Logger("db_log", "log/db.log")


@db_log.class_log
class DataBase:
    """DataBase class to work with a telegram database using sqlite3."""

    def __init__(self, database_path: str = ":memory:"):
        """init DataBase class"""
        self.database_path: str = database_path
        self.develop: bool = True
        self.conn: sqlite3.Connection = sqlite3.connect(database_path)
        if self.develop:
            if os.path.exists(database_path):
                self._delete_data()
            self._init_data()

    def close(self):
        """Close connection with the database."""
        if self.conn:
            self.conn.close()

    @staticmethod
    def _read_init_text() -> str:
        """Get init script for the database."""
        with open("db_requests/init_db.sql", "r", encoding="utf-8") as init_db_req:
            return init_db_req.read()

    def _init_data(self):
        """Initialize the database with the schema."""
        init_req = DataBase._read_init_text()
        self.conn.executescript(init_req)
        self.conn.commit()

    def _delete_data(self):
        """Delete data from the database."""
        # List of tables to be dropped
        tables = [
            "Users",
            "Block",
            "Media",
            "Gifts",
            "Tracks",
            "Meal",
            "Likes",
        ]  # Add or modify according to your database schema

        cursor = self.conn.cursor()
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
        self.conn.commit()

    # >>>>>>>>> user

    def user_reg(self, tg_id: int, name: str, on_the_party: bool = False) -> bool:
        """Register a user."""
        if self.get_user(tg_id):
            return True
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO Users(telegram_id, name, on_the_party) VALUES(?, ?, ?)",
            (tg_id, name, on_the_party),
        )
        self.conn.commit()
        return True

    def get_user(self, tg_id: int) -> Optional[User]:
        """Get a user from the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE telegram_id = ?", (tg_id,))
        result = cursor.fetchone()
        return User(*result) if result else None

    def user_out(self, tg_id: int):
        """Marks the user who left the party."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE Users SET on_the_party = 0 WHERE telegram_id = ?", (tg_id,)
        )
        self.conn.commit()

    def user_in(self, tg_id: int):
        """Marks the user who came to the party."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE Users SET on_the_party = 1 WHERE telegram_id = ?", (tg_id,)
        )
        self.conn.commit()

    def block_user(self, tg_id: int, delta: timedelta = timedelta(minutes=5)):
        """Blocks the user."""
        duration_in_seconds = int(delta.total_seconds())  # Convert timedelta to seconds
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO Block(user_id, start, block_duration) VALUES (?, ?, ?)",
            (tg_id, datetime.now(), duration_in_seconds),
        )
        self.conn.commit()

    def delete_block(self, tg_id: int):
        """Removes the user's lock."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Block WHERE user_id = ?", (tg_id,))
        self.conn.commit()

    def is_block(self, tg_id: int) -> bool:
        """Checks if the user is blocked."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT start, block_duration FROM Block WHERE user_id = ?", (tg_id,)
        )
        block = cursor.fetchone()
        if block is None:
            return False

        start_time, duration_in_seconds = block

        # Convert the duration from string to integer if necessary
        if isinstance(duration_in_seconds, str):
            duration_in_seconds = int(duration_in_seconds)

        # Convert start_time to a datetime object, including microseconds
        if isinstance(start_time, str):
            # Adjust the format to include microseconds
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")

        end_time = start_time + timedelta(seconds=duration_in_seconds)

        if datetime.now() >= end_time:
            self.delete_block(tg_id)
            return False
        return True

    # >>>>>>>>> tracks
    def add_track(self, track_id: int, name: str, author: str):
        """add track to db"""
        track = self.get_track(track_id)

        # check out if treck exists
        cursor = self.conn.cursor()

        if track is not None:
            cursor.execute(
                "UPDATE Tracks SET number_of_calls = ? WHERE id = ?",
                (track.number_of_calls + 1, track.track_id),
            )
            # TODO: set on the queue
            self.conn.commit()
            return

        cursor.execute(
            "INSERT INTO Tracks(id, name, author, number_of_calls) VALUES(?, ?, ?, ?)",
            (track_id, name, author, 1),
        )
        self.conn.commit()

    def get_track(self, track_id: int) -> Track | None:
        """get track from database"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM Tracks WHERE id = ?",
            (track_id,),
        )

        track = cursor.fetchone()

        if track is None:
            return None

        return Track(*track)
