# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import BaseDetailView
from doc_engine.models import Document
from django.db.models import Q
from django.utils.translation import ugettext as _

class DocumentIndexView(TemplateView):

    template_name = "doc_engine/index.html"

class DocumentListView(ListView):

    context_object_name = "document_list"
    model = Document

def DocumentSearchView(request):
    if 'q' in request.GET and request.GET['q']:
        query = request.GET['q']
        results = Document.objects.filter(Q(serial_number__contains=query)|Q(title__contains=query))
        payload = list()
        if results:
            for result in results:
                payload.append({'Serial Number': result.serial_number,
                                'Title': result.title,
                                'File': result.file.url,
                                })
        return HttpResponse(json.dumps(payload), mimetype="application/json")
    else:
        return HttpResponse(_("Please Enter a Query"))
    
    