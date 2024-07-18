from apps.core import models, serializers


class SalesReportService:
    model_cls = models.SalesReport
    serializer = serializers.SalesReportItemSerializer
    report = {}

    def do_report(self):
        for sale in models.Sales.objects.all():
            if sale.sale_id[0] == "S":
                actual_count = -1
                sale_count = 1
            else:
                actual_count = 1
                sale_count = -1
            if sale.nm_id in self.report.keys():
                item = self.report[sale.nm_id]
                item["actual_count"] += actual_count
                item["sale_count"] += sale_count
            else:
                self.report[sale.nm_id] = {
                    "supplier_article":  sale.supplier_article,
                    "nm_id": sale.nm_id,
                    "barcode": sale.barcode,
                    "actual_count": actual_count,
                    "sale_count": sale_count,
                }

        for order in models.Orders.objects.all():
            if order.is_cancel:
                actual_count = 1
                sale_count = -1
            else:
                actual_count = -1
                sale_count = 1
            if order.nm_id in self.report.keys():
                item = self.report[order.nm_id]
                item["actual_count"] += actual_count
                item["sale_count"] += sale_count
            else:
                self.report[order.nm_id] = {
                    "supplier_article":  order.supplier_article,
                    "nm_id": order.nm_id,
                    "barcode": order.barcode,
                    "actual_count": actual_count,
                    "sale_count": sale_count,
                }

            serializer = self.serializer(data=list(self.report.values()), many=True)
            serializer.is_valid(raise_exception=True)

            for item in serializer.validated_data:
                self.model_cls.objects.get_or_create(**item)

    def __init__(self):
        self.model_cls.objects.all().delete()
