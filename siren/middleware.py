"""
The `BasicAuthBackend` class is taken essentially verbatim from the Starlette
documentation.

https://www.starlette.io/authentication/
"""

import base64
import binascii

from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)

from siren.db import User


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "basic":
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError("Invalid basic auth credentials")

        username, _, password = decoded.partition(":")
        if not User.authenticate(username, password):
            raise AuthenticationError("Invalid basic auth credentials")

        return AuthCredentials(["authenticated"]), SimpleUser(username)
