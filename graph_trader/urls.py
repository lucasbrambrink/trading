from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'backtest/', include('backtest.urls', namespace='backtest')),
    # url(r'^admin/', include(admin.site.urls)),
)
