import datetime
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify, striptags
from django.contrib.comments.models import Comment
from django.views.decorators.http import require_POST

from members.models import *
from forms import *
from django.db import IntegrityError
from django.forms import URLField

def member_detail_edit(request,uuid):
    context={}
    form = MemberChangeForm(instance=request.user)
    if request.method == 'POST':
        form = MemberChangeForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.user.get_absolute_url() )
    context['form'] = form
    return render_to_response('members/edit.html',context,context_instance=RequestContext(request))

def member_detail(request,uuid):
    context={}
    context['member'] = content = get_object_or_404(Member,uuid=uuid)
    return render_to_response('members/detail.html',context,context_instance=RequestContext(request))

def member_list(request):
    context={}
    context['members'] = Member.objects.all()
    return render_to_response('members/list.html',context,context_instance=RequestContext(request))

def member_redirect(request,slug=None,member_id=None):
    context={}
    if not slug is None:
        member = get_object_or_404(Member,slug=slug)
        return HttpResponseRedirect(reverse('member_detail',args=[member.uuid]))
    if not member_id is None:
        member = get_object_or_404(Member,id=member_id)
        return HttpResponseRedirect(reverse('member_detail',args=[member.uuid]))
    return HttpResponseRedirect('/?hello')

@login_required
def insider_signup(request,template='insiders/signup.html'):
    context={}
    fUrl = URLField()
    context['social_profile_type_list'] = spt_list = SocialProfileType.objects.all()
    member,c = Member.objects.get_or_create(user=request.user)
    try:
        current_address = member.memberaddress
    except MemberAddress.DoesNotExist:
        current_address=None
    address_form = MemberAddressForm(prefix='address',instance=current_address)
    if request.method == 'POST':
        request.user.first_name = request.POST['first_name']
        request.user.last_name = request.POST['last_name']
        request.user.save()
        try:
            mbd = member.memberbirthdate
        except MemberBirthdate.DoesNotExist:
            mbd = MemberBirthdate(member=member)
        mbd.birthdate = request.POST['birthdate']
        mbd.save()
        
        address_form = MemberAddressForm(request.POST,prefix='address',instance=current_address)
        if address_form.is_valid():
            a = address_form.save(commit=False)
            a.member = member
            a.save()
        
        #member.save()
        for spt in spt_list:
            field_name = u'social_profile_type_%s' % spt.id
            if field_name in request.POST:
                try:
                    url = fUrl.clean(request.POST[field_name])
                    try:
                        sp = MemberSocialProfile.objects.get(member=member,profile_type=spt)
                    except MemberSocialProfile.DoesNotExist:
                        sp = MemberSocialProfile(member=member,profile_type=spt)
                    sp.url=url
                    sp.save()
                except:
                    pass #no data supplied
            
            #Websites
            for et in et_list:
                field_name = u'website_type_%s' % et.id
                if field_name in request.POST:
                    #break it out by line...
                    lines = request.POST[field_name].split('\r\n')
                    for line in lines:
                        try:
                            url = fUrl.clean(line)
                            ws,c = MemberWebsite.objects.get_or_create(member=member,website=url)
                            ws.website_type.add(et)
                        except:
                            pass
        insider = Insider.objects.get_or_create(user=request.user)
        return HttpResponseRedirect(reverse('insider_dashboard'))
                
    try:
        insider = request.user.insider
        return HttpResponseRedirect(reverse('insider_dashboard'))
    except Insider.DoesNotExist:
        context['address_form'] = address_form
        context['form'] = InsiderForm()
       
       
    return render_to_response(template,context,context_instance=RequestContext(request))

@login_required
def insider_dashboard(request,template='insiders/dashboard.html'):
    context={}
    try:
        insider = request.user.insider
        
    except Insider.DoesNotExist:
        return HttpResponseRedirect(reverse('insider_signup'))
    
    context['campaigns'] = InsiderCampaign.objects.all()
       
       
    return render_to_response(template,context,context_instance=RequestContext(request))


