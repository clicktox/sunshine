
import datetime
import re
import urlparse 

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.core import serializers
from django.template.defaultfilters import slugify

from django_twitter.models import *
from tweepy.parsers import Parser

import tweepy
from django.core.context_processors import csrf
import json
 
class RawJsonParser(Parser):
 
    def parse(self, method, payload):
        return payload



 
 
def authorize_twitter_user(request,appid):
    app = get_object_or_404(Application,appid=appid)
    
    # URL to where we will redirect to
    redirect_url = u'%s%s' % (settings.SITE_URL,reverse('twitter_authorize_url_callback',args=[app.appid]))
    
    # create the handler
    auth = tweepy.OAuthHandler(app.consumer_key.encode('ascii'), app.consumer_secret.encode('ascii'), redirect_url)
    
    # get the authorization url (i.e. https://api.twitter.com/oauth/authorize?oauth_token=XXXXXXX)
    # this method automatically grabs the request token first
    # Note: must ensure a callback URL (can be any URL) is defined for the application at dev.twitter.com,
    #       otherwise this will fail (401 Unauthorized)
    try:
        url = auth.get_authorization_url()
    except tweepy.TweepError as e:
        return HttpResponse(e)
    
    # store the returned values
    request.session['twitter_request_token_key'] = auth.request_token.key
    request.session['twitter_request_token_secret'] = auth.request_token.secret
    
    return HttpResponseRedirect(url)

def verify(request):
    # Twitter will direct with oauth_token and oauth_verifier in the URL
    # ?oauth_token=EoSsg1...&oauth_verifier=NB3bvAkb...
    
    # did the user deny the request
    if 'denied' in request.GET:
        return False
    
    # ensure we have a session state and the state value is the same as what twitter returned
    if 'twitter_request_token_key' not in request.session \
       or 'oauth_token' not in request.GET \
       or 'oauth_verifier' not in request.GET \
       or request.session['twitter_request_token_key'] != request.GET['oauth_token']:
        return False
    else:
        return True

def authorize_twitter_user_callback(request,appid):
    app = get_object_or_404(Application,appid=appid)
 
    data = {}
    if (not verify(request) ):
        return HttpReponse('Verification Failed...')
    
    # create the connection
    auth = tweepy.OAuthHandler(app.consumer_key.encode('ascii'), app.consumer_secret.encode('ascii'))
    
    # set the token and verifier
    auth.set_request_token(request.GET['oauth_token'], request.GET['oauth_verifier'])
    
    # determine if we've already requested an access token
    if 'twitter_access_token_key' not in request.session:
    
        # get the access token
        access_token = auth.get_access_token(request.GET['oauth_verifier'])
    
        # update the stored values
        request.session['twitter_access_token_key'] = access_token.key
        request.session['twitter_access_token_secret'] = access_token.secret
    
    else:
    
        # set the access token
        auth.set_access_token(request.session['twitter_access_token_key'], request.session['twitter_access_token_secret'])
    
    try:
        ua = UserApplicationAccess.objects.get(application = app,user=request.user)
        ua.access_token=request.session['twitter_access_token_key']
        ua.access_token_secret=request.session['twitter_access_token_secret']
        ua.save()
    
    except UserApplicationAccess.DoesNotExist:
        ua = UserApplicationAccess(application = app,user=request.user,access_token=request.session['twitter_access_token_key'],access_token_secret=request.session['twitter_access_token_secret'])
        ua.save()
    
    #profile
    # create the API instance
    api = tweepy.API(auth_handler=auth, parser=RawJsonParser())
    user = json.loads(api.me())
    
    try:
        tp = TwitterProfile.objects.get(id = user['id'])
    except TwitterProfile.DoesNotExist:
        tp = TwitterProfile(id = user['id'])
    tp.screen_name = user['screen_name']
    tp.name = user['name']
    tp.location = user['location']
    tp.raw =user
    tp.save()
    
    ua.profile = tp
    ua.save()
    
    return HttpResponseRedirect(reverse('home'))