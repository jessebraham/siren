# Siren

**Siren** provides an incredibly basic API for sending email and SMS messages via HTTP requests, authorized using HTTP Basic Authentication. Email are sent via a user-configured SMTP server, and SMS are sent using [Twilio](https://www.twilio.com/). Additional services may be supported in the future.

- - -

**Siren** is built using the following packages:  
[starlette](https://github.com/encode/starlette) | [uvicorn](https://github.com/encode/uvicorn) | [peewee](https://github.com/coleifer/peewee) | [bcrypt](https://github.com/pyca/bcrypt/) | [twilio](https://github.com/twilio/twilio-python)

The following packages are used for development and testing:  
[black](https://github.com/ambv/black) | [pytest](https://github.com/pytest-dev/pytest) | [pytest-cov](https://github.com/pytest-dev/pytest-cov)

> **Note:** `starlette` has yet to reach a `1.0` release, so this project will remain questionably stable until at least that point; do not use Siren for anything remotely important without first understanding the risks.

- - -

## Environment Variables

Siren expects a number of environment variables to be set in order to send messages.

For email:

> SIREN_SMTP_HOST  
> SIREN_SMTP_PORT  
> SIREN_SMTP_USERNAME  
> SIREN_SMTP_PASSWORD

For SMS:

> TWILIO_ACCOUNT_SID  
> TWILIO_AUTH_TOKEN


## Endpoints

Siren exposes the following endpoints:

| Action             | Parameters                              |
|:-------------------|:----------------------------------------|
| `POST /send/email` | `{ from_addr, to_addr, subject, body }` |
| `POST /send/sms`   | `{ from_addr, to_addr, body }`          |


## To Do

- [ ] Write documentation and tests  
- [x] ~~Find a simpler way to configure SMTP and Twilio API~~  
- [ ] Improve authentication/session handling  
- [ ] Passing around the `Message` object is less than ideal; fix it  
- [ ] Implement configurable rate limiting  
- [ ] Use CORS middleware?  
