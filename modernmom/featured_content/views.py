# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import *
import datetime
from datetime import date, timedelta
from urlparse import urlparse
from django.utils.html import strip_tags




def featured_by_date(request,year=None,month=None,day=None, template="featured_content/list.html",extra_context=None):
    context={}
    if extra_context is not None:
        context.update(extra_context)
    featured_items = FeaturedItem.objects.all()
    if year:
        featured_items = featured_items.filter(feature_date__year=year)
    if month:
        featured_items = featured_items.filter(feature_date__month=month)
    if day:
        featured_items = featured_items.filter(feature_date__day=day)
    paginator = Paginator(featured_items, 25) 

    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)
    context['items'] = items
    return render_to_response(template,context,context_instance=RequestContext(request))

from forms import *
def manage(request,template='featured_content/manage.html'):
    context = {}
    form = FeaturedItemForm()
    image_form = FeaturedItemImageForm(prefix='image')
    if request.method == 'POST':
        image_form = FeaturedItemImageForm(request.POST,request.FILES,prefix='image')
        form = form = FeaturedItemForm(request.POST)
        if form.is_valid():
            if image_form.is_valid():
                fi = form.save(commit=False)
                fii = image_form.save()
                fi.image = fii
                fi.save()
                return HttpResponseRedirect('/')
            
    context['form'] = form
    context['image_form'] = image_form
    context['featured_items'] = FeaturedItem.objects.filter(feature_date__gte=date.today()-timedelta(days=7))
    return render_to_response(template,context,context_instance=RequestContext(request))

def remove_featured_item(request,feature_item_id):
    item = get_object_or_404(FeaturedItem,id=feature_item_id)
    item.delete()
    return HttpResponseRedirect(reverse('manage_featured_content'))

def edit_featured_content_simple(request,feature_item_id,template='featured_content/edit_simple.html'):
    context = {}
    context['item'] = item = get_object_or_404(FeaturedItem,id=feature_item_id)
    form = FeaturedItemForm(instance=item)
    image_form = FeaturedItemImageForm(prefix='image',instance=item.image)
    
    if request.method == 'POST':
        image_form = FeaturedItemImageForm(request.POST,request.FILES,prefix='image',instance=item.image)
        form = form = FeaturedItemForm(request.POST,instance=item)
        if form.is_valid():
            if image_form.is_valid():
                fi = form.save(commit=False)
                fii = image_form.save()
                fi.image = fii
                fi.save()
                if 'continue' in request.POST:
                    return HttpResponseRedirect(reverse('edit_featured_content_simple',args=[fi.id]))
                return HttpResponseRedirect(reverse('manage_featured_content'))
    context['image_form'] = image_form
    context['form'] = form
    return render_to_response(template,context,context_instance=RequestContext(request))

@login_required
def update_featured_ordering(request):
    if request.is_ajax():
        message = 'AJAX!'
        for p in request.POST:
            message = '%s %s' % (message,p)
        itemids = request.POST.getlist('featureditems[]')
        count = len(itemids)
        for id in itemids:
            fi = FeaturedItem.objects.get(id=id)
            fi.priority = count
            fi.save()
            message = '%s, %s' % ( message,fi.name )
            count = count-1

    return HttpResponse(message)

from articles.models import Article
def new_featured_item(request):
    if request.method == "POST":
        if 'source_url' in request.POST:
            #make sure this is a modernmom url...
            urlp = urlparse(request.POST['source_url'])
            if not urlp.netloc.endswith('modernmom.com'):
                return HttpResponse('%s is not a valid ModernMom url..' % request.POST['source_url'])
            if urlp.path.endswith('.html'):
                
                uuid = urlp.path.split('/').pop().split('.')[0]
                article = Article.objects.get(uuid=uuid)
                
                if article.image:
                    fci,c = FeaturedItemImage.objects.get_or_create(image=article.image.image)
                    fc = FeaturedItem(name=article.title,description=strip_tags(article.introduction),image=fci,url=request.POST['source_url'],feature_date = date.today())
                    fc.save()
                    return HttpResponseRedirect(reverse('edit_featured_content_simple',args=[fc.id]))

            else:
                return HttpResponse('%s does not end with html..' % request.post['source_url'])
        else:
            return HttpResponse('source_url does not exist.')
    
                
                    
                
                
            
            
                
        
