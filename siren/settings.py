"""
Load the application's configuration. To set these values in a configuration
file first create './instance/env'. Values can be set by creating environment
variables with names matching those specified in this file.

eg.)    DEBUG=False

        TWILIO_ACCOUNT_SID="foo"
        TWILIO_AUTH_TOKEN="bar"
        TWILIO_FROM_NUMBER="+12223334444"

Read more at:
https://www.starlette.io/config/
"""

import pathlib

from starlette.config import Config

# The application's root and 'instance' directories. Most paths should be
# relative to `INSTANCE_DIR`.
BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()
INSTANCE_DIR = BASE_DIR / "instance"


# Config will be read from environment variables and/or '.env' files.
config = Config(INSTANCE_DIR / ".env")

# Production and Testing modes must be explicitly set if desired.
DEBUG = config("DEBUG", cast=bool, default=True)
TESTING = config("TESTING", cast=bool, default=False)

# SQLite is currently the only supported database. Paths are assumed to be
# relative to the application's root directory if configured in '.env'.
DATABASE_PATH = config(
    "DATABASE_PATH", cast=str, default=INSTANCE_DIR / "siren.db"
)

# Twilio API configuration. If *ALL* values have not been set, SMS
# capabilities are disabled.
TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID", cast=str, default="")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN", cast=str, default="")
TWILIO_FROM_NUMBER = config("TWILIO_FROM_NUMBER", cast=str, default="")

# Email configuration. If *ALL* values have not been set, email capabilities
# are disabled.
SIREN_SMTP_HOST = config("SIREN_SMTP_HOST", cast=str, default="")
SIREN_SMTP_PORT = config("SIREN_SMTP_PORT", cast=int, default=0)
SIREN_SMTP_USERNAME = config("SIREN_SMTP_USERNAME", cast=str, default="")
SIREN_SMTP_PASSWORD = config("SIREN_SMTP_PASSWORD", cast=str, default="")
SIREN_SMTP_FROM_ADDR = config("SIREN_SMTP_FROM_ADDR", cast=str, default="")

# Our messaging configuration can have a little structure, as a treat.
siren_config = {
    "email": {
        "host": SIREN_SMTP_HOST,
        "port": SIREN_SMTP_PORT,
        "username": SIREN_SMTP_USERNAME,
        "password": SIREN_SMTP_PASSWORD,
        "from_addr": SIREN_SMTP_FROM_ADDR,
    },
    "sms": {
        "account_sid": TWILIO_ACCOUNT_SID,
        "auth_token": TWILIO_AUTH_TOKEN,
        "from_number": TWILIO_FROM_NUMBER,
    },
}
