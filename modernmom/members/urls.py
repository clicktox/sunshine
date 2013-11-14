from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^login/$', 'members.connectviews.login', name='login'),
    url(r'^register/$', 'members.connectviews.register', name='register'),
    url(r'^logout/$', 'members.connectviews.logout', name='logout'),
    url(r'^password_reset/$', 'members.connectviews.password_reset', name='password_reset'),
    
    url(r'^members/$', 'members.views.member_list', name='member_list'),
    url(r'^members/share-it/$', 'members.views.share_it', name='share_it'),
    url(r'^members/(?P<uuid>[\d\w-]+)/$', 'members.views.member_detail', name='member_detail'),
    url(r'^members/(?P<uuid>[\d\w-]+)/edit/$', 'members.views.member_detail_edit', name='member_detail_edit'),
    #url(r'^users/(?P<slug>[\d\w-]+)/$', 'members.views.member_redirect', name='member_redirect_slug'),
    #url(r'^user/(?P<member_id>[\d]+)/$', 'members.views.member_redirect', name='member_redirect_id'),
    url(r'^insider/$', 'members.views.insider_dashboard', name='insider_dashboard'),
    url(r'^insider/signup/$', 'members.views.insider_signup', name='insider_signup'),
    url(r'^insider/campaign/(?P<uuid>[\w\d-]+)/$', 'members.views.insider_campaign_detail', name='insider_campaign_detail'),
    url(r'^insider/campaign/(?P<uuid>[\w\d-]+)/pr/(?P<product_id>[\d]+)/$', 'members.views.insider_campaign_product', name='insider_campaign_product'),
    url(r'^insider/campaign/(?P<uuid>[\w\d-]+)/share/$', 'members.views.insider_campaign_voteup', name='insider_campaign_voteup'),
    
    url(r'^members/twitter/auth/(?P<appid>[\d]+)/$', 'django_twitter.views.authorize_twitter_user', name='twitter_authorize_url'),
    
   
    #url(r'^survey/(?P<id>\d+)/$', 'survey.views.SurveyDetail', name='survey_detail'),
    #url(r'^survey/confirm/(?P<uuid>\w+)/$', 'survey.views.Confirm', name='survey_confirmation'),
    
)
