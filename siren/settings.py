# -*- coding: utf-8 -*-
#
# Read more at:
# https://www.starlette.io/config/

from starlette.config import Config


config = Config("./instance/.env")

DEBUG = config("DEBUG", cast=bool, default=False)
TESTING = config("TESTING", cast=bool, default=False)

DATABASE_PATH = config("DATABASE_PATH", cast=str, default="siren.db")

TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID", cast=str)
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN", cast=str)

SIREN_SMTP_HOST = config("SIREN_SMTP_HOST", cast=str)
SIREN_SMTP_PORT = config("SIREN_SMTP_PORT", cast=int)
SIREN_SMTP_USERNAME = config("SIREN_SMTP_USERNAME", cast=str)
SIREN_SMTP_PASSWORD = config("SIREN_SMTP_PASSWORD", cast=str)
