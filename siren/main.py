#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from starlette.applications import Starlette
from starlette.routing import Mount, Route, Router

from siren.db import close_database_connection, open_database_connection
from siren.endpoints import (
    EmailEndpoint,
    SessionEndpoint,
    SmsEndpoint,
    UserEndpoint,
)


# Instantiate a new Starlette application, and register event handlers for both
# the "startup" and "shutdown" events. These event handlers are used to
# automatically manage the connection to the database.
app = Starlette(debug=True)  # FIXME: set debug in a config file
app.add_event_handler("startup", open_database_connection)
app.add_event_handler("shutdown", close_database_connection)

# Create a separate router for all the "message" endpoints. Broken out to avoid
# deep nesting.
message_router = Router(
    [
        Route("/email", endpoint=EmailEndpoint, methods=("POST",)),
        Route("/sms", endpoint=SmsEndpoint, methods=("POST",)),
    ]
)
router = Router(
    [
        Mount("/messages", app=message_router),
        Route("/sessions", endpoint=SessionEndpoint, methods=("GET", "POST")),
        Route("/users", endpoint=UserEndpoint, methods=("GET", "POST")),
    ]
)
app.mount("", router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
