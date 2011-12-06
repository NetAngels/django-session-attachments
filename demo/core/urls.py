# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from demo.core import views


urlpatterns = patterns('',
    url(r'^$', views.hello, name='core-hello'),
)
