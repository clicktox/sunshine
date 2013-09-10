from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^channels/$', 'taxonomy.views.category_list',name='category_list'),
    url(r'^channels/(?P<parent>[\w\d-]+)/(?P<slug>[\w\d-]+)$', 'taxonomy.views.category_detail',name='subcategory_detail'),
    url(r'^channels/(?P<slug>[\w\d-]+)$', 'taxonomy.views.category_detail',name='category_detail'),
    
    url(r'^scoop/$', 'taxonomy.views.scoop_home',name='scoop_home'),
    url(r'^scoop/(?P<slug>[\w\d-]+)/$', 'taxonomy.views.scoop_detail',name='scoop_detail'),
    url(r'^scoop/(?P<slug>[\w\d-]+)/add/$', 'taxonomy.views.scoop_add_item',name='scoop_add_item'),
    
    url(r'^topics/$', 'taxonomy.views.topic_list',name='topic_list'),
    url(r'^topics/(?P<uuid>[\w\d-]+)/$', 'taxonomy.views.topic_detail',name='topic_detail'),
    url(r'^topics/(?P<uuid>[\w\d-]+)/edit/$', 'taxonomy.views.topic_edit',name='topic_edit'),
    url(r'^topics/(?P<uuid>[\w\d-]+)/edit/content/$', 'taxonomy.views.topic_edit_content',name='topic_edit_content'),
    url(r'^topics/(?P<uuid>[\w\d-]+)/edit/image/$', 'taxonomy.views.topic_edit_image',name='topic_edit_image'),
    url(r'^topics/add/$', 'taxonomy.views.topic_add',name='topic_add'),
    
    
    
)
