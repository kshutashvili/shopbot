# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery

from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from bot.models import Question, Answer, Category
from rest_framework.renderers import JSONRenderer

bot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)
bot.setWebhook(settings.WEBHOOK_URL)


class CommandReceiveView(View):
    categories = Category.objects.all()
    questions = Question.objects.all()
    answers = Answer.objects.all()

    def post(self, request):
        raw = request.body.decode('UTF8')

        try:
            update = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            callback = update.get('callback_query')
            if callback:
                update = callback

            chat_id = update['message']['chat']['id']
            command = update['message'].get('text')
            query_id = update.get('id')
            callback_data = update.get('data')

            if command == '/help':
                bot.sendMessage(chat_id, '*help ^^*', parse_mode='Markdown')

            elif command == '/start':
                keyboard = self._get_main_menu()
                msg = "*Вас приветствует бот Unlured, что Вас интересует?:*"
                bot.sendMessage(
                    chat_id=chat_id,
                    text=msg,
                    parse_mode='Markdown',
                    reply_markup=keyboard,
                )
            elif callback_data:
                mark, data = callback_data.split('_')
                if mark == 'categories':
                    keyboard = self._get_categories()
                    msg = "*Выберите категорию вопроса:*"
                    bot.sendMessage(
                        chat_id=chat_id,
                        text=msg,
                        parse_mode='Markdown',
                        reply_markup=keyboard,
                    )
                elif mark == 'catalog':
                    keyboard = self._get_categories()
                    msg = "*Выберите категорию вопроса:*"
                    bot.sendMessage(
                        chat_id=chat_id,
                        text=msg,
                        parse_mode='Markdown',
                        reply_markup=keyboard,
                    )
                elif mark == 'questions':
                    keyboard = self._get_questions(data) # data = category__slug
                    msg = "*Выберите вопрос:*"
                    bot.sendMessage(
                        chat_id=chat_id,
                        text=msg,
                        parse_mode='Markdown',
                        reply_markup=keyboard,
                    )
                elif mark == 'answer':
                    answer = self._get_answer(data) # data = question__id
                    keyboard = self._get_main_menu()
                    msg = "*Ответ:*"
                    bot.sendMessage(
                        chat_id=chat_id,
                        text=answer.text,
                        parse_mode='Markdown',
                        reply_markup=keyboard,
                    )

            else:
                bot.sendMessage(chat_id, 'I do not understand you, Sir!')
        return JsonResponse({}, status=200)

    def _get_main_menu(self):
        button_list = [[
             InlineKeyboardButton(text='Вопросы', callback_data='categories_'),
             InlineKeyboardButton(text='Каталог товаров', callback_data='catalog_'),
        ]]
        return InlineKeyboardMarkup(inline_keyboard=button_list)

    def _get_categories(self):
        mark = 'questions_'
        button_list = [[
            InlineKeyboardButton(
                text=item.name,
                callback_data=mark+item.slug),] for item in self.categories]
        return InlineKeyboardMarkup(inline_keyboard=button_list)

    def _get_questions(self, slug):
        mark = 'answer_'
        questions = self.questions.filter(category__slug=slug)
        button_list = [[
            InlineKeyboardButton(
                text=item.title,
                callback_data=mark+str(item.id)),] for item in questions]
        return InlineKeyboardMarkup(inline_keyboard=button_list)

    def _get_answer(self, question_id):
        answer = self.answers.get(question__id=question_id)
        return answer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
