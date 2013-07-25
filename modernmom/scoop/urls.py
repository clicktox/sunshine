from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'scoop.views.home', name='scoop_home'),
)
