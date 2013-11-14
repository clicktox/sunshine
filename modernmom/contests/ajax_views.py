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
#from django.core.urlresolvers import reverse
from subdomains.utils import reverse
from django.core import serializers
from django.template.defaultfilters import slugify

from contests.models import *


def list(request,template="contests/ajax/list.html",extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    context['contests'] = Contest.objects.all()
    return render_to_response(template,context,context_instance=RequestContext(request))
   