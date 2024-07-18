from django.db import models
from django.conf import settings


class Vault(models.Model):
    address = models.CharField(max_length=512, verbose_name="Адрес")
    name = models.CharField(max_length=512, verbose_name="Название")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="user", on_delete=models.PROTECT)
    city = models.CharField(max_length=256, verbose_name="Город",)
    external_id = models.BigIntegerField(verbose_name="ID")
    selected = models.BooleanField(default=False, verbose_name="Признак того, что склад уже выбран продавцом")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, verbose_name="Долгота")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, verbose_name="Широта")
    cargo_type = models.IntegerField(verbose_name="Тип доставки, который принимает склад")
    delivery_type = models.IntegerField(verbose_name="Тип товара, который принимает склад")

    class Meta:
        db_table = "vaults"
        verbose_name = "Склад WB"
        verbose_name_plural = "Склады WB"


class CustomerVault(models.Model):
    name = models.CharField(max_length=512, verbose_name="Название")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="user", on_delete=models.PROTECT)
    vault_id = models.ForeignKey("Vault", verbose_name="vault", on_delete=models.CASCADE)
    external_id = models.BigIntegerField(verbose_name="ID")
    cargo_type = models.IntegerField(verbose_name="Тип доставки, который принимает склад")
    delivery_type = models.IntegerField(verbose_name="Тип товара, который принимает склад")

    class Meta:
        db_table = "customer_vaults"
        verbose_name = "Склад продавца"
        verbose_name_plural = "Склады продавца"


class CustomerSettings(models.Model):
    name = models.CharField(max_length=512, verbose_name="Название")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="user", on_delete=models.PROTECT)
    token = models.CharField(max_length=512, verbose_name="API токен")

    class Meta:
        db_table = "customer_settings"
        verbose_name = "Настройка продавца"
        verbose_name_plural = "Настройки продавца"


class StocksState(models.Model):
    last_change_date = models.DateTimeField(verbose_name="Дата и время обновления информации в сервисе")
    warehouse_name = models.CharField(max_length=128, verbose_name="Название склада")
    supplier_article = models.CharField(max_length=128, verbose_name="Артикул продавца")
    nm_id = models.IntegerField(verbose_name="Артикул WB")
    barcode = models.CharField(max_length=128, verbose_name="Баркод")
    quantity = models.IntegerField(verbose_name="Количество, доступное для продажи")
    in_way_to_client = models.IntegerField(verbose_name="В пути к клиенту")
    in_way_from_client = models.IntegerField(verbose_name="В пути от клиента")
    quantity_full = models.IntegerField(verbose_name="Полное (непроданное) количество, которое числится за складом")
    category = models.CharField(max_length=128, verbose_name="Категория")
    subject = models.CharField(max_length=128, verbose_name="Предмет")
    brand = models.CharField(max_length=128, verbose_name="Бренд")
    tech_size = models.CharField(max_length=128, verbose_name="Размер")
    price = models.CharField(max_length=128, verbose_name="Цена")
    discount = models.CharField(max_length=128, verbose_name="Скидка")
    is_supply = models.BooleanField(verbose_name="Договор поставки (внутренние технологические данные)")
    is_realization = models.BooleanField(verbose_name="Договор реализации (внутренние технологические данные)")
    sc_code = models.CharField(max_length=128, verbose_name="Код контракта (внутренние технологические данные)")

    class Meta:
        db_table = "stock_state"
        verbose_name = "Остатки товаров на складах WB"
        verbose_name_plural = "Остаток товара на складе WB"