@login_required
def insider_campaign_detail(request,uuid,template='insiders/campaigns/detail.html'):
    context={}
    try:
        insider = request.user.insider
    except Insider.DoesNotExist:
        return HttpResponseRedirect(reverse('insider_signup'))
    context['campaign'] = campaign = get_object_or_404(InsiderCampaign,uuid=uuid)
    ic,c = InsiderCampaignApplicant.objects.get_or_create(campaign=campaign,insider=insider)
    context['application'] = ic
    from survey.forms import SurveyForm
    survey_form = SurveyForm(survey=campaign.insidercampaignsurvey_set.all()[0].survey,user=request.user)
    
    if request.method == 'POST':
        survey_form = SurveyForm(request.POST, survey=campaign.insidercampaignsurvey_set.all()[0].survey,user=request.user) 
        if survey_form.is_valid():
            survey_form.save()
            return HttpResponseRedirect( campaign.get_absolute_url() )
        
    context['survey_form'] = survey_form   
    return render_to_response(template,context,context_instance=RequestContext(request))


@login_required
def insider_campaign_product(request,uuid,product_id,template='insiders/campaigns/product.html'):
    context={}
    try:
        insider = request.user.insider
    except Insider.DoesNotExist:
        return HttpResponseRedirect(reverse('insider_signup'))
    context['campaign'] = campaign = get_object_or_404(InsiderCampaign,uuid=uuid)
    context['product'] = product = get_object_or_404(InsiderProduct,id=product_id)
    pc = get_object_or_404(InsiderProductCampaign,product=product,campaign=campaign) #just making sure..
    #is this user qualified...
    try:
        ic = InsiderCampaignApplicant.objects.get(campaign=campaign,insider=insider)
        if not ic.is_selected():
             return HttpResponse("You are not in this campaign...")
        context['applicant'] = ic
    except InsiderCampaignApplication.DoesNotExist:
        return HttpResponse("You are not in this campaign...")
    try:
        review = insider.insiderproductreview_set.filter(product=product)[0]
        context['review'] = review
    except Exception as e:
        review = None
    form = InsiderProductReviewForm(instance=review)
    if request.method == 'POST':
        form = InsiderProductReviewForm(request.POST,instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.insider = insider
            review.product = product
            review.save()
            return HttpResponseRedirect(pc.get_absolute_url())
        else:
            return HttpResponse(form.errors)
    context['form'] = form
    
    return render_to_response(template,context,context_instance=RequestContext(request))

import urllib
from voting.models import *
@login_required
def insider_campaign_voteup(request,uuid):
    campaign = get_object_or_404(InsiderCampaign,uuid=uuid)
    vote = Vote.objects.record_vote(campaign,request.user,+1)
    if 'fb' in request.GET:
        app_id = '208027353668'
        link='%s' % reverse('insider_dashboard')
        picture='http://connect.modernmom.com/media/images/mm_insider_300x250.jpg'
        title = ''
        description = "Do you want to try new products (for free) and review them for the community? Do have a blog or own a website? Are you considered an influencer among your peers? If you answered yes to any of these questions, then ModernMom Insiders is the program for you!"
        params = urllib.urlencode({'app_id':app_id,'link':link,'picture':picture,'name':'ModernMom Insiders','caption':'Join the ModernMom Insiders','description':description,'redirect_uri':link})
        goto = 'https://www.facebook.com/dialog/feed?%s' % params
        return HttpResponseRedirect(goto)
    return HttpResponseRedirect(campaign.get_absolute_url())

@login_required
def share_it(request):
    if 'shareon' in request.POST:
        share_form = MemberShareContentForm(request.POST)
        goto = 'http://connect.modernmom.com'
        if share_form.is_valid():
            #check to see if it exists...
            try:
                msc = MemberShareContent.objects.get(page=share_form.cleaned_data['page'])
            except MemberShareContent.DoesNotExist:
                msc = share_form.save()
            if share_form.cleaned_data['shareon'] == 'facebook':
                share_dict = {}
                share_dict['app_id'] = '208027353668'
                share_dict['link'] = msc.page
                share_dict['picture'] =msc.image
                share_dict['title'] = msc.title
                share_dict['description'] = msc.description
                share_dict['name'] = msc.title
                #share_dict['caption']: None
                share_dict['redirect_uri'] = msc.page
                params = urllib.urlencode(share_dict)
                member_share,c = MemberShare.objects.get_or_create(member=request.user.get_profile(),medium=share_form.cleaned_data['shareon'],content=msc)
                goto = 'https://www.facebook.com/dialog/feed?%s' % params
                return HttpResponseRedirect(goto)
        return HttpResponse(share_form.errors)
    return HttpResponseRedirect('/')

    