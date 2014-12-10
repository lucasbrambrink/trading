from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.generic.base import TemplateView


class RootView(TemplateView):
    template_name = 'home/root.html'