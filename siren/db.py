# -*- coding: utf-8 -*-

import datetime
import logging

import bcrypt

from peewee import CharField, DateTimeField, ForeignKeyField, Model
from playhouse.sqlite_ext import SqliteExtDatabase


# FIXME: set path in a config file
db = SqliteExtDatabase(
    "instance/siren.db",
    pragmas=(
        ("cache_size", -1024 * 64),  # 64MB page-cache
        ("journal_mode", "wal"),  # Use WAL-mode
        ("foreign_keys", 1),  # Enforce FK constraints
    ),
)
logger = logging.getLogger("siren")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(max_length=64, index=True, unique=True)
    password = CharField(max_length=64)
    created = DateTimeField(default=datetime.datetime.utcnow)
    # TODO: add ability to lock and unlock accounts

    @classmethod
    def create(cls, username, password):
        try:
            cls.get(cls.username ** username)
        except cls.DoesNotExist:
            user = cls(username=username)
            user.password = user.hash_password(password)
            user.save()
            return user
        else:
            raise Exception("User with provided username already exists.")

    @classmethod
    def authenticate(cls, username, password):
        try:
            user = cls.get(cls.username ** username)
        except cls.DoesNotExist:
            return False
        return user.verify_password(password)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def verify_password(self, password):
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password.encode("utf-8")
        )

    def __repr__(self):
        return f"<User username='{self.username}'>"


class Message(BaseModel):
    user = ForeignKeyField(User, backref="messages")
    timestamp = DateTimeField(default=datetime.datetime.utcnow)
    message_type = CharField(
        max_length=8, index=True, choices=(("email", "email"), ("sms", "sms"))
    )
    sender = CharField(max_length=256)
    recipient = CharField(max_length=256)
    sid = CharField(max_length=64, default="")

    @classmethod
    def create(cls, user, message_type, sender, recipient, sid=None):
        message = Message(
            user=user,
            message_type=message_type,
            sender=sender,
            recipient=recipient,
            sid=sid,
        )
        message.save()
        return message

    def __repr__(self):
        return f"<Message from='{self.sender}' to='{self.recipient}'>"


async def open_database_connection():
    db.connect()
    logger.info("Database connection established.")
    db.create_tables([User, Message])


async def close_database_connection():
    db.close()
    logger.info("Database connection closed.")
