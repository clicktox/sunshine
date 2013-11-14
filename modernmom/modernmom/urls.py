from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

    

urlpatterns = patterns('',
                       
    url(r'^$', 'modernmom.views.home', name='home'),
    url(r'^newsletter/', include('newsletter.urls')),
    
    #Specific Flatpages...
    url(r'^brooke-burke$', 'django.contrib.flatpages.views.flatpage', {'url': '/brooke-burke/'}, name='flatpage-brooke-burke'),
    url(r'^brooke-burke/the-naked-mom-book/$', 'django.contrib.flatpages.views.flatpage', {'url': '/brooke-burke/'}, name='flatpage-the-naked-mom-book'),
    url(r'^about-us/$', 'django.contrib.flatpages.views.flatpage', {'url': '/about-us/'}, name='flatpage-about'),
    url(r'^press/$', 'django.contrib.flatpages.views.flatpage', {'url': '/press/'}, name='flatpage-press'),
    url(r'^privacy-policy/$', 'django.contrib.flatpages.views.flatpage', {'url': '/privacy-policy/'}, name='flatpage-privacy-policy'),
    url(r'^terms-of-use/$', 'django.contrib.flatpages.views.flatpage', {'url': '/terms-of-use/'}, name='flatpage-terms-of-use'),
    url(r'^advertising/$', 'django.contrib.flatpages.views.flatpage', {'url': '/advertising/'}, name='flatpage-advertising'),
    #basic flat pages..
    (r'^pages/', include('django.contrib.flatpages.urls')),
    
    url(r'^', include('articles.urls')),
    url(r'^members/twitter/auth/(?P<appid>[\d]+)/$', 'django_twitter.views.authorize_twitter_user', name='authorize_twitter_user'),
    url(r'^twitter/callback/(?P<appid>[\d]+)/$', 'django_twitter.views.authorize_twitter_user_callback', name='twitter_authorize_url_callback'),
    url(r'^', include('members.urls')),
    url(r'^contributors/$', 'articles.views.author_list', name='contributors'),
    url(r'^contributors/all/$', 'articles.views.author_list',{'all':True}, name='contributors_all'),
    url(r'^contributors/(?P<uuid>[\w\d-]+)/$', 'articles.views.author_detail', name='author_detail'),
    #url(r'^channels/$', 'taxonomy.views.category_list', name='channels'),
    #url(r'^channels/(?P<parent>[\w\d-]+)/(?P<slug>[\w\d-]+)$', 'taxonomy.views.category_detail',name='subcategory_detail'),
    #url(r'^channels/(?P<slug>[\w\d-]+)$', 'taxonomy.views.category_detail',name='category_detail'),
    
    #url(r'^contributors/$', 'modernmom.views.contributors', name='contributors'),
    url(r'^featured-content/', include('featured_content.urls')),
    
    url(r'^contests/', include('contests.urls')),
    #url(r'^partners/', include('partners.urls')),
    
    url(r'^', include('cissonius.urls')),
    url(r'^', include('taxonomy.urls')),
    url(r'^toolbox/', include('toolbox.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

"""
urlpatterns += patterns('django.contrib.flatpages.views',
    
)
"""