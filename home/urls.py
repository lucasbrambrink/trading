from django.conf.urls import patterns, include, url
from django.contrib import admin
from home.views import *

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^account/myalgorithm/', MyAlgorithmView.as_view(), name='myalgorithm')
)
