from django.conf.urls import url

from .views import CommandReceiveView

urlpatterns = [
    url(r'^$', CommandReceiveView.as_view()),
]
