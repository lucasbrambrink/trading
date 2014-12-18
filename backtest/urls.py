from django.conf.urls import patterns, include, url
from backtest.views import *


urlpatterns = patterns('',
    url(r'^run/(?P<algo_id>[0-9a-zA-Z]{32})$', RunView.as_view(), name='run'),
    url(r'^realtime/(?P<backtest_id>[0-9a-zA-Z]{32})/(?P<num>[0-9]+)/', realtime_view, name='realtime'),
    url(r'^assets/(?P<backtest_uuid>[0-9a-zA-Z]{32})/$', AssetsList.as_view(), name='asset_list'),
    url(r'^assets/(?P<backtest_uuid>[0-9a-zA-Z]{32})/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})$', AssetsDateList.as_view(), name='asset_date_list'),
    # url(r'^history/$', list all algorithms)
    # url(r'^history/(?P<algo_id>[0-9a-zA-Z]{32})/$', list all backtests)
    # url(r'^history/(?P<algo_id>[0-9a-zA-Z]{32})/(?P<backtest_id>[0-9a-zA-Z]{32})$', show backtest result)
)
