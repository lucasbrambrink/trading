from django.conf.urls import patterns, include, url
from django.contrib import admin

from graph_trader.views import LoginView


urlpatterns = patterns('',
    url(r'^auth', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^account/login', LoginView.as_view(), name='account_login'),
    url(r'^account/', include('account.urls')),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social', app_name='python-social-auth')),
    url(r'^builder/', include('algo_builder.urls', namespace='builder', app_name='algo_bulider')),
    url(r'^backtest/', include('backtest.urls', namespace='backtest-runner', app_name='backtest')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('home.urls', namespace='homepage', app_name='home')),
)
