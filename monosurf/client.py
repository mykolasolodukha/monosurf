"""The `MonosurfClient`."""

import httpx

from endpoints import Endpoint
from schemas import MerchantSchema, MerchantCreateSchema, MonobankClientSchema, MonobankClientCreateSchema, \
    MonobankAccountSchema, MonobankJarSchema, MerchantApiKeySchema, PaycheckCreateSchema, PaycheckCreateResponseSchema
from settings import settings


class MonosurfClient:
    def __init__(self, api_key: str):
        self.__api_key = api_key

        self.api_host = "https://api.mono.surf"

        self._session = httpx.AsyncClient(headers={settings.API_KEY_HEADER_NAME: api_key})

    # region Syntax sugar
    async def _request(self, method: str, url: Endpoint, **kwargs) -> dict:
        response = await self._session.request(method, f"{self.api_host}/{url.value.lstrip('/')}", **kwargs)
        response.raise_for_status()
        return response.json()

    async def _get(self, url: Endpoint, **kwargs) -> dict:
        return await self._request("GET", url, **kwargs)

    async def _post(self, url: Endpoint, **kwargs) -> dict:
        return await self._request("POST", url, **kwargs)

    # endregion

    async def get_me(self) -> MerchantSchema:
        return MerchantSchema(**await self._get(Endpoint.GET_ME))

    async def get_merchant_by_id(self, merchant_id: int) -> MerchantSchema:
        return MerchantSchema(
            **await self._get(Endpoint.GET_MERCHANT_BY_ID, params={"merchant_id": merchant_id})
        )

    async def create_merchant(self, merchant: MerchantCreateSchema) -> MerchantSchema:
        return MerchantSchema(**await self._post(Endpoint.CREATE_MERCHANT, json=merchant.model_dump()))

    async def get_monobank_clients(self) -> list[MonobankClientSchema]:
        return [MonobankClientSchema(**client) for client in await self._get(Endpoint.GET_MONOBANK_CLIENTS)]

    async def create_monobank_client(self, monobank_client: MonobankClientCreateSchema) -> MonobankClientSchema:
        return MonobankClientSchema(
            **await self._post(Endpoint.CREATE_MONOBANK_CLIENT, json=monobank_client.model_dump())
        )

    async def get_monobank_accounts(self) -> list[MonobankAccountSchema]:
        return [MonobankAccountSchema(**account) for account in await self._get(Endpoint.GET_MONOBANK_ACCOUNTS)]

    async def get_monobank_jars(self) -> list[MonobankJarSchema]:
        return [MonobankJarSchema(**jar) for jar in await self._get(Endpoint.GET_MONOBANK_JARS)]

    async def create_api_key(self, merchant_id: int) -> dict:
        return await self._post(Endpoint.CREATE_API_KEY, json={"merchant_id": merchant_id})

    async def get_api_keys(self, merchant_id: int) -> list[MerchantApiKeySchema]:
        return [MerchantApiKeySchema(**api_key) for api_key in
                await self._get(Endpoint.GET_API_KEYS, params={"merchant_id": merchant_id})]

    async def create_paycheck(self, paycheck: PaycheckCreateSchema) -> PaycheckCreateResponseSchema:
        return PaycheckCreateResponseSchema(
            **await self._post(Endpoint.CREATE_PAYCHECK, json=paycheck.model_dump())
        )
