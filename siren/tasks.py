# -*- coding: utf-8 -*-

import datetime
import smtplib

from email.message import EmailMessage

from twilio.rest import Client

from siren import settings
from siren.db import Message


class EmailDispatcher:
    def __init__(self, host, port, username, password, from_addr):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.from_addr = from_addr

    def send(self, user, to_addr, subject, body):
        with smtplib.SMTP(self.host, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.username, self.password)
            message = smtp.send_message(
                self.construct_email(to_addr, subject, body)
            )

        msg = Message.create(user, "email", self.from_addr, to_addr)
        msg.status = "delivered"
        msg.delivered = datetime.datetime.utcnow()
        msg.save()

        return message

    def construct_email(self, to_addr, subject, body):
        message = EmailMessage()
        message["To"] = to_addr
        message["From"] = self.from_addr
        message["Subject"] = subject
        message.set_content(body)
        return message


class SmsDispatcher:
    def __init__(self, account_sid, auth_token, from_number):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        self.client = Client(account_sid, auth_token)

    def send(self, user, to_addr, body):
        message = self.client.messages.create(
            to=to_addr, from_=self.from_addr, body=body
        )

        msg = Message.create(user, "sms", self.from_number, to_addr)
        msg.status = "delivered"
        msg.delivered = datetime.datetime.utcnow()
        msg.sid = message.sid
        msg.save()

        return message


# -----------------------------------------------------------------------------
# Background Tasks

config = {
    "email": {
        "host": settings.SIREN_SMTP_HOST,
        "port": settings.SIREN_SMTP_PORT,
        "username": settings.SIREN_SMTP_USERNAME,
        "password": settings.SIREN_SMTP_PASSWORD,
        "from_addr": settings.SIREN_SMTP_FROM_ADDR,
    },
    "sms": {
        "account_sid": settings.TWILIO_ACCOUNT_SID,
        "auth_token": settings.TWILIO_AUTH_TOKEN,
        "from_number": settings.TWILIO_FROM_NUMBER,
    },
}

email_dispatcher = EmailDispatcher(**config["email"])
sms_dispatcher = SmsDispatcher(**config["sms"])


async def send_email(user, to_addr, subject, body):
    return email_dispatcher.send(user, to_addr, subject, body)


async def send_sms(user, to_addr, body):
    return sms_dispatcher.send(user, to_addr, body)
