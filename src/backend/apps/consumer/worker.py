import structlog
import requests

from apps.apis.base.statistics_api import StatisticsAPI
from apps.apis.base.suppliers_api import SuppliersAPI
from apps.core.models import Vault, CustomerVault, CustomerSettings, StocksState, Orders, Sales
from django.conf import settings

from apps.core.serializers import VaultSerializer, CustomerVaultSerializer, StocksSerializer, OrderSerializer, \
    SalesSerializer
from apps.core.services.sales_report import SalesReportService

logger = structlog.getLogger(__name__)


class APIError(Exception):
    pass


class ResponseError(APIError):
    def __init__(self, message: str, resp: requests.Response):
        super().__init__(message)
        self.resp = resp


class APIJsonError(ResponseError):
    pass


class Worker:
    suppliers_api = SuppliersAPI(host=settings.SUPPLIERS_URL)
    statistics_api = StatisticsAPI(host=settings.STATISTIC_URL)

    def get_vaults(self, conf: CustomerSettings) -> None:
        vaults = self.suppliers_api.get_vaults(token=conf.token)

        serializer = VaultSerializer(data=vaults, many=True)
        serializer.is_valid(raise_exception=True)

        for vault in serializer.validated_data:
            try:
                vault["owner"] = conf.owner
                Vault.objects.get_or_create(**vault)
            except Exception:
                logger.exception(f"Failed to create Vault {vault.get('external_id')}")

        logger.info(f"All {len(vaults)} Vaults created or updated")

    def get_customer_vaults(self, conf: CustomerSettings) -> None:
        vaults = self.suppliers_api.get_customer_vaults(token=conf.token)

        serializer = CustomerVaultSerializer(data=vaults, many=True)
        serializer.is_valid(raise_exception=True)

        for vault in serializer.validated_data:
            try:
                obj = Vault.objects.get(external_id=vault['vault_id'])
                vault["vault_id"] = obj
                vault["owner"] = conf.owner
                CustomerVault.objects.get_or_create(**vault)
            except Exception:
                logger.exception(f"Failed to create Vault {vault.get('external_id')}")

        logger.info(f"All {len(vaults)} Vaults created or updated")

    def get_stocks_statistics(self, conf: CustomerSettings) -> None:
        items = self.statistics_api.get_stocks_statistics(token=conf.token)

        serializer = StocksSerializer(data=items, many=True)
        serializer.is_valid(raise_exception=True)

        for item in serializer.validated_data:
            try:
                # item["owner"] = conf.owner # TODO add relation
                StocksState.objects.get_or_create(**item)
            except Exception:
                logger.exception(f"Failed to create Item {item}")

        logger.info(f"Item {len(items)} created or updated")

    def get_orders(self, conf: CustomerSettings) -> None:
        items = self.statistics_api.get_orders(token=conf.token)

        serializer = OrderSerializer(data=items, many=True)
        serializer.is_valid(raise_exception=True)

        for item in serializer.validated_data:
            try:
                # item["owner"] = conf.owner # TODO add relation
                Orders.objects.get_or_create(**item)
            except Exception:
                logger.exception(f"Failed to create OrderItem {item}")

        logger.info(f"OrderItem {len(items)} created or updated")

    def get_sales(self, conf: CustomerSettings) -> None:
        items = self.statistics_api.get_sales(token=conf.token)

        serializer = SalesSerializer(data=items, many=True)
        serializer.is_valid(raise_exception=True)

        for item in serializer.validated_data:
            try:
                # item["owner"] = conf.owner # TODO add relation
                Sales.objects.get_or_create(**item)
            except Exception:
                logger.exception(f"Failed to create SaleItem {item}")

        logger.info(f"SaleItem {len(items)} created or updated")

    def run(self):
        service = SalesReportService()
        service.do_report()
        for conf in CustomerSettings.objects.all():
            self.get_stocks_statistics(conf)
            self.get_orders(conf)
            self.get_sales(conf)

        exit(0)
