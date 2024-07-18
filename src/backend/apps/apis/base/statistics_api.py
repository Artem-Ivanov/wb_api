import datetime
from typing import Optional

import structlog

from apps.apis.base.transport import HttpTransport

logger = structlog.get_logger(__name__)


class StatisticsAPI:
    """
    API клиент для сервиса Statistics.

    https://openapi.wildberries.ru/statistics/api/ru/
    """

    def __init__(self, host: str, transport: Optional[HttpTransport] = None):
        self._host = host
        self._http = transport or HttpTransport()

    def get_stocks_statistics(self, token: str) -> dict:
        """
        Остатки товаров на складах WB. Данные обновляются раз в 30 минут.
        Сервис статистики не хранит историю остатков товаров, поэтому получить данные о
        них можно только в режиме "на текущий момент". Максимум 1 запрос в минуту.
        """
        url = f"{self._host}/api/v1/supplier/stocks"
        resp = self._http.get(url, token, params={"dateFrom": datetime.date.today().isoformat()})
        self._http.check_status(resp)
        return self._http.decode_json(resp)

    def get_orders(self, token: str) -> dict:
        """Заказы. Гарантируется хранение данных не более 90 дней от даты заказа.
        Данные обновляются раз в 30 минут. Для идентификации заказа следует использовать поле srid.
        1 строка = 1 заказ = 1 единица товара. Максимум 1 запрос в минуту
        """

        url = f"{self._host}/api/v1/supplier/orders"
        resp = self._http.get(url, token, params={"dateFrom": datetime.date.today().isoformat()})
        self._http.check_status(resp)
        return self._http.decode_json(resp)

    def get_sales(self, token: str) -> dict:
        """Продажи и возвраты. Гарантируется хранение данных не более 90 дней от даты продажи.
        Данные обновляются раз в 30 минут. Для идентификации заказа следует использовать поле srid.
        1 строка = 1 продажа/возврат = 1 единица товара. Максимум 1 запрос в минуту
        """
        url = f"{self._host}/api/v1/supplier/sales"
        resp = self._http.get(url, token, params={"dateFrom": datetime.date.today().isoformat()})
        self._http.check_status(resp)
        return self._http.decode_json(resp)
