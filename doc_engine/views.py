# Create your views here.
from django.views.generic import TemplateView
from doc_engine.models import Document, BatchRecordSearchForm, AccessRecord
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings

class DocumentIndexView(TemplateView):
    template_name = "doc_engine/index.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DocumentIndexView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['batch_record_search_form'] = BatchRecordSearchForm(auto_id=True)
        return context

    
def DocumentAccess(request, pk):
    MEDIA_ROOT = settings.MEDIA_ROOT
    user = request.user
    user_groups = user.groups.all()
    document = get_object_or_404(Document, pk=pk)
    document_groups = list(document.permitted_groups.all())

    #Check if the user has the necessary group permission to access the document
    for group in user_groups:
        if group in document_groups or user.is_superuser:
            #Allows access if the user is in the permitted group or is a superuser
            
            AccessRecord.objects.create(user=user, ip=request.META['REMOTE_ADDR'], document_accessed=document)
            return HttpResponse(document.file.name)

    return HttpResponseForbidden("Access Denied")

    
