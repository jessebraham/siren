#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from starlette.applications import Starlette
from starlette.routing import Route, Router

from siren.db import close_database_connection, open_database_connection
from siren.endpoints import EmailEndpoint, SmsEndpoint
from siren.middleware import HTTPBasicAuthMiddleware


# Instantiate a new Starlette application and register the HTTP Basic
# Authentication middleware, which ensures that each request is authenticated
# with a valid username and password.
app = Starlette(debug=True)  # FIXME: set debug in a config file
app.add_middleware(HTTPBasicAuthMiddleware)

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
