from django.conf.urls.defaults import *
from doc_engine.views import DocumentIndexView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(DocumentIndexView.as_view())),
    )



