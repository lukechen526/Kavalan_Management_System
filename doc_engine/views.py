# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.generic import TemplateView, ListView
from doc_engine.models import Document
from django.db.models import Q
from django.utils.translation import ugettext as _

class DocumentIndexView(TemplateView):

    template_name = "doc_engine/index.html"

class DocumentListView(ListView):

    context_object_name = "document_list"
    model = Document

def DocumentSearchView(request):
    """
    Receives a query 'q' via GET request, searches the database for rows matching the query in title or serial number,
    and returns the result as a JSON string.
    """
    if 'q' in request.GET and request.GET['q']:
        query = request.GET['q']
        results = Document.objects.filter(Q(serial_number__icontains=query)|Q(title__icontains=query))
        payload = list()
        if results:
            for result in results:
                payload.append({'SerialNumber': result.serial_number,
                                'Title': result.title,
                                'FileURL': result.file.url,
                                })
        return HttpResponse(json.dumps(payload), mimetype="application/json")
    else:
        return HttpResponse(_("Please Enter a Query"))
    
    