import datetime
import re
from django.db.models import Q
from django.conf import settings
from django.template.defaultfilters import slugify, striptags
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from photologue.models import get_storage_path

import lxml, urllib2
from django import forms
from django.db import models
import urllib, urlparse, os, re, copy
from urllib import urlretrieve

import hashlib,time, urllib2
import imghdr

from cissonius.models import *
from embedly import Embedly

def link_to_product(url,producer=None,commit=True):
    f_url = forms.URLField()
    try:
        url = f_url.clean(url)
        url=urlparse.urlparse(url)
        oUrl=url
    except Exception as e:
        return {'error':True,'message':'Not a valid link'}, False

    #TODO:  Stop the process on URLs who have asked is NOT to crawl them, esp GOOGLE, YAHOO, etc...


    eClient = Embedly('082feb14a1614dfba4bf5a36665b6046')
    o = eClient.objectify(url.geturl())
   
    if o.error:
        return {'error':True,'message':'Embedly Error: %d' % o.error_code,"URL":url.geturl()}, False
    if o.canonical:
        url = urlparse.urlparse(o.canonical)
    url = urlparse.urlparse(o.url)
    try:
        host = f_url.clean(url.netloc)
    except:
        return {'error':True,'message':'Improper url Format: %s' % url.geturl()}, False

    #Check to see if we already have this blog..
    try:
        productlink = ProductLink.objects.get(url=url.geturl())
        return productlink.product,True
    except ProductLink.DoesNotExist as e:
        pass
    
    if o.title == '':
        return {'error':True,'message':'No Page Title: %s' % source}, False
    product = Product()
    product.name=o.title
    product.description = o.description
    
    if producer:
        product.producer = producer
    else:
        producer,created = link_to_producer(url.netloc)
        if type(producer).__name__=='dict':
            return producer,False
        product.producer = producer
    
    
    #photo = fetch_image(o.thumbnail_url,title=item.title,uploaded_by=user,img=None)
    if len(o.images) > 0:
        image_url = o.images[0].url
        photo = fetch_product_image(image_url,title=product.name,img=None)
        product.image = photo
    product.save()
    
    p = ProductLink(product=product,url=url.geturl(),label=product.name)
    p.save()
          
    
    
    try:
        if commit:
            product.save()
        return product,commit
    except Exception as e:
        return {'error':True,'message':'Could not save blog post: %s' % e}, False   
   


def fetch_product_image(image_url,title,img=None,relpath_only=False):
    try:
        fi = hashlib.md5(str(time.time())).hexdigest()
        if img is None:
            img = urllib2.urlopen(image_url).read()
        t = imghdr.what('ignore',img)
        if t is None:
            return None,None,img
        fi = '%s.%s' % (fi,t)
        relpath = get_storage_path(None,fi) #os.path.join('photologue/photos/','%s' % fi)
        outpath = os.path.join(getattr(settings, 'MEDIA_ROOT', None),relpath)
        if not os.path.exists(outpath):
            urlretrieve(image_url,outpath)
        if (not relpath_only ):
            photo,create = ProductImage.objects.get_or_create(source=image_url,defaults={'image':relpath,'title':title})
        else:
            return relpath
    except Exception as e:
        a =  "Photo Captured Exception: %s" % e 
        return a
    return photo


def link_to_producer(url,commit=True):
    f_url = forms.URLField()
    try:
        url = f_url.clean(url)
        url=urlparse.urlparse(url)
        oUrl=url
    except Exception as e:
        return {'error':True,'message':'Not a valid link'},False
    
     #Check to see if we already have this blog..
    try:
        producerlink = ProducerLink.objects.get(url=url.geturl())
        return producerlink.producer,True
    except ProducerLink.DoesNotExist as e:
        pass
    
    #TODO:  Stop the process on URLs who have asked is NOT to crawl them, esp GOOGLE, YAHOO, etc...
    eClient = Embedly('082feb14a1614dfba4bf5a36665b6046')
    o = eClient.objectify(url.geturl())
    if o.error:
        return {'error':True,'message':'Embedly Error: %d' % o.error_code,"URL":url.geturl()}, False
    if o.canonical:
        url = urlparse.urlparse(o.canonical)
    url = urlparse.urlparse(o.url)
    try:
        host = f_url.clean(url.netloc)
    except:
        return {'error':True,'message':'Improper url Format: %s' % url.geturl()},False

   
    
    if o.title == '':
        return {'error':True,'message':'No Page Title: %s' % source}, False
    producer = Producer()
    producer.name=o.title
    try:
        photo = fetch_producer_image(o.images[0].url,title=producer.name,img=None)
        producer.image = photo
    except:
        print 'Item Image Fail'
    try:
        if commit:
            producer.save()
            p = ProducerLink(producer=producer,url=url.geturl(),label=producer.name)
            p.save()
   
        return producer,commit
    except Exception as e:
        return {'error':True,'message':'Could not save Producer: %s' % e},False

def fetch_producer_image(image_url,title,img=None):
    try:
        fi = hashlib.md5(str(time.time())).hexdigest()
        if img is None:
            img = urllib2.urlopen(image_url).read()
        t = imghdr.what('ignore',img)
        if t is None:
            return None,None,img
        fi = '%s.%s' % (fi,t)
        relpath = get_storage_path(None,fi) #os.path.join('photologue/photos/','%s' % fi)
        outpath = os.path.join(getattr(settings, 'MEDIA_ROOT', None),relpath)
        if not os.path.exists(outpath):
            urlretrieve(image_url,outpath)
        photo,create = ProducerImage.objects.get_or_create(source=image_url,defaults={'image':relpath,'title':title})
    except Exception as e:
        print("Photo Captured Exception: %s" % e)
        return None
    return photo
