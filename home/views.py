from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.generic.base import TemplateView

from account.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'


class MyAlgorithmView(TemplateView):
    template_name = 'home/root.html'