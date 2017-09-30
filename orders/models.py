# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from catalog.models import Product


class Order(models.Model):
    product = models.ForeignKey(Product,
                                verbose_name="Заказаный товар",
                                related_name="orders")
    customer_name = models.CharField("Имя клиента",
                                     max_length=128,
                                     blank=True)
    customer_phone = models.CharField("Телефон клиента",
                                      max_length=128)
    created = models.DateTimeField("Дата заказа",
                                   auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __unicode__(self):
        return self.customer_phone + " №" + str(self.id)
