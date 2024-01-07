# Assuming src.dataclasses contains a User class which is used by the DataBase class
import pytest
from faker import Faker

from src.database import DataBase


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


def test_add_and_get_track_twice(connection: DataBase, faker_data: Faker):
    """Test for adding and getting the same track twice."""
    # Generate fake data
    name = faker_data.name()
    track_id = faker_data.random_int(min=0)
    author = faker_data.name()

    # First addition of the track
    connection.add_track(track_id, name, author)
    first_retrieval = connection.get_track(track_id)
    assert (
        first_retrieval is not None
    ), "Track should be found in the database after first addition"
    assert first_retrieval.author == author, "Author should match after first addition"
    assert first_retrieval.name == name, "Name should match after first addition"
    assert (
        first_retrieval.number_of_calls == 1
    ), "Number of calls should be 1 after first addition"

    # Second addition of the same track
    connection.add_track(track_id, name, author)
    second_retrieval = connection.get_track(track_id)
    assert (
        second_retrieval is not None
    ), "Track should be found in the database after second addition"
    assert (
        second_retrieval.author == author
    ), "Author should match after second addition"
    assert second_retrieval.name == name, "Name should match after second addition"
    assert (
        second_retrieval.number_of_calls == 2
    ), "Number of calls should be incremented to 2 after second addition"
