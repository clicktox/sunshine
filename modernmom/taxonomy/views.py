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
import json
from django.core.urlresolvers import reverse
from django.core import serializers
from django.template.defaultfilters import slugify
from taxonomy.models import *
from articles.models import Reference,ArticleReference
from forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def scoop_detail(request,slug=None,template="scoop/detail.html",extra_context=None):
    scoop = get_object_or_404(Scoop,slug=slug)
    context={}
    if extra_context is not None:
        context.update(extra_context)
    templates = [u'scoop/custom/%s.html' % scoop.slug,template]
    paginator = Paginator(scoop.items.all(), 25) 

    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)
    
    context.update({'paginator': paginator,
                    'page_number': page,
                    'page_obj': items,
                    'scoop': scoop })
    
    return render_to_response(templates,context,context_instance=RequestContext(request))# Create your views here.

from articles.utils import ProcessReference
@staff_member_required
def scoop_add_item(request,slug=None,template='scoop/scoopitem/add/home.html',extra_context=None):
    context={}
    context['scoop'] = scoop = get_object_or_404(Scoop,slug=slug)
    if request.is_ajax():
        if 'reference_url' in request.POST:
            oReference = ProcessReference(request.POST['reference_url'])
            json_response = json.dumps(oReference)
            return HttpResponse(json_response,mimetype='application/json')
    
    if extra_context is not None:
        context.update(extra_context)
    
    form = ScoopItemForm()
    imageform = ScoopItemImageForm(prefix='image')
    
    if request.method == 'POST':
        hasErrors = False
        form = ScoopItemForm(request.POST)
        imageform = ScoopItemImageForm(request.POST,request.FILES,prefix='image')
        image = None
        if imageform.is_valid():
            image = imageform.save()
        else:
            if 'image' in imageform.errors:
                image = None
                pass #they were not trying to upload an image
            else:
                context['form'] = form
                context['imageform'] = imageform
                return render_to_response(template,context,context_instance=RequestContext(request))
                
        
        if form.is_valid():
            article = form.save(commit=False)
            article.creator = request.user
            article.image = image    
            article.save()
            scoop_item,c = ScoopItem.objects.get_or_create( scoop=scoop,
                                                            content_type = ContentType.objects.get_for_model(article),
                                                            object_id=article.pk)
            if 'reference_id' in request.POST:
                try:
                    reference = Reference.objects.get(id=request.POST['reference_id'])
                    article_reference,c = ArticleReference.objects.get_or_create(article=article,reference=reference)
                except:
                    pass
            return HttpResponseRedirect(article.get_absolute_url())
        
    context['form'] = form
    context['imageform'] = imageform
    return render_to_response(template,context,context_instance=RequestContext(request))

@staff_member_required
def scoop_add_post(request,slug=None,template='scoop/scoopitem/add/post.html',extra_context=None):
    context={}
    context['scoop'] = scoop = get_object_or_404(Scoop,slug=slug)
    if request.is_ajax():
        if 'reference_url' in request.POST:
            oReference = ProcessReference(request.POST['reference_url'])
            json_response = json.dumps(oReference)
            return HttpResponse(json_response,mimetype='application/json')
    
    if extra_context is not None:
        context.update(extra_context)
    
    form = ScoopItemForm()
    imageform = ScoopItemImageForm(prefix='image')
    
    if request.method == 'POST':
        hasErrors = False
        form = ScoopItemForm(request.POST)
        imageform = ScoopItemImageForm(request.POST,request.FILES,prefix='image')
        image = None
        if imageform.is_valid():
            image = imageform.save()
        else:
            if 'image' in imageform.errors:
                pass #they were not trying to upload an image
                image = None
            else:
                return render_to_response(template,context,context_instance=RequestContext(request))
                
        
        if form.is_valid():
            article = form.save(commit=False)
            article.creator = request.user
            article.image = image    
            article.save()
            scoop_item,c = ScoopItem.objects.get_or_create( scoop=scoop,
                                                            content_type = ContentType.objects.get_for_model(article),
                                                            object_id=article.pk)
            if 'reference_id' in request.POST:
                try:
                    reference = Reference.objects.get(id=request.POST['reference_id'])
                    article_reference,c = ArticleReference.objects.get_or_create(article=article,reference=reference)
                except:
                    pass
            return HttpResponseRedirect(article.get_absolute_url())
        
    context['form'] = form
    context['imageform'] = imageform
    return render_to_response(template,context,context_instance=RequestContext(request))

