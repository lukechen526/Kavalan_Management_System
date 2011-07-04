from piston.handler import BaseHandler
from piston.utils import *
from doc_engine.models import Document, BatchRecord
from django.db.models import Q

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

class BatchRecordHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = BatchRecord
    fields = ('name', )