# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json
import pickle
import telepot
from slugify import slugify
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery, PhotoSize, Contact, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove

from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from rest_framework.renderers import JSONRenderer

from bot.models import Question, Answer, Category
from catalog.models import ProductCategory, ProductAttributes, Product
from orders.models import Order


bot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)
bot.setWebhook(settings.WEBHOOK_URL)


class CommandReceiveView(View):
    categories = Category.objects.all()
    questions = Question.objects.all()
    answers = Answer.objects.all()
    product_categories = ProductCategory.objects.all()
    products = Product.objects.all()
    attributes = ProductAttributes.objects.all()
    order = 'telegram_bot/templates/order/order_{}.txt'

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
            callback_data = update.get('data')
            contact = update['message'].get('contact')
            if contact:
                phone_number = contact['phone_number']
                with open(self.order.format(chat_id), 'a+') as file:
                    if len(file.readlines()) < 2:
                        file.write(phone_number)
                    file.close()
                with open(self.order.format(chat_id), 'r') as file:
                    order = ""
                    c = 0
                    for line in file:
                        c = c + 1
                        if c == 1:
                            order = line.strip()
                    file.close()

                    if order != "":
                        keyboard = ReplyKeyboardRemove()
                        bot.sendMessage(
                            chat_id=chat_id,
                            text="Спасибо!",
                            reply_markup=keyboard,
                        )
                        product = Product.objects.get(id=order)
                        msg = "Подтвердите Ваш заказ:\nАртикул продукта: {},\nНомер телефона: {}"
                        keyboard = self._confirmation()
                        bot.sendMessage(
                            chat_id=chat_id,
                            text=msg.format(product.code, phone_number),
                            reply_markup=keyboard,
                        )

            if command == '/help':
                bot.sendMessage(chat_id, '*TODO: help*', parse_mode='Markdown')

            elif command == '/start':
                keyboard = self._get_main_menu()
                msg = "*Вас приветствует бот Unlured, что Вас интересует?*"
                bot.sendMessage(
                    chat_id=chat_id,
                    text=msg,
                    parse_mode='Markdown',
                    reply_markup=keyboard,
                )


            elif callback_data:
                if callback_data == "confirmed":
                    try:
                        with open(self.order.format(chat_id), 'r') as file:
                            product_id, phone_number = "", ""
                            c = 0
                            for line in file:
                                c = c + 1
                                if c == 1:
                                    product_id = line.strip()
                                if c == 2:
                                    phone_number = line
                            file.close()
                        order = self._create_an_order(product_id, phone_number)
                        keyboard = self._get_main_menu()
                        msg = "*Ваш заказ принят! Номер заказа: {}*"
                        bot.sendMessage(
                            chat_id=chat_id,
                            text=msg.format(order.id),
                            parse_mode='Markdown',
                            reply_markup=keyboard,
                        )
                        path = os.path.join(
                                os.path.abspath(os.path.dirname(__file__)),
                                'templates/order/order_{}.txt')
                        os.remove(path.format(chat_id))
                    except IOError as e:
                        keyboard = self._get_main_menu()
                        msg = "*Ваш заказ уже подтвержден!*"
                        bot.sendMessage(
                            chat_id=chat_id,
                            text=msg,
                            parse_mode='Markdown',
                            reply_markup=keyboard,
                        )

                else:
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
                        keyboard = self._get_product_category()
                        msg = "*Выберите категорию товара:*"
                        bot.sendMessage(
                            chat_id=chat_id,
                            text=msg,
                            parse_mode='Markdown',
                            reply_markup=keyboard,
                        )
                    elif mark == 'products':

                        products = self.products.filter(category__id=data)
                        for item in products:
                            attrs = self.attributes.filter(products=item)
                            link = ""
                            if item.external_link != "":
                                link = '\n\U0001F4CE {}'.format(
                                        item.external_link)
                            name_price = '{}\nЦена: {} руб\n'.format(
                                          item.name, item.price)
                            attrs_str = '\n'.join([attr.name + ": " + \
                                        attr.value for attr in attrs])
                            bot.sendPhoto(
                                chat_id=chat_id,
                                caption='{}{}{}'.format(name_price, attrs_str, link),
                                photo=item.photo,
                                reply_markup=self._get_product_menu(item.id),
                            )
                        keyboard = self._get_main_menu()
                        msg = 'Появились вопросы? Хотите просмотреть каталог?'
                        bot.sendMessage(
                            chat_id=chat_id,
                            text=msg,
                            reply_markup=keyboard,
                        )
                    elif mark == 'order':
                        with open(self.order.format(chat_id), 'w') as order:
                            order.write(str(data)+"\n")
                            order.close()
                        keyboard = self._get_phone()
                        bot.sendMessage(
                            chat_id=chat_id,
                            text="*Для заказа требуется Ваш номер телефона*",
                            parse_mode='Markdown',
                            reply_markup=keyboard,
                        )

                    elif mark == 'questions':
                        # data: category__slug
                        keyboard = self._get_questions(data)
                        msg = "*Выберите вопрос:*"
                        bot.sendMessage(
                            chat_id=chat_id,
                            text=msg,
                            parse_mode='Markdown',
                            reply_markup=keyboard,
                        )
                    elif mark == 'answer':
                        # data: question__id
                        answer = self._get_answer(data)
                        keyboard = self._get_main_menu()
                        msg = "*Ответ:*"
                        bot.sendMessage(
                            chat_id=chat_id,
                            text=answer.text,
                            parse_mode='Markdown',
                            reply_markup=keyboard,
                        )

            else:

                keyboard = self._get_main_menu()
                msg = "Появились вопросы? Хотите просмотреть каталог?"
                bot.sendMessage(
                            chat_id=chat_id,
                            text=msg,
                            reply_markup=keyboard,
                        )
        return JsonResponse({}, status=200)

    def _get_main_menu(self):
        button_list = [[
            InlineKeyboardButton(
                text='Вопросы',
                callback_data='categories_'
            ),
            InlineKeyboardButton(
                text='Каталог товаров',
                callback_data='catalog_'
            ),
        ]]
        return InlineKeyboardMarkup(inline_keyboard=button_list)

    def _get_product_menu(self, product_id):
        button_list = [[
            # InlineKeyboardButton(
            #     text='Просмотреть',
            #     callback_data='view_'+str(product_id)
            # ),
            InlineKeyboardButton(
                text='Заказ',
                callback_data='order_'+str(product_id)
            ),
        ]]
        return InlineKeyboardMarkup(inline_keyboard=button_list)

    def _get_phone(self):
        button_list = [[
            KeyboardButton(
                text='Отправить номер телефона',
                request_contact=True
            ),
        ]]
        return ReplyKeyboardMarkup(
                    keyboard=button_list,
                    resize_keyboard=True,
                    one_time_keyboard=True)

    def _confirmation(self):
        button_list = [[
            InlineKeyboardButton(
                text='Подтвердить заказ',
                callback_data='confirmed')
        ]]
        return InlineKeyboardMarkup(inline_keyboard=button_list)

    def _get_categories(self):
        mark = 'questions_'
        button_list = [[
            InlineKeyboardButton(
                text=item.name,
                callback_data=mark + item.slug),] for item in self.categories]
        return InlineKeyboardMarkup(inline_keyboard=button_list)

    def _get_questions(self, slug):
        mark = 'answer_'
        questions = self.questions.filter(category__slug=slug)
        button_list = [[
            InlineKeyboardButton(
                text=item.title,
                callback_data=mark + str(item.id)),] for item in questions]
        return InlineKeyboardMarkup(inline_keyboard=button_list)

    def _get_answer(self, question_id):
        return self.answers.get(question__id=question_id)

    def _get_product_category(self):
        mark = 'products_'
        button_list = [[
            InlineKeyboardButton(
                text=item.name,
                callback_data=mark + \
                str(item.id)),] for item in self.product_categories]
        return InlineKeyboardMarkup(inline_keyboard=button_list)

    def _create_an_order(self, product_id, phone_number):
        order = Order.objects.create(
            product_id=product_id,
            customer_phone=phone_number,
        )
        return order

    # def _get_products(self, category_id):
    #     mark = 'product_' # после нажатия на продукт, вывести его в
    #     products = self.products.filter(category__id=category_id)
    #     attrs = self.attributes.filter(products__in=products)
    #     button_list = [[
    #         InlineKeyboardButton(
    #             text='{} {}'.format(item.name, ', '.join([item.name + ": " + item.value for item in attrs])),
    #             callback_data=mark+str(item.id)),
    #     ] for item in products]
    #     return InlineKeyboardMarkup(inline_keyboard=button_list)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
