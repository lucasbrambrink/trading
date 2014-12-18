from django.conf.urls import patterns, include, url
from backtest.views import *


urlpatterns = patterns('',
    url(r'^run/(?P<algo_id>[0-9a-zA-Z]{32})$', RunView.as_view(), name='run'),
    #url(r'^realtime/(?P<backtest_id>[0-9a-zA-Z]{32})/(?P<num>[0-9]+)/', realtime, name='realtime'),
    # url(r'^history/$', list all algorithms)
    # url(r'^history/(?P<algo_id>[0-9a-zA-Z]{32})/$', list all backtests)
    # url(r'^history/(?P<algo_id>[0-9a-zA-Z]{32})/(?P<backtest_id>[0-9a-zA-Z]{32})$', show backtest result)
)
