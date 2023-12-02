import pytest_asyncio
from faker import Faker
from src.database import DataBase

# Assuming src.dataclasses contains a User class which is used by the DataBase class


@pytest_asyncio.fixture()
async def db_connection():
    # Initialize the database connection
    data = await DataBase.init()
    yield data
    # Close the database connection after the test
    await data.close()


@pytest_asyncio.fixture()
async def faker_data():
    # Create a Faker instance
    faker = Faker()
    return faker


async def test_user_reg(db_connection: DataBase, faker_data: Faker):
    # Generate a random Telegram ID and name
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    # Test the user registration
    result = await db_connection.user_reg(tg_id=tg_id, name=name)
    assert result is True

    # Verify if the user is actually registered
    user = await db_connection.get_user(tg_id=tg_id)
    assert user is not None
    assert user.telegram_id == tg_id
    assert user.name == name


async def test_get_user(db_connection: DataBase, faker_data: Faker):
    # Generate a random Telegram ID and name
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    # Register a user first
    await db_connection.user_reg(tg_id=tg_id, name=name)

    # Test retrieval of the registered user
    user = await db_connection.get_user(tg_id=tg_id)
    assert user is not None
    assert user.telegram_id == tg_id
    assert user.name == name


async def test_user_in(db_connection: DataBase, faker_data: Faker):
    # Generate a random Telegram ID and name
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    # Register a user and check them in
    await db_connection.user_reg(tg_id=tg_id, name=name)
    await db_connection.user_in(tg_id)

    # Verify the user's status
    user = await db_connection.get_user(tg_id)
    assert user is not None
    assert user.on_the_party == True


async def test_user_out(db_connection: DataBase, faker_data: Faker):
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    await db_connection.user_reg(tg_id=tg_id, name=name, on_the_party=True)
    await db_connection.user_out(tg_id)

    user = await db_connection.get_user(tg_id)
    assert user is not None
    assert user.on_the_party == False
