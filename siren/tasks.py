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
        msg_model = Message.create(user, "email", self.from_addr, to_addr)

        message = self.smtp_authenticate_and_send(to_addr, subject, body)
        if message is not None:
            msg_model.deliver()

        return message

    def smtp_authenticate_and_send(self, to_addr, subject, body):
        with smtplib.SMTP(self.host, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.username, self.password)

            try:
                email = self.construct_email(to_addr, subject, body)
                message = smtp.send_message(email)
            except Exception:
                message = None

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
        msg = Message.create(user, "sms", self.from_number, to_addr)

        message = self.client.messages.create(
            to=to_addr, from_=self.from_number, body=body
        )
        if message is not None:
            msg.sid = message.sid
            msg.deliver()

        return message


email_dispatcher = EmailDispatcher(**settings.siren_config["email"])
sms_dispatcher = SmsDispatcher(**settings.siren_config["sms"])


async def send_email(user, to_addr, subject, body):
    return email_dispatcher.send(user, to_addr, subject, body)


async def send_sms(user, to_addr, body):
    return sms_dispatcher.send(user, to_addr, body)
