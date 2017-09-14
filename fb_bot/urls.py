from django.conf.urls import url, include

from .views import MessengerBot, OrderView, OrderSuccessView


urlpatterns = [
    url(r'109380fccb6b8d326be3a6ac201f16ac1a8381d3efa49c5752/$', MessengerBot.as_view()),
    url(r'order/(?P<product_pk>[\d]+)/$', OrderView.as_view()),
    url(r'order/success/$', OrderSuccessView.as_view())
]