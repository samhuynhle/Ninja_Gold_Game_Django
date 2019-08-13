from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'cave$', views.cave),
    url(r'casino$', views.casino),
    url(r'dojo$', views.dojo),
    url(r'farm$', views.farm),
    url(r'reset$',views.reset),
    url(r'^anything$', views.reset),
    url(r'^rules$', views.rules)
]