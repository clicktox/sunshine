from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^channels/$', 'taxonomy.views.category_list',name='category_list'),
    url(r'^channels/(?P<parent>[\w\d-]+)/(?P<slug>[\w\d-]+)$', 'taxonomy.views.category_detail',name='subcategory_detail'),
    url(r'^channels/(?P<slug>[\w\d-]+)$', 'taxonomy.views.category_detail',name='category_detail'),
    
    url(r'^scoop/$', 'taxonomy.views.scoop_home',name='scoop_home'),
    url(r'^scoop/(?P<slug>[\w\d-]+)/$', 'taxonomy.views.scoop_home',name='scoop_detail'),
    url(r'^scoop/(?P<slug>[\w\d-]+)/add/$', 'taxonomy.views.scoop_add_item',name='scoop_add_item'),
    
    
    
)
