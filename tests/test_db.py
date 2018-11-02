# -*- coding: utf-8 -*-

import pytest

from peewee import SqliteDatabase

from siren.db import User


MODELS = [User]


# use an in-memory SQLite for tests.
@pytest.fixture
def test_database():
    test_db = SqliteDatabase(":memory:")
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables(MODELS)
    return test_db


def test_user_create(test_database):
    User.create(username="test", password="password")
    user = User.select().where(User.username == "test").get()
    assert user is not None
    assert user.username == "test"


def test_user_create_existing(test_database):
    User.create(username="test", password="password")
    with pytest.raises(Exception):
        User.create(username="test", password="password")


def test_user_authenticate(test_database):
    User.create(username="test", password="password")
    assert User.authenticate("test", "password")
    assert not User.authenticate("test", "wrong-password")
    assert not User.authenticate("", "")


def test_user_repr(test_database):
    user = User.create(username="test", password="password")
    assert user.__repr__() == "<User username='test'>"
