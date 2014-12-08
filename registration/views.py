from django.shortcuts import render,redirect
from django.views.generic.base import View
from app.settings import APP_KEY, APP_SECRET
from registration.models import User
from django.http import JsonResponse
# Create your views here.

from twython import Twython


def connect_to_twitter(request):
	twitter = Twython(APP_KEY, APP_SECRET)
	auth = twitter.get_authentication_tokens(callback_url='obscure-peak-4545.herokuapp.com/twitter/callback')
	OAUTH_TOKEN = auth['oauth_token']
	OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
	authentication_url = auth['auth_url']
	request.session['oauth_token'] = OAUTH_TOKEN
	request.session['oauth_token_secret'] = OAUTH_TOKEN_SECRET
	print(authentication_url)
	return redirect(authentication_url)

def callback(request):
	## get verifier ##
	OAUTH_VERIFIER = request.GET['oauth_verifier']
	
	## set up twitter as Twyton instance
	twitter = Twython(APP_KEY, APP_SECRET, request.session['oauth_token'], request.session['oauth_token_secret'])
	
	## get new tokens and secret ##
	authorized_tokens = twitter.get_authorized_tokens(OAUTH_VERIFIER)
	
	## redefine tokens ##
	request.session['oauth_token'] = authorized_tokens['oauth_token']
	request.session['oauth_token_secret'] = authorized_tokens['oauth_token_secret']
	return redirect('oauth:tweet')

class Tweet(View):

	def get(self,request):
		twitter = Twython(APP_KEY, APP_SECRET, request.session['oauth_token'], request.session['oauth_token_secret'])
		user_info = twitter.verify_credentials()
		name = user_info['name']
		first_name,last_name = name.split(' ')
		username = user_info['screen_name']
		test = User.objects.filter(username=username)
		if len(test) == 0:
			User.objects.create(first_name = first_name,
				 last_name=last_name,
				 username=username, 
				 oauth_token=request.session['oauth_token'],
				 oauth_token_secret=request.session['oauth_token_secret'])
			user = User.objects.get(username=username)
		else:
			user = User.objects.get(username=username)
			setattr(user, 'oauth_token', request.session['oauth_token'])
			setattr(user, 'oauth_token_secret', request.session['oauth_token_secret'])
			user.save()
		request.session['user_id'] = user.id
		return render(request, 'oauth/index.html', {'user': user})


class Send(View):
	def get(self,request):
		pass

	def post(self,request):
		tweet = request.POST['tweet']
		if len(tweet) > 140:
			new_tweet = ""
			a = 0 
			while a < 122:
				new_tweet += tweet[a]
				a += 1
			new_tweet += " and I like butts"
			tweet = new_tweet
		twitter = Twython(APP_KEY, APP_SECRET, request.session['oauth_token'], request.session['oauth_token_secret'])
		twitter.update_status(status=tweet)
		return JsonResponse({'tweet' : tweet})


def all_tweets(request):
	nothing = 'no'
	## this is where I would fetch them from the DB
	return JsonResponse({'nothing' : nothing })


	