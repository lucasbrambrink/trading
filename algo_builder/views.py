from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView


from uuid import uuid1

def UUIDView(request):
    id = uuid1().hex
    return redirect(reverse('builder:builder', kwargs={'id': id}))


class BuilderView(TemplateView):
    template_name = 'algo_builder/builder.html'

    def get_context_data(self, **kwargs):
        content = super(BuilderView, self).get_context_data(**kwargs)
        content['id'] = self.kwargs.get('id', None)
        return content
