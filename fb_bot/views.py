# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, requests, random, re
from pprint import pprint

from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.conf import settings

from bot.models import Category, Question, Answer
from catalog.models import ProductCategory, Product


def get_faq_categories_slugs():
        slugs = []
        for category in Category.objects.all():
            slugs.append(category.slug)
        return slugs

def get_product_categories_slugs():
        slugs = []
        for category in ProductCategory.objects.all():
            slugs.append(category.name)
        return slugs

def get_product_slugs():
        slugs = []
        for product in Product.objects.all():
            slugs.append(product.slug)
        return slugs

def get_questions_titles():
    titles = []
    for question in Question.objects.all():
        titles.append(question.title)
    #print(titles)
    return titles

params = {
        "access_token": settings.PAGE_ACCESS_TOKEN
}
headers = {
    "Content-Type": "application/json"
}
post_message_url = 'https://graph.facebook.com/v2.6/me/messages'


def post_facebook_message(fbid):
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
    print('STATUS')
    pprint(status.json())


def post_main_menu(fbid):
    response_msg = json.dumps(
        {
            "recipient": {"id": fbid},
            "message": {
                "text": "Что вас интересует???",
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
                # "attachment":{
                #     "type": "image",
                #     "payload":{
                #     "url": "http://6f28ece2.ngrok.io/media/products/shuba_PQXi2MG.jpg"
                #     }
                # }
            }
        }
    )
    status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)
    print('STATUS')
    pprint(status.json())


def post_facebook_message1(fbid, category_pk, domain, secure):
    #pr = Product.objects.all()
    #products = ProductSerializer(pr, many=True)
    print "SECURE"
    print secure
    product_list = []
    product_category = ProductCategory.objects.get(pk=category_pk)
    for product in product_category.products.all():
        product_descr = product.description if product.description else ""
        product_size = "Размер: {};".format(product.size) if product.size else ""
        product_price = "Цена: {};".format(product.price) if product.price else ""
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
                        "type": "postback",
                        "title": "Заказать",
                        "payload": "ORDER_{}".format(product.pk)
                    }
                    # {
                    #     "type": "web_url",
                    #     "title": "qw",
                    #     "url": "https://missmexx.ru/shop/product/zhiletka-iz-pestsa-tsvet-izumrud-202-75"
                    # }
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
                }
            }
        }
    )
    status = requests.post(post_message_url, params=params, headers=headers, data=response_msg)
    print('STATUS')
    pprint(status.json())


def post_product_categories(fbid):
    quick_replies = []
    for category in ProductCategory.objects.all():
        # print category.items()[0][1]
        # print category.items()[1][1]
        print category
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
    pprint(status.json())


