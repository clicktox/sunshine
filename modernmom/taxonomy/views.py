# Create your views here.
import datetime
import re

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.views.generic import date_based, list_detail
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.core import serializers
from django.template.defaultfilters import slugify
from taxonomy.models import *

def category_list(request,template="taxonomy/category/list.html",extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    #In templatecontext we already load all the top level categories, no need to ping it again...
    return render_to_response(template,context,context_instance=RequestContext(request))

def category_detail(request,slug,parent=None,template="taxonomy/category/detail.html",extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    if parent:
        parent = get_object_or_404(Category,slug=parent,parent=None)
        template = "taxonomy/subcategory/detail.html"
    context['category'] = get_object_or_404(Category,slug=slug,parent=parent)
    return render_to_response(template,context,context_instance=RequestContext(request))