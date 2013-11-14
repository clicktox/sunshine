from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'connect.views.home', name='home'),
    url(r'^login/$', 'connect.views.login', name='login'),
    url(r'^register/$', 'connect.views.register', name='register'),
    url(r'^logout/$', 'connect.views.logout', name='logout'),
    url(r'^password_reset/$', 'connect.views.password_reset', name='password_reset'),
    (r'^',include('members.urls'))
   
  
)
