# -*- coding: utf-8 -*-

import os
import smtplib

from email.message import EmailMessage

from twilio.rest import Client

from siren.db import Message


# TODO: replace environment variables with config file
# SMTP host and port values are loaded from the OS's environment.
SMTP_HOST = os.environ.get("SIREN_SMTP_HOST")
SMTP_PORT = os.environ.get("SIREN_SMTP_PORT")
SMTP_USERNAME = os.environ.get("SIREN_SMTP_USERNAME")
SMTP_PASSWORD = os.environ.get("SIREN_SMTP_PASSWORD")

# TODO: replace environment variables with config file
# Twilio "account_sid" and "auth_token" values are loaded from the OS's
# environment. If these aren't present the requests will fail to authenticate.
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")


class EmailDispatcher(object):
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def send(self, user, to_addr, from_addr, subject, body):
        with smtplib.SMTP(self.host, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.username, self.password)
            message = smtp.send_message(
                self.construct_email(to_addr, from_addr, subject, body)
            )
        Message(
            user=user, message_type="email", sender=from_addr, recipient=to_addr
        ).save()
        return message

    def construct_email(self, to_addr, from_addr, subject, body):
        message = EmailMessage()
        message["To"] = to_addr
        message["From"] = from_addr
        message["Subject"] = subject
        message.set_content(body)
        return message


class SmsDispatcher(object):
    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(account_sid, auth_token)

    def send(self, user, to_addr, from_addr, body):
        message = self.client.messages.create(
            to=to_addr, from_=from_addr, body=body
        )
        Message(
            user=user,
            message_type="sms",
            sender=from_addr,
            recipient=to_addr,
            sid=message.sid,
        ).save()
        return message


email_dispatcher = EmailDispatcher(
    SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
)
sms_dispatcher = SmsDispatcher(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# -----------------------------------------------------------------------------
# Background Tasks


async def send_email(user, to_addr, from_addr, subject, body):
    return email_dispatcher.send(user, to_addr, from_addr, subject, body)


async def send_sms(user, to_addr, from_addr, body):
    return sms_dispatcher.send(user, to_addr, from_addr, body)