class Orders(models.Model):
    date = models.DateTimeField(verbose_name="Дата и время заказа")
    last_change_date = models.DateTimeField(verbose_name="Дата и время обновления информации в сервисе")
    warehouse_name = models.CharField(max_length=128, verbose_name="Склад отгрузки")
    country_name = models.CharField(max_length=128, verbose_name="Страна")
    oblast_okrug_name = models.CharField(max_length=128, verbose_name="Округ", blank=True)
    region_name = models.CharField(max_length=128, verbose_name="Регион")
    supplier_article = models.CharField(max_length=128, verbose_name="Артикул продавца")
    nm_id = models.IntegerField(verbose_name="Артикул WB")
    barcode = models.CharField(max_length=128, verbose_name="Баркод")
    category = models.CharField(max_length=128, verbose_name="Категория")
    subject = models.CharField(max_length=128, verbose_name="Предмет")
    brand = models.CharField(max_length=128, verbose_name="Бренд")
    tech_size = models.CharField(max_length=128, verbose_name="Размер товара")
    income_id = models.IntegerField(verbose_name="Номер поставки")
    is_supply = models.BooleanField(verbose_name="Договор поставки")
    is_realization = models.BooleanField(verbose_name="Договор реализации")
    total_price = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, verbose_name="Цена без скидок")
    discount_percent = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, verbose_name="Скидка продавца")
    spp = models.IntegerField(verbose_name="Скидка WB")
    finished_price = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, verbose_name="Цена с учетом всех скидок, кроме суммы по WB Кошельку")
    price_with_disc = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, verbose_name="Цена со скидкой продавца")
    is_cancel = models.BooleanField(verbose_name="Отмена заказа.")
    cancel_date = models.CharField(max_length=128, verbose_name="Дата и время отмены заказа.")
    order_type = models.CharField(max_length=128, verbose_name="Тип заказа")
    sticker = models.CharField(max_length=128, verbose_name="Идентификатор стикера")
    g_number = models.CharField(max_length=128, verbose_name="Номер заказа")
    srid = models.CharField(max_length=128, verbose_name="Уникальный идентификатор заказа")

    class Meta:
        db_table = "orders"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Sales(models.Model):
    date = models.DateTimeField(verbose_name="Дата и время продажи")
    last_change_date = models.DateTimeField(verbose_name="Дата и время обновления информации в сервисе")
    warehouse_name = models.CharField(max_length=128, verbose_name="Склад отгрузки")
    country_name = models.CharField(max_length=128, verbose_name="Страна")
    oblast_okrug_name = models.CharField(max_length=128, verbose_name="Округ", blank=True)
    region_name = models.CharField(max_length=128, verbose_name="Регион")
    supplier_article = models.CharField(max_length=128, verbose_name="Артикул продавца")
    nm_id = models.IntegerField(verbose_name="Артикул WB")
    barcode = models.CharField(max_length=128, verbose_name="Баркод")
    category = models.CharField(max_length=128, verbose_name="Категория")
    subject = models.CharField(max_length=128, verbose_name="Предмет")
    brand = models.CharField(max_length=128, verbose_name="Бренд")
    tech_size = models.CharField(max_length=128, verbose_name="Размер товара")
    income_id = models.IntegerField(verbose_name="Номер поставки")
    is_supply = models.BooleanField(verbose_name="Договор поставки")
    is_realization = models.BooleanField(verbose_name="Договор реализации")
    total_price = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, verbose_name="Цена без скидок")
    discount_percent = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, verbose_name="Скидка продавца")
    spp = models.IntegerField(verbose_name="Скидка WB")
    payment_sale_amount = models.IntegerField(verbose_name="Оплачено с WB Кошелька")
    for_pay = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, verbose_name="К перечислению продавцу")
    finished_price = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, verbose_name="Фактическая цена с учетом всех скидок (к взиманию с покупателя)")
    price_with_disc = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, verbose_name="Цена со скидкой продавца")
    sale_id = models.CharField(max_length=128, verbose_name="Уникальный идентификатор продажи/возврата")
    order_type = models.CharField(max_length=128, verbose_name="Тип заказа")
    sticker = models.CharField(max_length=128, verbose_name="Идентификатор стикера")
    g_number = models.CharField(max_length=128, verbose_name="Номер заказа")
    srid = models.CharField(max_length=128, verbose_name="Уникальный идентификатор заказа")

    class Meta:
        db_table = "sales"
        verbose_name = "Продажа/возврат"
        verbose_name_plural = "Продажи и возвраты"


class SalesReport(models.Model):
    supplier_article = models.CharField(max_length=128, verbose_name="Артикул продавца")
    nm_id = models.IntegerField(verbose_name="Артикул WB")
    barcode = models.CharField(max_length=128, verbose_name="Баркод")
    actual_count = models.IntegerField(verbose_name="В наличии")
    sale_count = models.IntegerField(verbose_name="Продано сегодня")

    class Meta:
        db_table = "sales_report"
        verbose_name = "Отчет производства"
        verbose_name_plural = "Отчет производства"
