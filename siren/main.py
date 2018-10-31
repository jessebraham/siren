#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uvicorn

from starlette.applications import Starlette

from siren.db import open_database_connection, close_database_connection


# When the application's "startup" event is fired, establish a connection with
# the database. When the "shutdown" event is fired, make sure that we close the
# previously established connection.
app = Starlette(debug=True)  # FIXME: set debug in a config file
app.add_event_handler("startup", open_database_connection)
app.add_event_handler("shutdown", close_database_connection)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
