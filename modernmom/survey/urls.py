from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'survey.views.survey_list', name='survey_list'),
    url(r'^(?P<survey_id>[\d]+)/results/weighted/$', 'survey.views.survey_results_weighted', name='survey_results_weighted'),
     url(r'^(?P<survey_id>[\d]+)/results/(?P<user_id>[\d]+)/$', 'survey.views.survey_results_user', name='survey_results_user'),
    
    
)
