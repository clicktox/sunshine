import datetime
import re

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
from articles.models import Article
from featured_content.models import FeaturedItem

def home(request,template="homepage.html",extra_context=None):
    context={}
   
    if extra_context is not None:
        context.update(extra_context)
    context['latest'] = Article.objects.approved()[0:6]
    fi = FeaturedItem.objects.filter(feature_date=datetime.datetime.today()).order_by('-priority')
    context['featured_items'] = fi if fi.count() > 0 else FeaturedItem.objects.all().order_by('-feature_date', '-priority')[0:10]
    #if request.user.is_authenticated():
    #    return dashboard(request)
    return render_to_response(template,context,context_instance=RequestContext(request))

@login_required
def dashboard(request,template="homepage_authenticated.html",extra_context=None):
    context={}
   
    if extra_context is not None:
        context.update(extra_context)
    if hasattr(request.user,'is_verified'): 
        pass
    return render_to_response(template,context,context_instance=RequestContext(request))

def scoop(request,template="homepage.html",extra_context=None):
    context={}
   
    if extra_context is not None:
        context.update(extra_context)
    
    if request.user.is_authenticated():
        if hasattr(request.user,'is_verified'): 
            return dashboard(request)
        return HttpResponse('We need more info %s' % request.user.username)
    return render_to_response(template,context,context_instance=RequestContext(request))


def toolbox(request,template="homepage.html",extra_context=None):
    context={}
   
    if extra_context is not None:
        context.update(extra_context)
    
    if request.user.is_authenticated():
        if hasattr(request.user,'is_verified'): 
            return dashboard(request)
        return HttpResponse('We need more info %s' % request.user.username)
    return render_to_response(template,context,context_instance=RequestContext(request))