# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from catalog.models import Product


class TelegramOrder(models.Model):
    product = models.ForeignKey(Product)
    customer_name = models.CharField(max_length=128, blank=True)
    customer_phone = models.CharField(max_length=128, blank=True)
    customer_id = models.CharField(max_length=128, blank=True)
