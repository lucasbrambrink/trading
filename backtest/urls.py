from django.conf.urls import patterns, include, url
from django.contrib import admin
from backtest.views import *

urlpatterns = patterns('',
    url(r'^$', RootView.as_view(), name='root'),
    url(r'^run/', run, name='run'),
    url(r'^result/(?P<id>[0-9a-zA-Z]+)/$', ResultView.as_view(), name='result'),
    url(r'^result/(?P<id>[0-9a-zA-Z]+)/(?P<num>[0-9]+)/', data, name='data')
)
