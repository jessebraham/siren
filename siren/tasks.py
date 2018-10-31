# -*- coding: utf-8 -*-

import os

from twilio.rest import Client


# TODO: replace environment variables with config file
# Twilio "account_sid" and "auth_token" values are loaded from the OS's
# environment. If these aren't present the requests will fail to authenticate.
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")


class SmsDispatcher(object):
    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(account_sid, auth_token)

    def send(self, to_addr, from_addr, body):
        return self.client.messages.create(
            to=to_addr, from_=from_addr, body=body
        )


sms_dispatcher = SmsDispatcher(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# -----------------------------------------------------------------------------
# Background Tasks


async def send_email(to_addr, from_addr, subject, body):
    pass


async def send_sms(to_addr, from_addr, body):
    return sms_dispatcher.send(to_addr, from_addr, body)
