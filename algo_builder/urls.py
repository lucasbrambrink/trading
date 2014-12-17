from django.conf.urls import patterns, include, url
from django.contrib import admin
from algo_builder.views import *

urlpatterns = patterns('',
    url(r'^$', UUIDView, name='uuid'),
    url(r'^create_json/$', JsonBuilder.as_view(), name='json_builder'),
    url(r'^(?P<id>[0-9a-zA-Z]+)/', BuilderView.as_view(), name='builder'),
)
