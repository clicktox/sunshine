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
from cissonius.models import *

def home(request,template="homepage.html",extra_context=None):
    context={}
    
    if extra_context is not None:
        context.update(extra_context)
    #context['blogs'] = MemberBlog.objects.all()
    context['lisa'] = Product.objects.filter(productmusthave__user__username='lisa')
    context['new_products'] = Product.objects.all()[0:5]
    context['giftguides'] = GiftGuide.objects.all()
    
    return render_to_response(template,context,context_instance=RequestContext(request))
