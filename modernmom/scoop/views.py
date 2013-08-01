# Create your views here.
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
from forms import *
def home(request,template="scoop/homepage.html",extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    context['SCOOP_TOPICS'] = ScoopTopic.objects.all()
    if request.user.is_staff:
        ADMIN_FORMS = {}
        
        add_topic_form = ScoopTopicForm()
        ADMIN_FORMS['add_topic'] = add_topic_form
        
        if request.method == 'POST':
            add_topic_form = ScoopTopicForm(request.POST)
            if add_topic_form.is_valid():
                topic = add_topic_form.save()
                return HttpResponseRedirect('/scoop/')
        context['ADMIN_FORMS'] = ADMIN_FORMS
        
    return render_to_response(template,context,context_instance=RequestContext(request))# Create your views here.
