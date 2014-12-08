from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView
from registration.forms import UserCreateForm


urlpatterns = patterns('',
	url(r'^register/$', CreateView.as_view(
		template_name = 'registration/create.html',
		form_class = UserCreateForm,
		success_url = '/twitter/'), name='register'),
	url(r'^', include('django.contrib.auth.urls')),
)

