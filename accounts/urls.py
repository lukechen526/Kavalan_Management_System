from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change'),
    url(r'^password_change_done/$', 'django.contrib.auth.views.password_change_done'),

)
  