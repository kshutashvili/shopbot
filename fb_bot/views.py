# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, requests
from pprint import pprint

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from bot.models import Category, Question, Answer
from catalog.models import ProductCategory, Product
from orders.forms import OrderForm
from orders.models import Order


params = {
        "access_token": settings.PAGE_ACCESS_TOKEN
}
headers = {
    "Content-Type": "application/json"
}
post_message_url = 'https://graph.facebook.com/v2.6/me/messages'


def post_main_menu(fbid):
    response_msg = json.dumps(
        {
            "recipient": {"id": fbid},
            "message": {
                "text": "Что вас интересует?",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "Каталог товаров",
                        "payload": "CATALOG_PAYLOAD"
                    },
                    {
                        "content_type": "text",
                        "title": "Вопросы и Ответы",
                        "payload": "FAQ_PAYLOAD"
                    }
                ]
            }
        }
    )
    status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)
    #pprint(status.json())


def post_product_list(fbid, category_pk, domain, secure):
    product_list = []
    product_category = ProductCategory.objects.get(pk=category_pk)
    if product_category.products.count() < 1:
        response_msg = json.dumps(
            {
                "recipient": {"id": fbid},
                "message": {
                    "text": "В данный момент, в этой категории нет ни одного товара\n\nЧто еще вас может заинтересовать?",
                    "quick_replies": [
                        {
                            "content_type": "text",
                            "title": "Каталог товаров",
                            "payload": "CATALOG_PAYLOAD"
                        },
                        {
                            "content_type": "text",
                            "title": "Вопросы и Ответы",
                            "payload": "FAQ_PAYLOAD"
                        }
                    ]
                }
            }
        )
        status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)
        return
    for product in product_category.products.all():
        product_descr = product.description if product.description else ""
        product_size = "Размер: {};".format(product.size) if product.size else ""
        product_price = "Цена: {} руб.;".format(product.price) if product.price else ""
        for product_attr in product.attributes.all():
            product_attrs = "{}: {};".format(product_attr.name,
                                             product_attr.value)

        if secure:
            product_photo_url = "https://{}{}".format(domain, product.photo.url)
        else:
            product_photo_url = "http://{}{}".format(domain, product.photo.url)

        product_list.append(
            {
                "title": product.name,
                "image_url": product_photo_url,
                "subtitle": "{0}\n{1} {2} {3}".format(
                        product_descr,
                        product_size,
                        product_price,
                        product_attrs
                    ),
                "default_action": {
                    "type": "web_url",
                    "url": product.external_link
                },
                "buttons":[
                    {
                        "type": "web_url",
                        "title": "Заказать",
                        "url": "https://{}/fb_bot/order/{}".format(domain, product.pk),
                        "webview_height_ratio": "tall"
                    }
                ]
            }
        )
    response_msg = json.dumps(
        {
            "recipient": {"id": fbid},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "image_aspect_ratio": "square",
                        "elements": product_list
                    }
                },
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "Каталог товаров",
                        "payload": "CATALOG_PAYLOAD"
                    },
                    {
                        "content_type": "text",
                        "title": "Вопросы и Ответы",
                        "payload": "FAQ_PAYLOAD"
                    }
                ]
            }
        }
    )
    status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)


def post_product_categories(fbid):
    quick_replies = []
    for category in ProductCategory.objects.all():
        quick_replies.append({
            "content_type": "text",
            "title": category.name,
            "payload": "PCATEGORY_{}".format(category.pk)
        })
    response_msg = json.dumps(
        {
            "recipient": {"id": fbid},
            "message": {
                "text": "Выберите категорию",
                "quick_replies": quick_replies
            }
        }
    )
    status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)
    #pprint(status.json())


def post_questions_categories(fbid):
    quick_replies = []
    for category in Category.objects.all():
        quick_replies.append({
            "content_type": "text",
            "title": category.name,
            "payload": "QCATEGORY_{}".format(category.pk)
        })
    response_msg = json.dumps(
        {
            "recipient": {"id": fbid},
            "message": {
                "text": "Выберите категорию",
                "quick_replies": quick_replies
            }
        }
    )
    status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)
    pprint(status.json())


def post_questions(fbid, category_pk):
    quick_replies = []
    current_category = Category.objects.get(pk=category_pk)
    if current_category.questions.count() < 1:
        response_msg = json.dumps(
            {
                "recipient": {"id": fbid},
                "message": {
                    "text": "В данный момент, в этой категории нет ни одного вопроса\n\nЧто еще вас может заинтересовать?",
                    "quick_replies": [
                        {
                            "content_type": "text",
                            "title": "Каталог товаров",
                            "payload": "CATALOG_PAYLOAD"
                        },
                        {
                            "content_type": "text",
                            "title": "Вопросы и Ответы",
                            "payload": "FAQ_PAYLOAD"
                        }
                    ]
                }
            }
        )
        status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)
        return
    for question in current_category.questions.all():
        quick_replies.append({
            "content_type": "text",
            "title": question.title,
            "payload": "QUESTION_{}".format(question.pk)
        })
    response_msg = json.dumps(
        {
            "recipient": {"id": fbid},
            "message": {
                "text": "Выберите вопрос",
                "quick_replies": quick_replies
            }
        }
    )
    status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)


def post_answer(fbid, question_pk):
    quick_replies = []
    answer = Answer.objects.get(question__pk=question_pk)
    response_msg = json.dumps(
        {
            "recipient": {"id": fbid},
            "message": {
                "text": answer.text,
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "Каталог товаров",
                        "payload": "CATALOG_PAYLOAD"
                    },
                    {
                        "content_type": "text",
                        "title": "Вопросы и Ответы",
                        "payload": "FAQ_PAYLOAD"
                    }
                ]
            }
        }
    )
    status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)


class MessengerBot(generic.View):

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == settings.MESSENGER_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse("Error, invalid token")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incomming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incomming_message['entry']:
            if 'standby' in entry:
                post_main_menu(entry['standby'][0]['sender']['id'])
                return HttpResponse()
            for message in entry['messaging']:
                if 'message' in message:
                    if 'quick_reply' in message['message']:
                        payload = message['message']['quick_reply']['payload']
                        if "_" in payload:
                            payload, item = payload.split("_")
                        if payload == "FAQ":
                            post_questions_categories(message['sender']['id'])
                            return HttpResponse()
                        elif payload == "CATALOG":
                            post_product_categories(message['sender']['id'])
                        elif payload == "PCATEGORY":
                            post_product_list(message['sender']['id'],
                                                   item,
                                                   request.META['HTTP_HOST'],
                                                   request.is_secure())
                        elif payload == "QCATEGORY":
                            post_questions(message['sender']['id'], item)
                        elif payload == "QUESTION":
                            post_answer(message['sender']['id'], item)
                        elif payload == 'BOT_START':
                            post_main_menu(message['sender']['id'])

                    elif 'text' in message['message']:
                        post_main_menu(message['sender']['id'])
                    else:
                        post_main_menu(message['sender']['id'])
                elif 'postback' in message:
                    if 'GET_STARTED' == message['postback']['payload']:
                        post_main_menu(message['sender']['id'])
                    else:
                        post_main_menu(message['sender']['id'])
        return HttpResponse()


class OrderView(generic.CreateView):
    model =Order
    template_name = "fb_bot/order.html"
    form_class = OrderForm
    success_url = "fb/order/success"

    def get_initial(self):
        product_pk = self.kwargs.get('product_pk')
        product = get_object_or_404(Product, pk=product_pk)
        return {
            'product': product
        }


class OrderSuccessView(generic.TemplateView):
    template_name = "fb_bot/order_success.html"
