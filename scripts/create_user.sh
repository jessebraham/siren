#!/bin/sh
#
# Create a new user from the provided username and password positional arguments.
#
#   ex.) bash scripts/create_user.sh hjfarnsworth pazuzu3

USERNAME="$1"
PASSWORD="$2"

if [ ! -f instance/siren.db ];
then
    python -c "from siren.db import db, User; db.create_tables([User])"
fi

python -c "from siren.db import User; User.create('$USERNAME', '$PASSWORD')"
