from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', include('home.urls', namespace='homepage', app_name='home')),
    url(r'^builder/', include('algo_builder.urls', namespace='builder-app', app_name='algo_bulider')),
    url(r'^backtest/', include('backtest.urls', namespace='backtest-app', app_name='backtest')),
    url(r'^admin/', include(admin.site.urls)),
)
