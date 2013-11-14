from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^subscribe/$', 'newsletter.views.subscribe', name='subscribe'),
)

