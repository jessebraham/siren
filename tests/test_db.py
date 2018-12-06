# -*- coding: utf-8 -*-

import pytest

from peewee import SqliteDatabase

from siren.db import Message, User


MODELS = [Message, User]


# Use an in-memory SQLite database for tests
@pytest.fixture
def test_database():
    test_db = SqliteDatabase(":memory:")
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables(MODELS)
    return test_db


def test_user_create(test_database):
    User.create("root", "toor")
    user = User.select().where(User.username == "root").get()
    assert user is not None
    assert user.username == "root"


def test_user_create_existing(test_database):
    User.create("hjfarnsworth", "pazuzu3")
    with pytest.raises(Exception):
        User.create("hjfarnsworth", "pazuzu3")


def test_user_authenticate(test_database):
    User.create("troy_mcclure", "earwigs,ew!")
    assert User.authenticate("troy_mcclure", "earwigs,ew!")
    assert not User.authenticate("troy_mcclure", "wrong-password")
    assert not User.authenticate("", "")


def test_user_lock_unlock(test_database):
    user = User.create("admin", "password")

    user.lock()
    assert user.locked is True
    assert user.locked_on is not None

    user.unlock()
    assert user.locked is False
    assert user.locked_on is None


def test_user_repr(test_database):
    user = User.create("root", "toor")
    assert user.__repr__() == "<User username='root'>"


def test_message_create(test_database):
    user = User.create("hjfarnsworth", "pazuzu3")
    message = Message.create(user, "sms", "+12225551234", "+12225555678")
    assert message is not None
    assert message.user == user
    assert message.message_type == "sms"


def test_message_repr(test_database):
    user = User.create("troy_mcclure", "earwigs,ew!")
    message = Message.create(user, "sms", "+12225551234", "+12225555678")
    assert (
        message.__repr__()
        == "<Message type='sms' from='+12225551234' to='+12225555678'>"
    )
