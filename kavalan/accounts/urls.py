from django.conf.urls.defaults import *

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout', {'next_page': '/'}),
    url(r'^password_change/$', 'password_change'),
    url(r'^password_change_done/$', 'password_change_done'),
)

urlpatterns += patterns('accounts.views',
    url(r'^manage/$', 'account_manage'),
    url(r'^create_user/$', 'create_user'),
)

urlpatterns += patterns('simpleavatar.views',
    url(r'^change_avatar/$', 'change', {'template_name': 'registration/change_avatar.html'}, name='account-change-avatar')
)