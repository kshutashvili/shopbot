# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = models.SlugField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey('Category', related_name='categories')
    title = models.CharField(max_length=128, verbose_name='Title')
    text = models.TextField(max_length=1024, verbose_name='Additional text')

    def __unicode__(self):
        return self.text


class Answer(models.Model):
    question = models.OneToOneField(Question, verbose_name='Question')
    text = models.TextField(max_length=8192, verbose_name='Answer')

    def __unicode__(self):
        return self.question.text
