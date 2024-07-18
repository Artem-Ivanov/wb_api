from django.contrib import admin

from apps.core import models
from apps.core.services.sales_report import SalesReportService


@admin.action(description="Сформировать отчет")
def do_sales_report(self, request, queryset):
    service = SalesReportService()
    service.do_report()
    return models.SalesReport.objects.all()
