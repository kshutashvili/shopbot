from django.conf.urls import url
from django.contrib import admin

from .views import CommandReceiveView

urlpatterns = [
    url(r'^$', CommandReceiveView.as_view(), name='command'),
]
