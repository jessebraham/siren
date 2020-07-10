# Siren

[![Build Status](https://travis-ci.org/jessebraham/siren.svg?branch=master)](https://travis-ci.org/jessebraham/siren)
[![Coverage Status](https://coveralls.io/repos/github/jessebraham/siren/badge.svg?branch=master)](https://coveralls.io/github/jessebraham/siren?branch=master)

__Siren__ provides a basic API for sending email and SMS messages via HTTP requests, authorized using [HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication). Email are sent via a user-configured SMTP server, and SMS are sent using [Twilio](https://www.twilio.com/). Additional services may be supported in the future; if you would like to see a service supported feel free to open an issue.

> __NOTE:__ `starlette` has yet to reach a `1.0` release, so this project will remain questionably stable until at least that point; do not use Siren for anything remotely important without first understanding the risks.

- - -

__Siren__ is built using the following packages:  
[bcrypt](https://github.com/pyca/bcrypt/) | [peewee](https://github.com/coleifer/peewee) | [starlette](https://github.com/encode/starlette) | [twilio](https://github.com/twilio/twilio-python) | [uvicorn](https://github.com/encode/uvicorn)

The following packages are used for development and testing:  
[black](https://github.com/ambv/black) | [faker](https://github.com/joke2k/faker) | [pytest](https://github.com/pytest-dev/pytest) | [pytest-cov](https://github.com/pytest-dev/pytest-cov)

- - -

## Quickstart

__TODO:__ write me

## Configuration

Configuration is done using Environment Variables, following [the twelve-factor pattern](https://12factor.net/config). An example configuration file can be found below.

```bash
# instance/.env
#
# Don't commit this to source control.
# Eg. Include ".env" in your `.gitignore` file.

DEBUG=False

TWILIO_ACCOUNT_SID="your-twilio-account-sid"
TWILIO_AUTH_TOKEN="your-twilio-auth-token"
TWILIO_FROM_NUMBER="+18005551234"

SIREN_SMTP_HOST="smtp.example.com"
SIREN_SMTP_PORT=587
SIREN_SMTP_USERNAME="you@example.com"
SIREN_SMTP_PASSWORD="your-smtp-password"
SIREN_SMTP_FROM_ADDR="you@example.com"
```

## Endpoints

__Siren__ exposes the following endpoints:

| Method | Route         | Parameters                   |
|:-------|:--------------|:-----------------------------|
| `POST` | `/send/email` | `{ to_addr, subject, body }` |
| `POST` | `/send/sms`   | `{ to_addr, body }`          |

A username and password must be supplied, as _all_ requests are authenticated using [HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication). To send an SMS message using `curl`, run:

```bash
$ curl -X POST \
  http://user:password@localhost:8000/send/sms \
  -H 'Content-Type: application/json' \
  -d '{ "to_addr": "+12223334444", "body": "Science!" }'
```

## License

__Siren__ is released under the MIT License. See the bundled [LICENSE](LICENSE) file for details.
