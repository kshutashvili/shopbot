# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    name = models.CharField('Категория',
                            max_length=32,
                            unique=True
                            )
    slug = models.SlugField('Постоянная ссылка',
                            max_length=64,
                            unique=True
                            )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __unicode__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(Category,
                                related_name='categories',
                                verbose_name='Категория вопроса'
                                )
    title = models.CharField(max_length=128, verbose_name='Заголовок вопроса')
    text = models.TextField(
                            max_length=1024,
                            verbose_name='Дополнительный текст'
                            )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    question = models.OneToOneField(Question, verbose_name='Вопрос')
    text = models.TextField('Ответ', max_length=8192)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __unicode__(self):
        return self.question.title
