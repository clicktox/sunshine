from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^products/$', 'cissonius.views.product_list', name='product_list'),
    url(r'^products/add/$', 'cissonius.views.product_add', name='product_add'),
    url(r'^products/add-from-url/$', 'cissonius.views.product_add_fromurl', name='product_add_fromurl'),
    url(r'^products/(?P<uuid>[\d\w-]+)/$', 'cissonius.views.product_detail', name='product_detail'),
    url(r'^products/(?P<uuid>[\d\w-]+)/edit/$', 'cissonius.views.product_detail_edit', name='product_detail_edit'),
    url(r'^products/(?P<uuid>[\d\w-]+)/edit/image/$', 'cissonius.views.product_detail_edit_image', name='product_detail_edit_image'),
    
    url(r'^producer/(?P<uuid>[\d\w-]+)/$', 'cissonius.views.producer_detail', name='producer_detail'),
    url(r'^giftguides/(?P<slug>[\d\w-]+)/$', 'cissonius.views.giftguide_detail', name='giftguide_detail'),
    url(r'^giftguides/(?P<slug>[\d\w-]+)/add/$', 'cissonius.views.giftguide_product_add', name='giftguide_product_add'),
    url(r'^giftguides/(?P<slug>[\d\w-]+)/list/$', 'cissonius.views.giftguide_product_list', name='giftguide_product_list'),
    url(r'^giftguides/$', 'cissonius.views.giftguide_list', name='giftguide_list'),
    
    url(r'^(?P<username>\w+)-must-haves/$', 'cissonius.views.musthaves_user_detail', name='musthaves_user_detail'),
    url(r'^(?P<username>\w+)-must-haves/(?P<slug>[\w\d-]+)/$', 'cissonius.views.groupmusthave_detail', name='groupmusthave_detail'),
    url(r'^(?P<username>\w+)-must-haves/(?P<slug>[\w\d-]+)/add/$', 'cissonius.views.groupmusthave_product_add', name='groupmusthave_product_add'),
    
    
    #url(r'^giftguides/', 'products.views.home', name='home'),
    #url(r'^producers/', 'products.views.home', name='home'),
    #url(r'^retailers/', 'products.views.home', name='home'),

)
