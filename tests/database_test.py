# Assuming src.dataclasses contains a User class which is used by the DataBase class

import pytest_asyncio
from faker import Faker
from src.database import DataBase


@pytest_asyncio.fixture(name="connection")
async def db_connection():
    """Get db connection"""
    # Initialize the database connection
    data = await DataBase.init()
    yield data
    # Close the database connection after the test
    await data.close()


@pytest_asyncio.fixture(name="faker_data")
async def init_faker():
    """Init fake data maker"""
    # Create a Faker instance
    faker = Faker()
    return faker


async def test_user_reg(connection: DataBase, faker_data: Faker):
    """testing user registration"""
    # Generate a random Telegram ID and name
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    # Test the user registration
    result = await connection.user_reg(tg_id=tg_id, name=name)
    assert result is True

    # Verify if the user is actually registered
    user = await connection.get_user(tg_id=tg_id)
    assert user is not None
    assert user.telegram_id == tg_id
    assert user.name == name


async def test_get_user(connection: DataBase, faker_data: Faker):
    """a test function for obtaining user information"""
    # Generate a random Telegram ID and name
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    # Register a user first
    await connection.user_reg(tg_id=tg_id, name=name)

    # Test retrieval of the registered user
    user = await connection.get_user(tg_id=tg_id)
    assert user is not None
    assert user.telegram_id == tg_id
    assert user.name == name


async def test_user_in(connection: DataBase, faker_data: Faker):
    """A function test to identify the user as having come the party"""
    # Generate a random Telegram ID and name
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    # Register a user and check them in
    await connection.user_reg(tg_id=tg_id, name=name)
    await connection.user_in(tg_id)

    # Verify the user's status
    user = await connection.get_user(tg_id)
    assert user is not None
    assert bool(user.on_the_party) is True


async def test_user_out(connection: DataBase, faker_data: Faker):
    """A function test to identify the user as having left the party"""
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    await connection.user_reg(tg_id=tg_id, name=name, on_the_party=True)
    await connection.user_out(tg_id)

    user = await connection.get_user(tg_id)
    assert user is not None
    assert bool(user.on_the_party) is False


async def test_block_user(connection: DataBase, faker_data: Faker):
    """тест на блокировку пользователя"""
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    await connection.user_reg(tg_id=tg_id, name=name, on_the_party=True)
    await connection.block_user(tg_id=tg_id)

    assert await connection.is_block(tg_id=tg_id)
