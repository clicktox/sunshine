from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import json

from models import *
from forms import *
from utils import *
import datetime
from django.views.decorators.csrf import csrf_exempt
 
def product_list(request,template='cissonius/products/list.html'):
    context={}
    context['products'] = Product.objects.all()
    return render_to_response(template, context,context_instance=RequestContext(request))

def product_detail(request,uuid,template='cissonius/products/detail.html'):
    context={}
    context['product'] = product = get_object_or_404(Product,uuid=uuid)
    context['giftguides'] = GiftGuide.objects.filter(giftguideproduct__product=product)
    #has the user already committed a review?
    review = None
    if request.user.is_authenticated():
        try:
            review = ProductReview.objects.get(user=request.user,product=product)
        except:
            review = None
    context['product_review_form'] = ProductReviewForm(instance=review)
    if request.method == 'POST':
        review_form = ProductReviewForm(request.POST,instance=review)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            if 'add_to_musthaves' in request.POST:
                musthave,c = ProductMustHave.objects.get_or_create(product=product,user=request.user)
            return HttpResponseRedirect(reverse('product_detail',args=[product.uuid]))
    
    return render_to_response(template, context,context_instance=RequestContext(request))

def producer_detail(request,uuid,template='cissonius/producer/detail.html'):
    context={}
    context['producer'] = producer = get_object_or_404(Producer,uuid=uuid)
    context['products'] = Product.objects.filter(producer=producer)
    return render_to_response(template, context,context_instance=RequestContext(request))

@staff_member_required
def product_detail_edit(request,uuid,template='cissonius/products/edit.html'):
    context={}
    
    context['product'] = product = get_object_or_404(Product,uuid=uuid)
    context['product_form'] = ProductForm(instance=product,prefix='product')
    context['product_image_form'] = ProductImageForm(instance=product.image,prefix='productimage')
    context['producer_form'] = ProducerForm(instance=product,prefix='producer')
    context['product_link_form'] = ProductLinkForm(prefix='productlink')
    debug = {}
    if request.method == 'POST':
        product_form = ProductForm(request.POST,instance=product,prefix='product')
        if product_form.is_valid() and product_form.has_changed():
            old_desc = product.description
            product = product_form.save()
            new_desc = product.description
            return HttpResponseRedirect(reverse('product_detail_edit',args=[product.uuid]))
    context['product_from_url'] = ProductFromUrlForm()
   
    return render_to_response(template, context,context_instance=RequestContext(request))

@staff_member_required
def product_detail_edit_image(request,uuid,template=''):
    context={}
    
    context['product'] = product = get_object_or_404(Product,uuid=uuid)
    context['product_image_form'] = ProductImageForm(instance=product.image,prefix='productimage')
    debug = {}
    if request.method == 'POST':
        image_form = ProductImageForm(request.POST, instance=product.image,prefix='productimage')
        if image_form.is_valid():
            #image_form.clean()
            image = image_form.save(commit=False)
            if 'source' in image_form.changed_data:
                image_url = image_form.cleaned_data['source']
                relpath = fetch_product_image(image_url,'',img=None,relpath_only=True)
                image.image = relpath
            image.save()
            product.image = image
            product.save()
        else:
            return HttpResponse(image_form.errors)
    return HttpResponseRedirect(reverse('product_detail_edit',args=[product.uuid]))

@staff_member_required
def product_add(request,template='cissonius/products/add.html'):
    context={}
    context['product_form'] = ProductForm()
    context['producer_form'] = ProducerForm()
    context['product_from_url'] = ProductFromUrlForm()
    
    return render_to_response(template, context,context_instance=RequestContext(request))

@staff_member_required
def product_add_fromurl(request):
    context={}
    if request.method == 'POST':
        form = ProductFromUrlForm(request.POST)
        if form.is_valid():
            product,created = link_to_product(form.cleaned_data['url'])
            if type(product).__name__=='dict':
                return HttpResponse(json.load(product))
                
            return HttpResponseRedirect(product.get_absolute_url())
    return HttpResponseRedirect(reverse('product_add'))

@csrf_exempt 
def giftguide_detail(request,slug,template='cissonius/giftguides/detail.html'):
    context={}
    context['filters'] = GiftGuideFilter.objects.all()
    context['giftguide'] = giftguide = get_object_or_404(GiftGuide,slug=slug)
    context['giftguideproducts'] = GiftGuideProduct.objects.filter(giftguide=giftguide).order_by('-promotedgiftguideproduct')
    if 'for' in request.GET:
        try:
            filter = GiftGuideFilter.objects.get(slug=request.GET['for'])
            context['giftguideproducts'] = GiftGuideProduct.objects.filter(giftguide=giftguide,giftguideproductfilter__giftguidefilter=filter).order_by('-promotedgiftguideproduct')
        except GiftGuideFilter.DoesNotExist:
            pass #context['giftguideproducts'] = GiftGuideProduct.objects.filter(giftguide=giftguide,giftguideproductfilter__giftguidefilter=filer).order_by('-promotedgiftguideproduct')
    
    
    templates = ['cissonius/giftguides/custom/%s.html' % slug,template]
    return render_to_response(templates, context,context_instance=RequestContext(request))
