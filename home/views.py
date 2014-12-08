from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.generic.base import View

# Create your views here.

class RootView(View):
	template_name = 'home/root.html'
	
	def get(self,request):
		return render(request, self.template_name)

	def post(self,request):
		pass
