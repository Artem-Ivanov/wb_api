from typing import Optional

import structlog

from apps.apis.base.transport import HttpTransport

logger = structlog.get_logger(__name__)


class SuppliersAPI:
    """
    API клиент для сервиса Suppliers.

    https://openapi.wildberries.ru/marketplace/api/ru/
    """

    def __init__(self, host: str, transport: Optional[HttpTransport] = None):
        self._host = host
        self._http = transport or HttpTransport()

    def get_vaults(self, token: str) -> dict:
        """
        Получить список складов WB.
        """
        url = f"{self._host}/api/v3/offices"
        resp = self._http.get(url, token)
        self._http.check_status(resp)
        return self._http.decode_json(resp)

    def get_customer_vaults(self, token: str) -> dict:
        """
        Получить список складов продавца.
        """
        url = f"{self._host}/api/v3/warehouses"
        resp = self._http.get(url, token)
        self._http.check_status(resp)
        return self._http.decode_json(resp)
