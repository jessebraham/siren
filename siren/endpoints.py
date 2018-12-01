# -*- coding: utf-8 -*-

import logging

from starlette.background import BackgroundTask
from starlette.endpoints import HTTPEndpoint
from starlette.responses import UJSONResponse

from siren.db import Message, User
from siren.tasks import send_email, send_sms


logger = logging.getLogger("siren")


class EmailEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        user = User.get(User.username == request.get("current_user"))

        msg = Message.create(user, "email", data["from_addr"], data["to_addr"])
        task = BackgroundTask(
            send_email,
            user=user,
            msg=msg,
            from_addr=data["from_addr"],
            to_addr=data["to_addr"],
            subject=data["subject"],
            body=data["body"],
        )

        headers = {"Location": f"/queued/{msg.id}"}
        return UJSONResponse(
            "Accepted", status_code=202, headers=headers, background=task
        )


class SmsEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        user = User.get(User.username == request.get("current_user"))

        msg = Message.create(user, "sms", data["from_addr"], data["to_addr"])
        task = BackgroundTask(
            send_sms,
            user=user,
            msg=msg,
            from_addr=data["from_addr"],
            to_addr=data["to_addr"],
            body=data["body"],
        )

        headers = {"Location": f"/queued/{msg.id}"}
        return UJSONResponse(
            "Accepted", status_code=202, headers=headers, background=task
        )
