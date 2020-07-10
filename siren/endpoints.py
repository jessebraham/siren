from starlette.background import BackgroundTask
from starlette.endpoints import HTTPEndpoint
from starlette.responses import UJSONResponse

from siren.db import User
from siren.tasks import send_email, send_sms


class EmailEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        user = User.get(User.username ** request.user.username)

        task = BackgroundTask(
            send_email,
            user=user,
            to_addr=data["to_addr"],
            subject=data["subject"],
            body=data["body"],
        )

        return UJSONResponse("Accepted", status_code=202, background=task)


class SmsEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        user = User.get(User.username ** request.user.username)

        task = BackgroundTask(
            send_sms, user=user, to_addr=data["to_addr"], body=data["body"]
        )

        return UJSONResponse("Accepted", status_code=202, background=task)
