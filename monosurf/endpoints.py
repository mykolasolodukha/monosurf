"""All the endpoints for the `monosurf` API service."""

from enum import Enum


class Endpoint(str, Enum):
    """The endpoints for the `monosurf` API service."""

    GET_ME = "/merchants/me"
    CREATE_MERCHANT = "/merchants/create"

    GET_MERCHANT_BY_ID = "/merchants/${merchant_id}"

    GET_MONOBANK_CLIENTS = "/monobank/clients"
    CREATE_MONOBANK_CLIENT = "/monobank/clients/create"

    GET_MONOBANK_ACCOUNTS = "/monobank/accounts"

    GET_MONOBANK_JARS = "/monobank/jars"

    GET_API_KEYS = "/api-keys"
    CREATE_API_KEY = "/api-keys/create"

    CREATE_PAYCHECK = "/paychecks/create"
    GET_PAYCHECK = "/paychecks/${paycheck_id}"
