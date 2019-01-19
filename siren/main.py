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

app = Starlette()
app.debug = settings.DEBUG
app.testing = settings.TESTING

app.mount(
    "/send",
    Router(
        [
            Route("/email", endpoint=EmailEndpoint, methods=("POST",)),
            Route("/sms", endpoint=SmsEndpoint, methods=("POST",)),
        ]
    ),
)

# Register event handlers for both the "startup" and "shutdown" events. These
# event handlers are used to automatically manage the connection to the
# database.
app.add_event_handler("startup", open_database_connection)
app.add_event_handler("shutdown", close_database_connection)

# Use the built-in Authentication Middleware, utilizing the custom HTTP Basic
# Authentication backend from `middleware.py`. Using this middleware, every
# request requires a username and password to be provided.
app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
