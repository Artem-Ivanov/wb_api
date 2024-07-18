import structlog
from django.contrib import admin


from apps.core import models, admin_action

logger = structlog.getLogger(__name__)


class BaseReadOnlyModel(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(models.Vault)
class VaultAdmin(BaseReadOnlyModel):
    list_display = (
        "id",
        "external_id",
        "address",
        "name",
        "city",
    )

    search_fields = (
        "external_id",
    )

    def get_queryset(self, request):
        return models.Vault.objects.filter(owner=request.user)


@admin.register(models.CustomerVault)
class CustomerVaultAdmin(BaseReadOnlyModel):
    list_display = (
        "id",
        "name",
        "vault_id",
        "external_id",
    )

    def get_queryset(self, request):
        return models.CustomerVault.objects.filter(owner=request.user)


@admin.register(models.CustomerSettings)
class CustomerVaultAdmin(BaseReadOnlyModel):
    list_display = (
        "name",
        "token",
    )

    def get_queryset(self, request):
        return models.CustomerSettings.objects.filter(owner=request.user)

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return not models.CustomerSettings.objects.filter(owner=request.user).exists()


@admin.register(models.StocksState)
class StocksStateAdmin(BaseReadOnlyModel):
    list_display = (
        "supplier_article",
        "warehouse_name",
        "barcode",
        "quantity",
        "in_way_to_client",
        "in_way_from_client",
        "quantity_full",
    )

    search_fields = (
        "barcode",
    )


@admin.register(models.Orders)
class OrderAdmin(BaseReadOnlyModel):
    list_display = (
        "date",
        "supplier_article",
        "barcode",
        "is_cancel",
    )

    search_fields = (
        "barcode",
    )


@admin.register(models.Sales)
class SalesAdmin(BaseReadOnlyModel):
    list_display = (
        "date",
        "supplier_article",
        "barcode",
        "sale_id",
    )

    search_fields = (
        "barcode",
    )


@admin.register(models.SalesReport)
class ReportsAdmin(BaseReadOnlyModel):
    list_display = (
        "supplier_article",
        "nm_id",
        "barcode",
        "actual_count",
    )

    actions = [admin_action.do_sales_report]
