from django.conf.urls import patterns, include, url
from algo_builder.views import *

urlpatterns = patterns('',
    url(r'^$', uuid_view, name='uuid'),
    url(r'^create_json/$', JsonBuilder.as_view(), name='json_builder'),
    url(r'^new/(?P<algo_id>[0-9a-zA-Z]{32})/$', NewView.as_view(), name='new'),
    url(r'^save/$', save_view, name='save')
    #ulr(r'^/update/(?P<id>[0-9a-zA-Z]{32})/$', UpdateView.as_view(), name='update')
)
