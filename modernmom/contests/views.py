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
import json
from django.core.urlresolvers import reverse
from django.core import serializers
from django.template.defaultfilters import slugify

from contests.models import *
from contests.forms import ContestantEntryImageForm

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home(request,template="contests/homepage.html",extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    context['contests'] = Contest.active.all() #objects.filter(status=1)
    return render_to_response(template,context,context_instance=RequestContext(request))

from django import forms
def detail(request,url,template="contests/detail.html",reached_daily_max=False,reached_total_max=False,extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    context['contest'] = contest = get_object_or_404(Contest,url=url)
    if contest.is_expired():
        return expired(request,url=url)
    myTemplate = u'contests/custom/%s.html' % contest.guid
    templates = [myTemplate,template]
    if not reached_daily_max and not reached_total_max:
        email_field = forms.EmailField()
        
        if request.method == 'POST':
            if 'email' in request.POST:
                try:
                    email = email_field.clean(request.POST['email'])
                    contestant,c = Contestant.objects.get_or_create(email=email)
         
                    entries_total = contestant.contestantentry_set.filter(contest=contest).count()
                    if entries_total >= contest.total_entry_count:
                        #return HttpResponseRedirect(u'%s?reached_total_max=True' % reverse('contest_detail',args=[contest.url]))
                        if request.is_ajax():
                            mimetype = 'application/json'
                            data = {'contestant':contestant.id,'message':'You have entered the contest enough times!'}
                            return HttpResponse(json.dumps(data),mimetype)
                        return HttpResponseRedirect(reverse('contest_detail_thankyou',args=[contest.url]))
                    if contest.entries_per_day > 0:
                        today = datetime.datetime.today()
                        entries_today = contestant.contestantentry_set.filter(entered_on__year=today.year,entered_on__day = today.day,entered_on__month=today.month).count()
                        if entries_today >= contest.entries_per_day:
                            #return HttpResponseRedirect(u'%s?reached_daily_max=True' % reverse('contest_detail',args=[contest.url]))
                            if request.is_ajax():
                                mimetype = 'application/json'
                                data = {'contestant':contestant.id,'message':'You have entered the contenst enough today, come back tomorrow!'}
                                return HttpResponse(json.dumps(data),mimetype)
    
                            return HttpResponseRedirect(reverse('contest_detail_thankyou',args=[contest.url]))
                    entry = ContestantEntry(contest=contest,contestant=contestant,ip_address=get_client_ip(request))
                    entry.save()
                    
                    if 'image' in request.FILES:
                        image_form = ContestantEntryImageForm(request.POST,request.FILES)
                        if image_form.is_valid():
                            cie = image_form.save(commit=False)
                            cie.contestantentry = entry
                            cie.save()
                    for key, value in request.POST.iteritems():
                        if key.startswith(contest.guid):
                            key = key.replace(contest.guid,'')
                            k = ContestantEntryKey(entry_key=key,entry_value=value,contestantentry=entry)
                            k.save()
                    
                    if request.is_ajax():
                        mimetype = 'application/json'
                        data = {'contestant':contestant.id,'message':"You're entry was succefull!"}
                        return HttpResponse(json.dumps(data),mimetype)
                    return HttpResponseRedirect(reverse('contest_detail_thankyou',args=[contest.url]))
                except forms.ValidationError:
                    context['errors'] = 'Please provide a valid email address.'
            if request.is_ajax():
                mimetype = 'application/json'
                data = {'error':True,'message':"Please complete all the required fields on the form."}
                return HttpResponse(json.dumps(data),mimetype)
                    
            

    return render_to_response(templates,context,context_instance=RequestContext(request))

def thankyou(request,url,template="contests/thankyou.html",reached_daily_max=False,reached_total_max=False,extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    
    context['contest'] = contest = get_object_or_404(Contest,url=url)
    context['contests'] = Contest.objects.filter(status=1).exclude(id=contest.id)
    myTemplate = u'custom/%s_thankyou.html' % contest.guid
    templates = [myTemplate,template]
    return render_to_response(templates,context,context_instance=RequestContext(request))

def rules(request,url,template="contests/rules.html",reached_daily_max=False,reached_total_max=False,extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    
    context['contest'] = contest = get_object_or_404(Contest,url=url)
    myTemplate = u'contests/custom/%s-rules.html' % contest.guid
    templates = [myTemplate,template]
    return render_to_response(templates,context,context_instance=RequestContext(request))

def expired(request,url,template="contests/expired.html",reached_daily_max=False,reached_total_max=False,extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    
    context['contest'] = contest = get_object_or_404(Contest,url=url)
    context['contests'] = Contest.objects.filter(status=1).exclude(id=contest.id)
    myTemplate = u'custom/%s_expired.html' % contest.guid
    templates = [myTemplate,template]
    return render_to_response(templates,context,context_instance=RequestContext(request))

import urllib
def share_contest(request,url):
    contest = get_object_or_404(Contest,url=url)
    if 'share_on' in request.GET:
        if int(request.GET['share_on']) == 0:
            if 'contestant' in request.POST:
                contestant = Contestant.objects.get(id = int(request.POST['contestant']))
                cs = ContestantShare(contestant=contestant,contest=contest,shared_on=0)
                cs.save()
            app_id = '208027353668'
            link='%s' % contest.get_absolute_url()
            try:
                picture='http://contests.modernmom.com%s' % contest.contestimage.get_largegrid_url()
            except:
                picture = None
            title = contest.name
            try:
                description = contest.contestdescription
            except:
                description = ''
            params = urllib.urlencode({'app_id':app_id,'link':link,'picture':picture,'name':title,'caption':'','description':description,'redirect_uri':link})
            goto = 'https://www.facebook.com/dialog/feed?%s' % params
            return HttpResponseRedirect(goto)
    return HttpResponseRedirect(contest.get_absolute_url())

def enter_contest(request,guid,template=''):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    context['contest'] = contest = get_object_or_404(Contest,guid=guid)
    if request.method=='POST':
        pass

from django.contrib.admin.views.decorators import staff_member_required
from forms import *

@staff_member_required
def contest_report(request,url,template="contests/report.html",reached_daily_max=False,reached_total_max=False,extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    context['contest'] = contest = get_object_or_404(Contest,url=url)
    if request.method == 'POST':
        form = ContestantEntryWinnerForm(request.POST)
        if form.is_valid():
            w = form.save(commit=False)
            w.chosen_by = request.user
            w.save()
            return HttpResponseRedirect(contest.get_report_url())
    context['winner_form'] = ContestantEntryWinnerForm()
    context['winners'] = ContestantEntryWinner.objects.filter(contestantentry__contest=contest)
    context['random'] = ContestantEntry.objects.filter(contest=contest).order_by('?')[0] if ContestantEntry.objects.filter(contest=contest).count() > 0 else None
    myTemplate = u'custom/%s_report.html' % contest.guid
    templates = [myTemplate,template]
    return render_to_response(templates,context,context_instance=RequestContext(request))

@staff_member_required
def upload_contest_assets(request,url,extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    context['contest'] = contest = get_object_or_404(Contest,url=url)
    if request.method == 'POST':
        form = ContestantEntryWinnerForm(request.POST)
        if form.is_valid():
            w = form.save(commit=False)
            w.chosen_by = request.user
            w.save()
            return HttpResponseRedirect(contest.get_report_url())
    context['winner_form'] = ContestantEntryWinnerForm()
    context['winners'] = ContestantEntryWinner.objects.filter(contestantentry__contest=contest)
    context['random'] = ContestantEntry.objects.filter(contest=contest).order_by('?')[0] if ContestantEntry.objects.filter(contest=contest).count() > 0 else None
    myTemplate = u'custom/%s_report.html' % contest.guid
    templates = [myTemplate,template]
    return render_to_response(templates,context,context_instance=RequestContext(request))

import csv
from django.utils.encoding import smart_text
@staff_member_required
def export_contest(request,url):
    # Create the HttpResponse object with the appropriate CSV header.
    contest = get_object_or_404(Contest,url=url)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % contest.url
    writer = csv.writer(response)
    entries = ContestantEntry.objects.filter(contest=contest)
    for e in entries:
        writer.writerow([e.contestant, e.entered_on, e.ip_address,e.contestantentrykey_set.all()[0].entry_value.encode('utf-8', errors='ignore')])
    return response


