import pytest
from faker import Faker
from peewee import SqliteDatabase

from siren.db import Message, User

fake = Faker()


# Use an in-memory SQLite database for tests
@pytest.fixture
def test_database():
    test_db = SqliteDatabase(":memory:")
    test_db.bind([Message, User], bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables([Message, User])
    return test_db


def test_user_create(test_database):
    username = fake.user_name()
    password = fake.password()

    User.create(username, password)
    user = User.select().where(User.username == username).get()

    assert user is not None
    assert user.username == username


def test_user_create_existing(test_database):
    username = fake.user_name()
    password = fake.password()

    User.create(username, password)
    with pytest.raises(Exception):
        User.create(username, password)


def test_user_authenticate(test_database):
    username = fake.user_name()
    password = fake.password()

    User.create(username, password)

    assert User.authenticate(username, password)
    assert not User.authenticate(username, fake.password())
    assert not User.authenticate(fake.user_name(), fake.password())


def test_user_lock_unlock(test_database):
    user = User.create(fake.user_name(), fake.password())

    user.lock()
    assert user.locked is True
    assert user.locked_on is not None

    user.unlock()
    assert user.locked is False
    assert user.locked_on is None


def test_user_repr(test_database):
    username = fake.user_name()
    user = User.create(username, fake.password())

    assert user.__repr__() == f"<User username='{username}'>"


def test_message_create(test_database):
    user = User.create(fake.user_name(), fake.password())
    message = Message.create(user, "sms", "+12225551234", "+12225555678")

    assert message is not None
    assert message.user == user
    assert message.message_type == "sms"


def test_message_deliver(test_database):
    user = User.create(fake.user_name(), fake.password())
    message = Message.create(user, "sms", "+12225551234", "+12225555678")
    assert message.status == "queued"

    message.deliver()

    assert message.status == "delivered"
    assert message.delivered is not None


def test_message_repr(test_database):
    user = User.create(fake.user_name(), fake.password())
    message = Message.create(user, "sms", "+12225551234", "+12225555678")

    assert (
        message.__repr__()
        == "<Message type='sms' from='+12225551234' to='+12225555678'>"
    )