def post_questions_categories(fbid):
    quick_replies = []
    for category in Category.objects.all():
        # print category.items()[0][1]
        # print category.items()[1][1]
        print category
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
        print "INCOMING"
        print incomming_message
        #print request.META['HTTP_HOST']
        for entry in incomming_message['entry']:
            if 'standby' in entry:
                post_facebook_message(entry['standby'][0]['sender']['id'])
                return HttpResponse()
            for message in entry['messaging']:
                if 'message' in message:
                    #pprint(message)
                    if 'quick_reply' in message['message']:
                        payload = message['message']['quick_reply']['payload']
                        print(payload)
                        if "_" in payload:
                            payload, item = payload.split("_")
                        if payload == "FAQ":
                            #cats = Category.objects.all()
                            #serialized_cats = CategorySerializer(cats, many=True)
                            post_questions_categories(message['sender']['id'])
                            return HttpResponse()
                        elif payload == "CATALOG":
                            #cats = ProductCategory.objects.all()
                            #serialized_cats = ProductCategorySerializer(cats, many=True)
                            post_product_categories(message['sender']['id'])
                        elif payload == "PCATEGORY":
                            post_facebook_message1(message['sender']['id'],
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
                        if message['message']['text'] == 'qq':
                            cat = Category.objects.get(slug='kontakty')
                            #serialized_cats = CategorySerializer(cats, many=True)
                            #print serialized_cats.data
                            for question in cat.questions.all():
                                print question
                            post_facebook_message(message['sender']['id'])
                    else:
                        #cats = Category.objects.all()
                        #serialized_cats = CategorySerializer(cats, many=True)
                        #print serialized_cats.data
                        #for category in serialized_cats.data:
                        #    print category.items()
                        #cat = Category.objects.get(slug='kontakty')
                        #serialized_cats = CategorySerializer(cats, many=True)
                        #print serialized_cats.data
                        #for question in cat.questions.all():
                        #    print question
                        post_facebook_message(message['sender']['id'])
                elif 'postback' in message:
                    if 'GET_STARTED' == message['postback']['payload']:
                        post_main_menu(message['sender']['id'])
                    else:
                        post_facebook_message(message['sender']['id'])

        return HttpResponse()


# EXAMPLES
# ----------------------------------------------------------------
# 1 шаблон кнопки
# response_msg = json.dumps(
#         {
#             "recipient": {"id": fbid},
#             "message": {
#                 "attachment": {
#                     "type": "template",
#                     "payload": {
#                         "template_type": "button",
#                         "text": "Что дальше?",
#                         "buttons": [
#                             {
#                                 "type": "postback",
#                                 "title": "Click me",
#                                 "payload": "DEV_CLICK"
#                             },
#                             {
#                                 "type": "web_url",
#                                 "title": "web CLick",
#                                 "url": "https://facebook.me"
#                             },
#                         ]
#                     }
#                 }
#             }
#         }
#     )
# --------------------------------------------------------------------
# 2 кнопки обратного вызова
# response_msg = json.dumps(
#         {
#             "recipient": {"id": fbid},
#             "message": {
#                 "text": "TEXT",
#                 "quick_replies": [
#                     {
#                         "content_type": "text",
#                         "title": "Каталог товаров",
#                         "payload": "TEXT_REPLY"
#                     },
#                     {
#                         "content_type": "text",
#                         "title": "Вопросы и Ответы",
#                         "payload": "TEXT_IMG_REPLY"
#                     }
#                 ]
#             }
#         }
#     )
# -----------------------------------------------------------------------
# 3 open graph
# message:
# "attachment":{
#       "type":"template",
#       "payload":{
#         "template_type":"open_graph",
#         "elements":[
#            {
#             "url":"https://open.spotify.com/track/7GhIk7Il098yCjg4BQjzvb",
#             "buttons":[
#               {
#                 "type":"web_url",
#                 "url":"https://en.wikipedia.org/wiki/Rickrolling",
#                 "title":"View More"
#               }              
#             ]      
#           }
#         ]
#       }
#     }
# --------------------------------------------------------------------------
# 4 direct call
# message:
#            "attachment":{
#       "type":"template",
#       "payload":{
#         "template_type": "button",
#         "text": "CALL",
#         "buttons":[
#            {
#             "type":"phone_number",
#             "title": "Call me",
#             "payload": "+380950968326"
#           }
#         ]
#         }
#     }
# 5
# LIST
# "attachment": {
#      "type": "template",
#      "payload": {
#        "template_type": "list",
#        "top_element_style": "compact",
#        "elements": [
#          {
#                     "title": "Classic Black T-Shirt",
#                     "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTKtYBBr8doTiJ7TjTwLgXAq_G7QDZ4HtbWoeWcsi0_ghBHap_QGVdr9k",
#                     "subtitle": "100% Cotton, 200% Comfortable",
#                     "buttons": [
#                         {
#                             "title": "Buy",
#                             "type": "web_url",
#                             "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTKtYBBr8doTiJ7TjTwLgXAq_G7QDZ4HtbWoeWcsi0_ghBHap_QGVdr9k",
#                         }
#                     ]                
#                 },
#                 {
#                     "title": "Classic Black T-Shirt",
#                     "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTKtYBBr8doTiJ7TjTwLgXAq_G7QDZ4HtbWoeWcsi0_ghBHap_QGVdr9k",
#                     "subtitle": "100% Cotton, 200% Comfortable",
#                     "buttons": [
#                         {
#                             "title": "Buy",
#                             "type": "web_url",
#                             "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTKtYBBr8doTiJ7TjTwLgXAq_G7QDZ4HtbWoeWcsi0_ghBHap_QGVdr9k",
#                         }
#                     ]                
#                 },
#        ],
#        "buttons": [
#                 {
#                     "title": "View More",
#                     "type": "postback",
#                     "payload": "NEXT_DEV_APP"                        
#                 }
#             ]  
#      }
#    }