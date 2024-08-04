"""The `MonosurfClient`."""

import httpx

from endpoints import Endpoint
from schemas import (
    MerchantApiKeySchema,
    MerchantCreateSchema,
    MerchantSchema,
    MonobankAccountSchema,
    MonobankClientCreateSchema,
    MonobankClientSchema,
    MonobankJarSchema,
    PaycheckCreateResponseSchema,
    PaycheckCreateSchema,
)
from settings import settings


class MonosurfClient:
    """The `MonosurfClient`."""

    def __init__(self, api_key: str):
        """Initialize the `MonosurfClient` with the given `api_key`."""
        self.api_host = "https://api.mono.surf"

        self._session = httpx.AsyncClient(headers={settings.API_KEY_HEADER_NAME: api_key})

    # region Syntax sugar
    async def _request(self, method: str, url: Endpoint, **kwargs) -> dict:
        """Make a request to the given `url` with the given `method`."""
        response = await self._session.request(method, f"{self.api_host}/{url.value.lstrip('/')}", **kwargs)
        response.raise_for_status()
        return response.json()

    async def _get(self, url: Endpoint, **kwargs) -> dict:
        """Make a GET request to the given `url`."""
        return await self._request("GET", url, **kwargs)

    async def _post(self, url: Endpoint, **kwargs) -> dict:
        """Make a POST request to the given `url`."""
        return await self._request("POST", url, **kwargs)

    # endregion

    async def get_me(self) -> MerchantSchema:
        """Get the current merchant."""
        return MerchantSchema(**await self._get(Endpoint.GET_ME))

    async def get_merchant_by_id(self, merchant_id: int) -> MerchantSchema:
        """Get the merchant by the given `merchant_id`. Available only for admins."""
        return MerchantSchema(**await self._get(Endpoint.GET_MERCHANT_BY_ID, params={"merchant_id": merchant_id}))

    async def create_merchant(self, merchant: MerchantCreateSchema) -> MerchantSchema:
        """Create a new merchant. Available only for admins."""
        return MerchantSchema(**await self._post(Endpoint.CREATE_MERCHANT, json=merchant.model_dump()))

    async def get_monobank_clients(self) -> list[MonobankClientSchema]:
        """Get all the Monobank clients."""
        return [MonobankClientSchema(**client) for client in await self._get(Endpoint.GET_MONOBANK_CLIENTS)]

    async def create_monobank_client(self, monobank_client: MonobankClientCreateSchema) -> MonobankClientSchema:
        """Create a new Monobank client."""
        return MonobankClientSchema(
            **await self._post(Endpoint.CREATE_MONOBANK_CLIENT, json=monobank_client.model_dump())
        )

    async def get_monobank_accounts(self) -> list[MonobankAccountSchema]:
        """Get all the Monobank accounts."""
        return [MonobankAccountSchema(**account) for account in await self._get(Endpoint.GET_MONOBANK_ACCOUNTS)]

    async def get_monobank_jars(self) -> list[MonobankJarSchema]:
        """Get all the Monobank jars."""
        return [MonobankJarSchema(**jar) for jar in await self._get(Endpoint.GET_MONOBANK_JARS)]

    async def create_api_key(self, merchant_id: int) -> dict:
        """Create a new API key. Available only for admins."""
        return await self._post(Endpoint.CREATE_API_KEY, json={"merchant_id": merchant_id})

    async def get_api_keys(self, merchant_id: int) -> list[MerchantApiKeySchema]:
        """Get all the API keys for the given `merchant_id`."""
        return [
            MerchantApiKeySchema(**api_key)
            for api_key in await self._get(Endpoint.GET_API_KEYS, params={"merchant_id": merchant_id})
        ]

    async def create_paycheck(self, paycheck: PaycheckCreateSchema) -> PaycheckCreateResponseSchema:
        """Create a new paycheck."""
        return PaycheckCreateResponseSchema(**await self._post(Endpoint.CREATE_PAYCHECK, json=paycheck.model_dump()))
