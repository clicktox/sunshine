import datetime
import re

from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, get_user_model
from django.shortcuts import render_to_response, get_object_or_404,resolve_url
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
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
from django.utils.http import base36_to_int, is_safe_url
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory

from members.forms import *

def home(request,template="homepage.html",extra_context=None):
    context={}
   
    if extra_context is not None:
        context.update(extra_context)
    
    if request.user.is_authenticated():
        if hasattr(request.user,'is_verified'): 
            return dashboard(request)
        user_form = BaseUserForm(instance=request.user)
        member_form = BaseMemberForm(instance=request.user.member)
        avatar_form = AvatarForm(instance=request.user.member.avatar)
        if request.method == 'POST':
            user_form = BaseUserForm(request.POST, instance=request.user)
            member_form = BaseMemberForm(request.POST, instance=request.user.member)
            avatar_form = AvatarForm(request.POST, request.FILES, instance=request.user.member.avatar)
            if user_form.has_changed():
                if user_form.is_valid():
                    user_form.save()
            if member_form.has_changed():
                if member_form.is_valid():
                    member_form.save()
            if avatar_form.is_valid():
                image = avatar_form.save(commit=False)
                image.uploaded_by = request.user
                image.save()
                request.user.member.avatar = image
                request.user.member.save()
            if 'insider' in request.POST:
                return HttpResponseRedirect(reverse('insider_signup'))
            return HttpResponseRedirect('http://connect.modernmom.com/')
            
        #context['member_form'] = member_form
        template = 'members/welcome.html'
        context['user_form'] = user_form
        context['member_form'] = member_form
        context['avatar_form'] = avatar_form
        
    return render_to_response(template,context,context_instance=RequestContext(request))

def dashboard(request,template='members/dashboard.html'):
    return render_to_response(template,context,context_instance=RequestContext(request))

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def logout(request, next_page=None,
           template_name='registration/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)

    if next_page is not None:
        next_page = resolve_url(next_page)

    if redirect_field_name in request.REQUEST:
        next_page = request.REQUEST[redirect_field_name]
        # Security check -- don't allow redirection to a different host.
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = request.path

    if next_page:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page)

    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Logged out')
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
        current_app=current_app)


def register(request):
    context = {}
    member_form = BaseRegistrationForm()
    if request.method == 'POST':
        member_form = BaseRegistrationForm(data=request.POST)
        if member_form.is_valid():
            user = member_form.save()
    context['form'] = member_form
    template = 'registration/register.html'
    return render_to_response(template,context,context_instance=RequestContext(request))

def password_reset(request):
    pass