from django.conf.urls.defaults import *
from featured_content import views


urlpatterns = patterns('',
    url(r'^manage/$',views.manage,name='manage_featured_content'),
    url(r'^manage/update_ordering/$',views.update_featured_ordering,name='update_featured_ordering'),
    url(r'^manage/add/$',views.new_featured_item,name='new_featured_item'),
    url(r'^manage/(?P<feature_item_id>[\d]+)/remove/$',views.remove_featured_item,name='remove_featured_content'),
    url(r'^manage/(?P<feature_item_id>[\d]+)/simple/$',views.edit_featured_content_simple,name='edit_featured_content_simple'),
    
    
    url(r'^(?P<year>\d{4})/(?P<month>.{2})/(?P<day>\d{1,2})/$', views.featured_by_date,name="featured_by_day"),
    url(r'^(?P<year>\d{4})/(?P<month>.{2})/$', views.featured_by_date,name="featured_by_month"),
    url(r'^(?P<year>\d{4})/$', views.featured_by_date,name="featured_by_year"),
    url(r'^$', views.featured_by_date,name="featured_content_list"),
   
)
