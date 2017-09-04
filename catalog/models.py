# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class ProductCategory(models.Model):
    name = models.CharField("Название категории",
                            max_length=128)
    description = models.TextField("Описание категории")

    class Meta:
        verbose_name = "Категория товаров"
        verbose_name_plural = "Категории товаров"

    def __unicode__(self):
        return self.name


class ProductAttributes(models.Model):
    name = models.CharField("Характеристика товара",
                            max_length=128,
                            help_text="Страна, материал и т.п.")
    value = models.CharField("Значение",
                             max_length=128)

    class Meta:
        verbose_name = "Характеристика товара"
        verbose_name_plural = "Характеристики товаров"

    def __unicode__(self):
        return "{} - {}".format(self.name, self.value)


class Product(models.Model):
    category = models.ForeignKey(ProductCategory,
                                 related_name="products",
                                 verbose_name="Категория товара")
    name = models.CharField("Название",
                            max_length=128,
                            blank=True)
    photo = models.ImageField("Изображение",
                              upload_to='products')
    code = models.CharField("Код (Артикул)",
                            max_length=128,
                            blank=True)
    description = models.TextField("Описание",
                                   blank=True)
    size = models.CharField("Размер",
                            max_length=128,
                            blank=True)
    price = models.DecimalField("Цена",
                                max_digits=12,
                                decimal_places=2,
                                blank=True)
    attributes = models.ManyToManyField(ProductAttributes,
                                        related_name="products",
                                        verbose_name="Дополнительные атрибуты")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __unicode__(self):
        return self.name