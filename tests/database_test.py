import pytest_asyncio
from src import database
from src.dataclasses import User
from src.database import DataBase


@pytest_asyncio.fixture()
async def db_connection():
    data = await DataBase.init()
    yield data
    await data.close()


async def test_user_reg(db_connection):
    # Test the user registration
    result = await db_connection.user_reg(tg_id=1, name="Вован")
    assert result is True

    # Verify if the user is actually registered
    user = await db_connection.get_user(tg_id=1)
    assert user is not None
    assert user.telegram_id == 1
    assert user.name == "Вован"


async def test_get_user(db_connection):
    # Register a user first
    await db_connection.user_reg(tg_id=2, name="Анна")

    # Test retrieval of the registered user
    user = await db_connection.get_user(tg_id=2)
    assert user is not None
    assert user.telegram_id == 2
    assert user.name == "Анна"


async def test_user_in(db_connection: DataBase):
    await db_connection.user_reg(tg_id=3, name="Петя")

    # >>>> check in res
    await db_connection.user_in(3)

    user = await db_connection.get_user(3)

    assert user is not None
    assert user.on_the_party == True


async def test_user_out(db_connection: DataBase):
    await db_connection.user_reg(tg_id=4, name="Петяфил", on_the_party=True)

    # >>>> check in res
    await db_connection.user_out(4)

    user = await db_connection.get_user(3)

    assert user is not None
    assert user.on_the_party == False


# async def test_user_out(db_connection):
#     pass
#
#
# async def test_user_in(db_connection):
#     pass
