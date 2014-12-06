from django.conf.urls import patterns, include, url
from django.contrib import admin
from backtest.views import *

urlpatterns = patterns('',
	(r'^home/', RootView.as_view(), name='root'),
)
