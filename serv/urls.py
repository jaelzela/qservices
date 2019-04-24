from django.conf.urls import url

from serv import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^([0-9]+)/reviews$', views.reviews, name='index'),
]
