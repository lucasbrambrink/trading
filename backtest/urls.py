from django.conf.urls import patterns, include, url
from django.contrib import admin
from backtest.views import *

urlpatterns = patterns('',
	url(r'^$', RootView.as_view(), name='root'),
)
