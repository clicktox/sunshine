# Create your views here.
import datetime
import re

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.core import serializers
from django.template.defaultfilters import slugify
from taxonomy.models import *
from forms import *


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


def scoop_home(request,template="scoop/homepage.html",extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    context['scoop_list'] = Scoop.objects.all()
    return render_to_response(template,context,context_instance=RequestContext(request))# Create your views here.


@staff_member_required
def scoop_add_item(request,slug=None,template='scoop/scoopitem/add.html',extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    form = ScoopItemForm(request.POST)
    if request.method == 'POST':
        if (not slug == None):
            scoop = get_object_or_404(Scoop,slug=slug)
        else:
            if not 'scoop_slug' in request.POST:
                raise Http404
            scoop = get_object_or_404(Scoop,slug=request.POST['scoop_slug'])
        if form.is_valid():
            article = form.save(commit=False)
            article.creator = request.user
            article.save()
            scoop_item,c = ScoopItem.objects.get_or_create( scoop=scoop,
                                                            content_type = ContentType.objects.get_for_model(article),
                                                            object_id=article.pk)
            return HttpResponseRedirect(article.get_absolute_url)
    context['form'] = form
    return render_to_response(template,context,context_instance=RequestContext(request))
        