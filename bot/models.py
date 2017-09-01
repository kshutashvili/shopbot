# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=16, verbose_name='Title')
    text = models.TextField(max_length=1024, verbose_name='Additional text')

    def __str__(self):
        return '{}'.format(self.text)


class Answer(models.Model):
    question = models.OneToOneField(Question, verbose_name='Question')
    text = models.TextField(max_length=10240, verbose_name='Answer')

    def __str__(self):
        return '{}'.format(self.question.text)
