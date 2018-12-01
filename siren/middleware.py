# -*- coding: utf-8 -*-

import base64

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from siren.db import User


class HTTPBasicAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        self.app = app

    def __call__(self, scope):
        basic_auth = self.header_value(scope, "authorization")
        if not basic_auth:
            return self.unauthorized(
                "Unauthorized: Access is denied due to missing credentials"
            )

        (username, password) = self.decode_credentials(basic_auth)
        if not User.authenticate(username, password):
            return self.unauthorized(
                "Unauthorized: Access is denied due to invalid credentials"
            )

        scope["current_user"] = username
        return self.app(scope)

    def header_value(self, scope, header):
        headers = scope["headers"]
        try:
            return next(v for h, v in headers if h.decode("utf-8") == header)
        except StopIteration as exc:
            return None

    def decode_credentials(self, basic_auth):
        b64encoded = basic_auth.decode("utf-8").split(" ")[1]
        b64decoded = base64.b64decode(b64encoded).decode("utf-8")
        (username, password) = b64decoded.split(":")
        return (username, password)

    def unauthorized(self, message):
        headers = {
            "WWW-Authenticate": 'Basic realm="Login Required", charset="UTF-8"'
        }
        return Response(message, status_code=401, headers=headers)
