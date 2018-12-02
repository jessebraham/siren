# -*- coding: utf-8 -*-

import datetime
import os
import smtplib

from email.message import EmailMessage

from twilio.rest import Client


class EmailDispatcher:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def send(self, user, msg, to_addr, from_addr, subject, body):
        with smtplib.SMTP(self.host, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.username, self.password)
            message = smtp.send_message(
                self.construct_email(to_addr, from_addr, subject, body)
            )

        msg.status = "delivered"
        msg.delivered = datetime.datetime.utcnow()
        msg.save()

        return message

    def construct_email(self, to_addr, from_addr, subject, body):
        message = EmailMessage()
        message["To"] = to_addr
        message["From"] = from_addr
        message["Subject"] = subject
        message.set_content(body)
        return message


class SmsDispatcher:
    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(account_sid, auth_token)

    def send(self, user, msg, to_addr, from_addr, body):
        message = self.client.messages.create(
            to=to_addr, from_=from_addr, body=body
        )

        msg.status = "delivered"
        msg.delivered = datetime.datetime.utcnow()
        msg.sid = message.sid
        msg.save()

        return message


# -----------------------------------------------------------------------------
# Background Tasks

config = {
    "email": {
        "host": os.environ.get("SIREN_SMTP_HOST"),
        "port": os.environ.get("SIREN_SMTP_PORT"),
        "username": os.environ.get("SIREN_SMTP_USERNAME"),
        "password": os.environ.get("SIREN_SMTP_PASSWORD"),
    },
    "sms": {
        "account_sid": os.environ.get("TWILIO_ACCOUNT_SID"),
        "auth_token": os.environ.get("TWILIO_AUTH_TOKEN"),
    },
}

email_dispatcher = EmailDispatcher(**config["email"])
sms_dispatcher = SmsDispatcher(**config["sms"])


async def send_email(user, msg, to_addr, from_addr, subject, body):
    return email_dispatcher.send(user, msg, to_addr, from_addr, subject, body)


async def send_sms(user, msg, to_addr, from_addr, body):
    return sms_dispatcher.send(user, msg, to_addr, from_addr, body)
