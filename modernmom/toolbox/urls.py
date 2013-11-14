from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'toolbox.views.home', name='toolbox_home'),
    url(r'^$', 'toolbox.views.downloads', name='toolbox_downloads'),
)
