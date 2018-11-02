# -*- coding: utf-8 -*-

import datetime
import logging

import bcrypt

from peewee import CharField, DateTimeField, Model, SqliteDatabase


db = SqliteDatabase("instance/siren.db")  # FIXME: set path in a config file
logger = logging.getLogger("siren")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(max_length=256, unique=True)
    password = CharField(max_length=64)
    created = DateTimeField(default=datetime.datetime.utcnow)

    @classmethod
    def create(cls, username, password):
        try:
            cls.select().where(cls.username ** username).get()
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
            user = cls.select().where(cls.username ** username).get()
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


async def open_database_connection():
    db.connect()
    logger.info("Database connection established.")
    db.create_tables([User])


async def close_database_connection():
    db.close()
    logger.info("Database connection closed.")
