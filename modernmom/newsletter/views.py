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

from python_constantcontact import cc

def subscribe(request,template="newsletter/subscribe.html",extra_context=None):
    context={}
    api = cc.Api(api_key="v37mw649kkhhxsynq9e7fcrt", username="seedwithroot@gmail.com", password="C0nst@ntC0nt@ct")
    # should return a 201 CREATED response status code
    #response, body = api.create_contact("justin@modernmom.com", [2,3])
    response, body = api.create_contact("seedwithroot@gmail.com", ['001ae8c0-3a13-11e3-aea5-d4ae529a826e',], first_name="Justin", last_name="Lane")
    return HttpResponse(body)
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template,context,context_instance=RequestContext(request))