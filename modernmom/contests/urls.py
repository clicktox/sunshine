from django.conf.urls import patterns, include, url
#from members.models import InsiderProductReview


urlpatterns = patterns('',
    url(r'^$', 'contests.views.home', name='contests_home'),
    #url(r'^simplehuman/$', 'contests.views.detail', {'url':'simplehuman','extra_context':{'reviews':InsiderProductReview.objects.all()}},name='contest_simplehuman'),
    url(r'^(?P<url>[\d\w-]+)/$', 'contests.views.detail', name='contest_detail'),
    url(r'^(?P<url>[\d\w-]+)/share/$', 'contests.views.share_contest', name='share_contest'),
    url(r'^(?P<url>[\d\w-]+)/$', 'contests.views.detail',{'reached_total_max':True}, name='contest_reached_total_max'),
    url(r'^(?P<url>[\d\w-]+)/$', 'contests.views.detail',{'reached_daily_max':True}, name='contest_reached_daily_max'),
    url(r'^(?P<url>[\d\w-]+)/$', 'contests.views.detail',{'entry_success':True}, name='contest_entry_success'),
    url(r'^(?P<url>[\d\w-]+)/thankyou/$', 'contests.views.thankyou', name='contest_detail_thankyou'),
    url(r'^(?P<url>[\d\w-]+)/rules/$', 'contests.views.rules', name='contest_detail_rules'),
    url(r'^(?P<url>[\d\w-]+)/manage/$', 'contests.views.contest_report', name='contest_report'),
    url(r'^(?P<url>[\d\w-]+)/manage/export/$', 'contests.views.export_contest', name='contest_export'),
  
    #url(r'^ajax/list/$', 'contests.ajax_views.list', name='contests_ajax_list'),
   

)