@staff_member_required
def scoop_add_slideshow(request,slug=None,template='scoop/scoopitem/add/slideshow/step1.html',extra_context=None):
    context={}
    context['scoop'] = scoop = get_object_or_404(Scoop,slug=slug)
    
    if extra_context is not None:
        context.update(extra_context)
    
    form = ScoopItemSlideshowForm()
    imageform = ScoopItemImageForm(prefix='image')
    
    if request.method == 'POST':
        hasErrors = False
        form = ScoopItemSlideshowForm(request.POST)
        imageform = ScoopItemImageForm(request.POST,request.FILES,prefix='image')
        image = None
        if imageform.is_valid():
            image = imageform.save()
        else:
            if 'image' in imageform.errors:
                pass #they were not trying to upload an image
                image = None
            else:
                return render_to_response(template,context,context_instance=RequestContext(request))
                
        
        if form.is_valid():
            article = form.save(commit=False)
            article.creator = request.user
            article.image = image    
            article.display_type = 'slideshow'
            article.save()
            scoop_item,c = ScoopItem.objects.get_or_create( scoop=scoop,
                                                            content_type = ContentType.objects.get_for_model(article),
                                                            object_id=article.pk)
            
            return HttpResponseRedirect(reverse('articles_edit_article_content',args=[article.uuid]))
        
    context['form'] = form
    context['imageform'] = imageform
    return render_to_response(template,context,context_instance=RequestContext(request))

@staff_member_required
def topic_add(request,template='taxonomy/topics/add.html',extra_context=None):
    context = {}
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.slug = slugify(topic.name)
            topic.save()
            return HttpResponseRedirect(reverse('edit_topic',args=[topic.uuid]))
    context['form'] = form
            
    return render_to_response(template,context,context_instance=RequestContext(request))

@staff_member_required
def topic_edit(request,uuid=None,template='taxonomy/topics/edit.html',extra_context=None):
    context = {}
    context['topic'] = topic = get_object_or_404(Topic,uuid=uuid)
    context['topic_image_form'] = TopicImageForm()
    
            
    return render_to_response(template,context,context_instance=RequestContext(request))


@staff_member_required
def topic_edit_content(request,uuid=None,template='taxonomy/topics/edit.html',extra_context=None):
    context = {}
    context['topic'] = topic = get_object_or_404(Topic,uuid=uuid)
    if request.is_ajax():
        if 'content' in request.POST:
            content,c = TopicContent.objects.get_or_create(topic=topic,defaults={'content':request.POST['content']})
            if ( not c ):
                content.content = request.POST['content']
            content.save()
            json_response = json.dumps({"message":'Saved'})
            return HttpResponse(json_response,mimetype='application/json')
    return HttpResponseRedirect(reverse('topic_edit',args=[topic.uuid]))

@staff_member_required
def topic_edit_image(request,uuid=None,template='taxonomy/topics/edit.html',extra_context=None):
    context = {}
    context['topic'] = topic = get_object_or_404(Topic,uuid=uuid)
    if request.method=="POST":
        form = TopicImageForm(request.POST, request.FILES)
        if form.is_valid():
            ti = form.save(commit=False)
            ti.topic = topic
            ti.save()
    return HttpResponseRedirect(reverse('topic_edit',args=[topic.uuid]))

def topic_detail(request,uuid=None,template='taxonomy/topics/detail.html',extra_context=None):
    context = {}
    context['topic'] = topic = get_object_or_404(Topic,uuid=uuid)
    
            
    return render_to_response(template,context,context_instance=RequestContext(request))

def topic_list(request,template='taxonomy/topics/list.html',extra_context=None):
    context = {}
    context['topics'] = Topic.objects.all()
    return render_to_response(template,context,context_instance=RequestContext(request))

        