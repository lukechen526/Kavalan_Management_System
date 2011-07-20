from piston.handler import BaseHandler
from piston.utils import *
from doc_engine.models import Document, BatchRecord
from django.db.models import Q
from dynamo.core import build_query
from doc_engine.models import BatchRecordSearchForm
from piston.utils import validate

class DocumentHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Document
    fields = ('title', 'serial_number', 'version', 'file_url')

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
            resp.write("Needs a query parameter")
            return resp

class BatchRecordHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = BatchRecord
    fields = ('name', 'batch_number', 'date_manufactured', 'location')

    @validate(BatchRecordSearchForm, 'GET')
    def read(self, request):
        query = dict()
        query['filters'] = []

        if 'name' in request.GET and request.GET['name']:
            query['filters'].append(dict(field='name',
                                         lookuptype='icontains',
                                         value=request.GET['name'],
                                         op='AND',
                                         exclude=False))

        if 'batch_number' in request.GET and request.GET['batch_number']:
            query['filters'].append(dict(field='batch_number',
                                         lookuptype='icontains',
                                         value=request.GET['batch_number'],
                                         op='AND',
                                         exclude=False))

        if 'date_manufactured_from' in request.GET and request.GET['date_manufactured_from']:
            query['filters'].append(dict(field='date_manufactured',
                                         lookuptype='gte',
                                         value=request.GET['date_manufactured_from'],
                                         op='AND',
                                         exclude=False))

        if 'date_manufactured_to' in request.GET and request.GET['date_manufactured_to']:
            query['filters'].append(dict(field='date_manufactured',
                                         lookuptype='lte',
                                         value=request.GET['date_manufactured_to'],
                                         op='AND',
                                         exclude=False))
        if not query['filters']:
            #Needs at least one filter
            resp = rc.BAD_REQUEST
            resp.write("Needs at least one filter")
            return resp

        else:
            result = build_query(query, BatchRecord)
            return result


