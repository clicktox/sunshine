from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from views import *
from views_apps import *
import datetime


urlpatterns = patterns('',
    (r'^$', home),
    (r'^',include('cissonius.urls')),
    (r'^apps/facebook/tab/',facebook_tab),
    
)
