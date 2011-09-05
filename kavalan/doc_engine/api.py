from piston.handler import BaseHandler
from piston.utils import *
from doc_engine.models import Document, BatchRecord
from django.db.models import Q
from dynamo.core import build_query
from doc_engine.forms import DocumentSearchForm, BatchRecordSearchForm
from piston.utils import validate
import json

class DocumentHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Document
    fields = ('title', 'serial_number', 'version', 'file_url', 'location', ('labels',('content',)))

    def read(self, request):
        """
        Searches 'Document' for entries with title and/or serial_number containing the query
        :param request: HttpRequest object containing 'q' for the query
        :return: QuerySet if 'q' is valid, or rc.BAD_REQUEST if not
        """
        if request.GET.get('query', None):
            try:
                query = json.loads(request.GET.get('query'))
            except:
                query = dict()

            query = DocumentSearchForm(query)

            if not query.is_valid():
                resp = rc.BAD_REQUEST
                resp.write(str(query.errors))
                return resp

            sn_title = query.cleaned_data['sn_title']
            document_level = query.cleaned_data['document_level']
            labels = query.cleaned_data['labels']

            result = Document.objects.all()
            
            if sn_title:
                result = result.filter(Q(serial_number__icontains=sn_title)|Q(title__icontains=sn_title)).filter(searchable=True)

            if document_level:
                result = result.filter(document_level__exact=document_level)

            if labels:
                for label in labels:
                    #Apply AND operation to labels
                    result = result.filter(labels__in=[label])
                    
                result = result.distinct()

            if not sn_title and not labels:
                #If no sn_title or labels are supplied, returns no result. 
                return []

            return result
        
        else:
            resp = rc.BAD_REQUEST
            resp.write("Needs a query parameter")
            return resp

class BatchRecordHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = BatchRecord
    fields = ('name', 'batch_number', 'date_manufactured', 'date_manufactured_minguo', 'location')

    def read(self, request):
        
        if request.GET.get('query', None):
            try:
                q = json.loads(request.GET.get('query'))
            except:
                q= dict()

            q = BatchRecordSearchForm(q)

            if not q.is_valid():
                resp = rc.BAD_REQUEST
                resp.write(str(q.errors))
                return resp

            name = q.cleaned_data['name']
            batch_number = q.cleaned_data['batch_number']
            date_manufactured_from = q.cleaned_data['date_manufactured_from']
            date_manufactured_to = q.cleaned_data['date_manufactured_to']

            query = dict()
            query['filters'] = []

            if name:
                query['filters'].append(dict(field='name',
                                             lookuptype='icontains',
                                             value=name,
                                             op='AND',
                                             exclude=False))

            if batch_number:
                query['filters'].append(dict(field='batch_number',
                                             lookuptype='icontains',
                                             value=batch_number,
                                             op='AND',
                                             exclude=False))

            if date_manufactured_from:
                query['filters'].append(dict(field='date_manufactured',
                                             lookuptype='gte',
                                             value=date_manufactured_from,
                                             op='AND',
                                             exclude=False))

            if date_manufactured_to:
                query['filters'].append(dict(field='date_manufactured',
                                             lookuptype='lte',
                                             value=date_manufactured_to,
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
        else:
            resp = rc.BAD_REQUEST
            resp.write("Needs a query parameter")
            return resp

