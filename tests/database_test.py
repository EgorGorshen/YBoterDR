# Assuming src.dataclasses contains a User class which is used by the DataBase class
import pytest
from faker import Faker
from src.database import DataBase
from src.dataclasses import Track


@pytest.fixture(name="connection")
def db_connection():
    """Get db connection"""
    # Initialize the database connection
    data = DataBase()
    yield data
    # Close the database connection after the test
    data.close()


@pytest.fixture(name="faker_data")
def init_faker():
    """Init fake data maker"""
    # Create a Faker instance
    faker = Faker()
    return faker


def test_user_reg(connection: DataBase, faker_data: Faker):
    """testing user registration"""
    # Generate a random Telegram ID and name
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    # Test the user registration
    result = connection.user_reg(tg_id=tg_id, name=name)
    assert result is True

    # Verify if the user is actually registered
    user = connection.get_user(tg_id=tg_id)
    assert user is not None
    assert user.telegram_id == tg_id
    assert user.name == name


def test_get_user(connection: DataBase, faker_data: Faker):
    """a test function for obtaining user information"""
    # Generate a random Telegram ID and name
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    # Register a user first
    connection.user_reg(tg_id=tg_id, name=name)

    # Test retrieval of the registered user
    user = connection.get_user(tg_id=tg_id)
    assert user is not None
    assert user.telegram_id == tg_id
    assert user.name == name


def test_user_in(connection: DataBase, faker_data: Faker):
    """A function test to identify the user as having come the party"""
    # Generate a random Telegram ID and name
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    # Register a user and check them in
    connection.user_reg(tg_id=tg_id, name=name)
    connection.user_in(tg_id)

    # Verify the user's status
    user = connection.get_user(tg_id)
    assert user is not None
    assert bool(user.on_the_party) is True


def test_user_out(connection: DataBase, faker_data: Faker):
    """A function test to identify the user as having left the party"""
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    connection.user_reg(tg_id=tg_id, name=name, on_the_party=True)
    connection.user_out(tg_id)

    user = connection.get_user(tg_id)
    assert user is not None
    assert bool(user.on_the_party) is False


def test_block_user(connection: DataBase, faker_data: Faker):
    """Test for blocking a user"""
    tg_id = faker_data.random_int(min=1)
    name = faker_data.name()

    connection.user_reg(tg_id=tg_id, name=name, on_the_party=True)
    connection.block_user(tg_id=tg_id)

    assert connection.is_block(tg_id=tg_id)


def test_add_and_get_track(connection: DataBase, faker_data: Faker):
    """Test for add and get track func"""
    name = faker_data.name()
    author = faker_data.name()
    returner = Track(0, name, author)

    connection.add_track(name, author)

    get_track = connection.get_track(name, author)
    assert get_track is not None
    assert returner.author == get_track.author
    assert returner.name == get_track.name
