from piston.handler import BaseHandler
from piston.utils import *
from doc_engine.models import Document
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.conf import settings

class DefaultAuthenticationHandler(object):
    def is_authenticated(self, request):
        return request.user.is_authenticated()

    def challenge(self):
        return HttpResponseRedirect(settings.LOGIN_URL)
        
class DocumentHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Document
    fields = ('title', 'serial_number', 'file_url')

    @classmethod
    def read(self, request):
        """
        Searches 'Document' for entries with title and/or serial_number containing the query
        :param request: HttpRequest object containing 'q' for the query
        :return: QuerySet if 'q' is valid, or rc.BAD_REQUEST if not
        """
        if 'q' in request.GET and request.GET['q']:
            query = request.GET['q']
            result = Document.objects.filter(Q(serial_number__icontains=query)|Q(title__icontains=query))
            return result
        else:
            resp = rc.BAD_REQUEST
            resp.write("Need query parameter")
            return resp
            
  