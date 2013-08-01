from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^article-categories/$', 'taxonomy.views.category_list',name='category_list'),
    url(r'^article-categories/(?P<parent>[\w\d-]+)/(?P<slug>[\w\d-]+)$', 'taxonomy.views.category_detail',name='subcategory_detail'),
    url(r'^article-categories/(?P<slug>[\w\d-]+)$', 'taxonomy.views.category_detail',name='category_detail'),
    
)
