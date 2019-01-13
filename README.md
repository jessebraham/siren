# Siren

[![Build Status](https://travis-ci.org/jessebraham/siren.svg?branch=master)](https://travis-ci.org/jessebraham/siren) [![Coverage Status](https://coveralls.io/repos/github/jessebraham/siren/badge.svg?branch=master)](https://coveralls.io/github/jessebraham/siren?branch=master)

**Siren** provides a basic API for sending email and SMS messages via HTTP requests, authorized using [HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication). Email are sent via a user-configured SMTP server, and SMS are sent using [Twilio](https://www.twilio.com/). Additional services may be supported in the future; if you would like to see a service supported feel free to open an issue.

> **Note:** `starlette` has yet to reach a `1.0` release, so this project will remain questionably stable until at least that point; do not use Siren for anything remotely important without first understanding the risks.

- - -

**Siren** is built using the following packages:  
[starlette](https://github.com/encode/starlette) | [uvicorn](https://github.com/encode/uvicorn) | [peewee](https://github.com/coleifer/peewee) | [bcrypt](https://github.com/pyca/bcrypt/) | [twilio](https://github.com/twilio/twilio-python)

The following packages are used for development and testing:  
[black](https://github.com/ambv/black) | [pytest](https://github.com/pytest-dev/pytest) | [pytest-cov](https://github.com/pytest-dev/pytest-cov)

- - -

## Endpoints

Siren exposes the following endpoints:

| Action             | Parameters                   |
|:-------------------|:-----------------------------|
| `POST /send/email` | `{ to_addr, subject, body }` |
| `POST /send/sms`   | `{ to_addr, body }`          |

### Example

```bash
$ curl -X POST \
  http://user:password@localhost:8000/send/sms \
  -H 'Content-Type: application/json' \
  -d '{ "to_addr": "+12223334444", "body": "Science!" }'
```


## Configuration

Configuration is performed via Environment Variables, following [the twelve-factor pattern](https://12factor.net/config). An example configuration file, `.env.example`, is included in the project's root directory. To use it:

```bash
$ cp .env.example instance/.env
$ # modify contents of instance/.env
$ source instance/.env
```


## To Do

- [x] ~~Find a simpler way to configure SMTP and Twilio API~~  
- [x] ~~Passing around the `Message` object is less than ideal; fix it~~  
- [ ] Event handlers have stopped firing; fix them  
- [ ] Write documentation, more tests  
- [ ] Implement configurable rate limiting?  
- [ ] Use CORS middleware?  
