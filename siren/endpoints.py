# -*- coding: utf-8 -*-

import logging

from starlette.background import BackgroundTask
from starlette.endpoints import HTTPEndpoint
from starlette.responses import UJSONResponse

from siren.db import User
from siren.tasks import send_email, send_sms


logger = logging.getLogger("siren")


class EmailEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        user = request.get("current_user")
        task = BackgroundTask(
            send_email,
            user=User.get(User.username == user),
            from_addr=data["from_addr"],
            to_addr=data["to_addr"],
            subject=data["subject"],
            body=data["body"],
        )
        message = {"success": True, "data": data}
        return UJSONResponse(message, background=task)


class SmsEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        user = request.get("current_user")
        task = BackgroundTask(
            send_sms,
            user=User.get(User.username == user),
            from_addr=data["from_addr"],
            to_addr=data["to_addr"],
            body=data["body"],
        )
        message = {"success": True, "data": data}
        return UJSONResponse(message, background=task)
