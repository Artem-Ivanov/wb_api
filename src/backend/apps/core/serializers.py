from rest_framework import serializers


class VaultSerializer(serializers.Serializer):
    address = serializers.CharField()
    name = serializers.CharField()
    city = serializers.CharField()
    id = serializers.IntegerField(source="external_id")
    selected = serializers.BooleanField(default=False)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    cargoType = serializers.IntegerField(source="cargo_type")
    deliveryType = serializers.IntegerField(source="delivery_type")


class CustomerVaultSerializer(serializers.Serializer):
    name = serializers.CharField()
    officeId = serializers.IntegerField(source="vault_id")
    id = serializers.IntegerField(source="external_id")
    cargoType = serializers.IntegerField(source="cargo_type")
    deliveryType = serializers.IntegerField(source="delivery_type")


class StocksSerializer(serializers.Serializer):
    lastChangeDate = serializers.DateTimeField(source="last_change_date")
    warehouseName = serializers.CharField(source="warehouse_name")
    supplierArticle = serializers.CharField(source="supplier_article")
    nmId = serializers.IntegerField(source="nm_id")
    barcode = serializers.CharField()
    quantity = serializers.IntegerField()
    inWayToClient = serializers.IntegerField(source="in_way_to_client")
    inWayFromClient = serializers.IntegerField(source="in_way_from_client")
    quantityFull = serializers.IntegerField(source="quantity_full")
    category = serializers.CharField()
    subject = serializers.CharField()
    brand = serializers.CharField()
    techSize = serializers.CharField(source="tech_size")
    Price = serializers.CharField(source="price")
    Discount = serializers.CharField(source="discount")
    isSupply = serializers.BooleanField(source="is_supply")
    isRealization = serializers.BooleanField(source="is_realization")
    SCCode = serializers.CharField(source="sc_code")


class OrderSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    lastChangeDate = serializers.DateTimeField(source="last_change_date")
    warehouseName = serializers.CharField(source="warehouse_name")
    countryName = serializers.CharField(source="country_name")
    oblastOkrugName = serializers.CharField(source="oblast_okrug_name", allow_blank=True)
    regionName = serializers.CharField(source="region_name")
    supplierArticle = serializers.CharField(source="supplier_article")
    nmId = serializers.IntegerField(source="nm_id")
    barcode = serializers.CharField()
    category = serializers.CharField()
    subject = serializers.CharField()
    brand = serializers.CharField()
    techSize = serializers.CharField(source="tech_size")
    incomeID = serializers.IntegerField(source="income_id")
    isSupply = serializers.BooleanField(source="is_supply")
    isRealization = serializers.BooleanField(source="is_realization")
    totalPrice = serializers.DecimalField(max_digits=9, decimal_places=6, default=0.0, source="total_price")
    discountPercent = serializers.DecimalField(max_digits=9, decimal_places=6, default=0.0, source="discount_percent")
    spp = serializers.IntegerField()
    finishedPrice = serializers.DecimalField(max_digits=9, decimal_places=6, default=0.0, source="finished_price")
    priceWithDisc = serializers.DecimalField(max_digits=9, decimal_places=6, default=0.0, source="price_with_disc")
    isCancel = serializers.BooleanField(source="is_cancel")
    cancelDate = serializers.CharField(source="cancel_date")
    orderType = serializers.CharField(source="order_type")
    sticker = serializers.CharField(allow_null=True, allow_blank=True)
    gNumber = serializers.CharField(source="g_number")
    srid = serializers.CharField()


class SalesSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    lastChangeDate = serializers.DateTimeField(source="last_change_date")
    warehouseName = serializers.CharField(source="warehouse_name")
    countryName = serializers.CharField(source="country_name")
    oblastOkrugName = serializers.CharField(source="oblast_okrug_name", allow_blank=True)
    regionName = serializers.CharField(source="region_name")
    supplierArticle = serializers.CharField(source="supplier_article")
    nmId = serializers.IntegerField(source="nm_id")
    barcode = serializers.CharField()
    category = serializers.CharField()
    subject = serializers.CharField()
    brand = serializers.CharField()
    techSize = serializers.CharField(source="tech_size")
    incomeID = serializers.IntegerField(source="income_id")
    isSupply = serializers.BooleanField(source="is_supply")
    isRealization = serializers.BooleanField(source="is_realization")
    totalPrice = serializers.DecimalField(max_digits=9, decimal_places=6, default=0.0, source="total_price")
    discountPercent = serializers.DecimalField(max_digits=9, decimal_places=6, default=0.0, source="discount_percent")
    spp = serializers.IntegerField()
    paymentSaleAmount = serializers.IntegerField(source="payment_sale_amount")
    forPay = serializers.DecimalField(max_digits=9, decimal_places=6, default=0.0, source="for_pay")
    finishedPrice = serializers.DecimalField(max_digits=9, decimal_places=6, default=0.0, source="finished_price")
    priceWithDisc = serializers.DecimalField(max_digits=9, decimal_places=6, default=0.0, source="price_with_disc")
    saleID = serializers.CharField(source="sale_id")
    orderType = serializers.CharField(source="order_type")
    sticker = serializers.CharField(allow_null=True, allow_blank=True)
    gNumber = serializers.CharField(source="g_number")
    srid = serializers.CharField()


class SalesReportItemSerializer(serializers.Serializer):
    supplier_article = serializers.CharField()
    nm_id = serializers.IntegerField()
    barcode = serializers.CharField()
    actual_count = serializers.IntegerField()
    sale_count = serializers.IntegerField()
