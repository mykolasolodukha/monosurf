"""The schemas for the API."""

from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_core import Url

from settings import settings


# region Merchant schemas
class BaseMerchantSchema(BaseModel):
    """The base schema for a Merchant."""

    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)

    username: str = Field(..., max_length=255)

    email: EmailStr = Field(..., max_length=255)


class MerchantCreateSchema(BaseMerchantSchema):
    """The schema for a Merchant."""


class MerchantSchema(BaseMerchantSchema):
    """The schema for a Merchant."""

    id: int


# endregion


# region Monobank client & accounts schemas
class MonobankClientBaseSchema(BaseModel):
    """The base schema for a Monobank client."""

    merchant_id: int


class MonobankClientCreateSchema(MonobankClientBaseSchema):
    """The schema for a Monobank client creation request."""

    token: str


class MonobankClientSchema(MonobankClientBaseSchema):
    """The schema for a Monobank client."""

    client_id: str
    name: str
    web_hook_url: str
    permissions: str


# endregion


# region Monobank Account & Jar schemas


class BaseMonobankAccountSchema(BaseModel):
    """The base schema for a Monobank account."""

    id: Annotated[str, Field(str, max_length=31)]
    send_id: Annotated[str, Field(str, max_length=14)] | None = None

    currency_code: int
    balance: int


class MonobankAccountSchema(BaseMonobankAccountSchema):
    """The schema for a Monobank account."""

    masked_pan: str | None = None

    type: str

    credit_limit: int

    cashback_type: str | None = None


class MonobankJarSchema(BaseMonobankAccountSchema):
    """The schema for a Monobank jar."""

    title: str
    description: str | None = None

    goal: int | None = None


# endregion


# region API key schemas
class MerchantApiKeyBaseSchema(BaseModel):
    """The base schema for a Merchant API key."""

    merchant_id: int


class MerchantApiKeyCreateSchema(MerchantApiKeyBaseSchema):
    """The schema for a Merchant API key creation request."""


class MerchantApiKeySchema(MerchantApiKeyBaseSchema):
    """The schema for a Merchant API key."""

    id: int

    key: UUID | None = Field(None, description="The API key. `null` if the key is masked.")
    masked_key: str = Field(
        ...,
        description="The masked API key. The first 4 and the last 4 characters are visible, the rest are masked.",
    )


# endregion


# region Paycheck schemas
class BasePaycheckSchema(BaseModel):
    """The base schema for a Paycheck."""

    for_customer_id: Annotated[int | str, Field(gt=0, description="The ID of the customer.")]

    @field_validator("for_customer_id")
    @classmethod
    def for_customer_id_must_be_int_or_str(cls, v: int | str) -> int | str:
        """Validate the `for_customer_id` field."""
        if not isinstance(v, (int, str)):
            raise ValueError("`for_customer_id` must be an integer or a string")
        if isinstance(v, str) and len(v) > 255:
            raise ValueError("`for_customer_id` must be at most 255 characters long")
        return v

    to_account_id: Annotated[str, Field(max_length=22, description="The ID of the account.")] | None = None
    to_jar_id: Annotated[str, Field(max_length=31, description="The ID of the jar.")] | None = None

    amount: Annotated[
        int,
        Field(
            gt=0,
            description="The amount of the paycheck in the smallest currency unit.",
        ),
    ]

    comment: str | None = None

    currency_symbol: str = settings.DEFAULT_CURRENCY_SYMBOL
    currency_code: int = settings.DEFAULT_CURRENCY_CODE


class PaycheckCreateSchema(BasePaycheckSchema):
    """The schema for a paycheck creation request."""


class PaycheckCreateResponseSchema(PaycheckCreateSchema):
    """The schema for a paycheck creation response."""

    id: UUID

    payment_link: Url

    is_paid: bool


# endregion
