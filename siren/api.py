# -*- coding: utf-8 -*-

from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.endpoints import HTTPEndpoint
from starlette.responses import UJSONResponse

from siren.tasks import send_email, send_sms
from siren.utils import get_logger


api_app = Starlette(debug=True)  # FIXME: set debug in a config file
logger = get_logger()


@api_app.route("/email", methods=("POST",))
class EmailEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        task = BackgroundTask(
            send_email,
            from_addr=data["from_addr"],
            to_addr=data["to_addr"],
            subject=data["subject"],
            body=data["body"],
        )
        message = {"success": True, "data": data}
        return UJSONResponse(message, background=task)


@api_app.route("/sms", methods=("POST",))
class SmsEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        task = BackgroundTask(
            send_sms,
            from_addr=data["from_addr"],
            to_addr=data["to_addr"],
            body=data["body"],
        )
        message = {"success": True, "data": data}
        return UJSONResponse(message, background=task)
