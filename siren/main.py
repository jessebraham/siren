#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from starlette.applications import Starlette
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Route, Router

from siren import settings
from siren.db import close_database_connection, open_database_connection
from siren.endpoints import EmailEndpoint, SmsEndpoint
from siren.middleware import BasicAuthBackend


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

# Instantiate a new Starlette application.
app = Starlette()
app.debug = settings.DEBUG
app.testing = settings.TESTING

# Register the HTTP Basic Authentication middleware, which ensures that each
# request is authenticated with a valid username and password.
app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())

# Register event handlers for both the "startup" and "shutdown" events. These
# event handlers are used to automatically manage the connection to the
# database.
app.add_event_handler("startup", open_database_connection)
app.add_event_handler("shutdown", close_database_connection)

router = Router(
    [
        Route("/email", endpoint=EmailEndpoint, methods=("POST",)),
        Route("/sms", endpoint=SmsEndpoint, methods=("POST",)),
    ]
)
app.mount("/send", router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
