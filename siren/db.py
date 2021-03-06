import datetime
import logging

import bcrypt
from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    Model,
)
from playhouse.sqlite_ext import SqliteExtDatabase

from siren import settings

db = SqliteExtDatabase(
    settings.DATABASE_PATH,
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
    locked = BooleanField(default=False)
    locked_on = DateTimeField(null=True)

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
        return not user.locked and user.verify_password(password)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def verify_password(self, password):
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password.encode("utf-8")
        )

    def lock(self):
        self.locked = True
        self.locked_on = datetime.datetime.utcnow()
        return self.save()

    def unlock(self):
        self.locked = False
        self.locked_on = None
        return self.save()

    def __repr__(self):
        return f"<User username='{self.username}'>"


class Message(BaseModel):
    user = ForeignKeyField(User, backref="messages")
    message_type = CharField(
        max_length=8, index=True, choices=(("email", "email"), ("sms", "sms"))
    )
    sender = CharField(max_length=256)
    recipient = CharField(max_length=256)
    status = CharField(
        max_length=16,
        index=True,
        choices=(("queued", "queued"), ("delivered", "delivered")),
        default="queued",
    )
    queued = DateTimeField(default=datetime.datetime.utcnow)
    delivered = DateTimeField(null=True)
    sid = CharField(max_length=64, null=True)

    @classmethod
    def create(cls, user, message_type, sender, recipient):
        message = cls(
            user=user,
            message_type=message_type,
            sender=sender,
            recipient=recipient,
        )
        message.save()
        return message

    def deliver(self):
        self.status = "delivered"
        self.delivered = datetime.datetime.utcnow()
        self.save()

    def __repr__(self):
        return (
            f"<Message type='{self.message_type}' "
            f"from='{self.sender}' to='{self.recipient}'>"
        )


async def open_database_connection():
    db.connect()
    logger.info("Database connection established.")
    db.create_tables([User, Message])


async def close_database_connection():
    db.close()
    logger.info("Database connection closed.")
