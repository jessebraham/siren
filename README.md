# siren

Siren provides an incredibly basic API for sending email and SMS messages via HTTP requests, using HTTP Basic Authentication. Email are sent via a user-configured SMTP server, and SMS are sent using [Twilio](https://www.twilio.com/).

Siren is built using the following packages:  
[starlette](https://github.com/encode/starlette) | [uvicorn](https://github.com/encode/uvicorn) | [peewee](https://github.com/coleifer/peewee) | [bcrypt](https://github.com/pyca/bcrypt/) | [twilio](https://github.com/twilio/twilio-python)

The following packages are used for development and testing:  
[black](https://github.com/ambv/black) | [pytest](https://github.com/pytest-dev/pytest) | [pytest-cov](https://github.com/pytest-dev/pytest-cov)

**Note:** Starlette has yet to reach a `1.0` release, so this project will remain questionably stable until that point; do not use for anything moderately important without understanding the risks.


## Endpoints

Siren exposes the following endpoints:

| Action             | Parameters                              |
|:-------------------|:----------------------------------------|
| `POST /send/email` | `{ from_addr, to_addr, subject, body }` |
| `POST /send/sms`   | `{ from_addr, to_addr, body }`          |


## To Do

- [ ] Find a simpler way to configure SMTP and Twilio API
- [ ] Implement configurable rate limiting
- [ ] Improve authentication/session handling
- [ ] Create a minimal admin interface
- [ ] Write documentation and tests