@csrf_exempt 
def giftguide_product_detail(request,slug,id,template='cissonius/giftguides/product_detail.html'):
    context={}
    context['giftguide'] = giftguide = get_object_or_404(GiftGuide,slug=slug)
    context['product'] = get_object_or_404(GiftGuideProduct,giftguide=giftguide,id=id)
    templates = [template,]
    return render_to_response(templates, context,context_instance=RequestContext(request))

@staff_member_required
def giftguide_product_add(request,slug,template='cissonius/giftguides/products_add.html'):
    context={}
    product_form = ProductForm(prefix='product')
    product_image_form = ProductImageForm(prefix='image')
    
    context['giftguide'] = giftguide = get_object_or_404(GiftGuide,slug=slug)
    if request.method == 'POST':
        
        if 'product_id' in request.POST:
            for id in request.POST.getlist('product_id'):
                product = Product.objects.get(uuid=id)
                g,c = GiftGuideProduct.objects.get_or_create(giftguide=giftguide,product=product,defaults={'added_by':request.user})
            return HttpResponseRedirect(giftguide.get_absolute_url())
        
        
        product_image_form = ProductImageForm(request.POST,request.FILES,prefix='image')
        if product_image_form.is_valid():
            image = product_image_form.save()
        else:
            image = None
        
        product_form = ProductForm(request.POST,prefix='product')
        if product_form.is_valid():
            product = product_form.save()
            product.image = image
            product.save()
            g,c = GiftGuideProduct.objects.get_or_create(giftguide=giftguide,product=product,defaults={'added_by':request.user})
            return HttpResponseRedirect(giftguide.get_absolute_url())
            
    
    context['products'] = Product.objects.exclude(giftguideproduct__giftguide=giftguide)
    context['product_form'] = product_form
    context['product_image_form'] = product_image_form
    return render_to_response(template, context,context_instance=RequestContext(request))

@staff_member_required
def giftguide_product_list(request,slug,template='cissonius/giftguides/products_list.html'):
    context={}
    
    context['giftguide'] = giftguide = get_object_or_404(GiftGuide,slug=slug)
    if request.method == 'POST':
        if 'product_id' in request.POST:
            for id in request.POST.getlist('product_id'):
                product = Product.objects.get(uuid=id)
                ggp = GiftGuideProduct.objects.get(giftguide=giftguide,product=product)
                #ggp.delete()
            return HttpResponseRedirect(giftguide.get_absolute_url())
    context['products'] = Product.objects.filter(giftguideproduct__giftguide=giftguide)
    return render_to_response(template, context,context_instance=RequestContext(request))

@csrf_exempt 
def giftguide_list(request,template='cissonius/giftguides/list.html'):
    context={}
    context['giftguides'] = GiftGuide.objects.all()
    return render_to_response(template, context,context_instance=RequestContext(request))



def musthaves_user_detail(request,username,template='cissonius/musthaves/list.html'):
    context={}
    user = get_object_or_404(User,username=username)
    context['products'] = Product.objects.filter(productmusthave__user=user)
    context['groupmusthaves'] = request.user.groupmusthaves.all()
    return render_to_response(template, context,context_instance=RequestContext(request))

def groupmusthave_detail(request,username,slug,template="cissonius/musthaves/groupmusthave_detail.html"):
    context={}
    user = get_object_or_404(User,username=username)
    context['groupmusthave'] = get_object_or_404(GroupMustHave,user=user,slug=slug)
    return render_to_response(template, context,context_instance=RequestContext(request))


@login_required
def groupmusthave_product_add(request,username,slug,template='cissonius/musthaves/products_add.html'):
    context={}
    
    user = get_object_or_404(User,username=username)
    groupmusthave = get_object_or_404(GroupMustHave,user=user,slug=slug)
    if request.method == 'POST':
        if 'product_id' in request.POST:
            for id in request.POST.getlist('product_id'):
                product = ProductMustHave.objects.get(id=id)
                g,c = GroupMustHaveProduct.objects.get_or_create(groupmusthave=groupmusthave,productmusthave=product)
            return HttpResponseRedirect(groupmusthave.get_absolute_url())
    context['products'] = ProductMustHave.objects.exclude(groupmusthaveproduct__groupmusthave=groupmusthave)
    return render_to_response(template, context,context_instance=RequestContext(request))
