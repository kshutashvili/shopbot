# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'text',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
