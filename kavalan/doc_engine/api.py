from piston.handler import BaseHandler
from piston.utils import *
from doc_engine.models import StoredDocument, BatchRecord
from dynamo.core import build_query
from doc_engine.forms import DocumentSearchForm, BatchRecordSearchForm
import json
from haystack.query import SearchQuerySet

def get_documents(query_str):

    try:
        query = json.loads(query_str)
    except:
        query = dict()

    query = DocumentSearchForm(query)

    if not query.is_valid():
        resp = rc.BAD_REQUEST
        resp.write(str(query.errors))
        return resp

    qw = query.cleaned_data['qw']
    document_level = query.cleaned_data['document_level']
    tags = query.cleaned_data['tags']

    result = StoredDocument.objects.all()

    if qw:
        sqs = SearchQuerySet().auto_query(query_string=qw)
        sqs_pk_list = sqs.values_list('pk', flat=True)
        result = result.filter(pk__in=sqs_pk_list)

    if document_level:
        result = result.filter(document_level__exact=document_level)

    if tags:
        for tag in tags:
            #Apply AND operation to labels
            result = result.filter(tag__in=[tag])

        result = result.distinct()

    if qw is None and document_level is None and tags is None:
        #If no search criteria were specified, results an empty list.
        result = []

    return result

class DocumentHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = StoredDocument
    fields = ('id','name', 'serial_number', 'version', 'file', 'location', ('tags',('tag',)))

    def read(self, request, document_id=None):
        """
        Searches 'Document' for entries with title and/or serial_number containing the query
        :param request: HttpRequest object containing 'q' for the query
        :return: QuerySet if 'q' is valid, or rc.BAD_REQUEST if not
        """
        
        if document_id:
            #If document_id was specified, tries to return the requested object; otherwise, throws an error
            try:
                return StoredDocument.objects.get(id__exact=document_id)
            except StoredDocument.DoesNotExist:
                resp = rc.BAD_REQUEST
                resp.write('Invalid Document ID')
                return resp
        else:
            #Otherwise, returns Documents that match the specified query parameters
            if request.GET.get('query', None):    
                return get_documents(request.GET.get('query'))
            else:
                resp = rc.BAD_REQUEST
                resp.write("Needs a query parameter")
                return resp

def get_batchrecords(query_str):

    try:
        q = json.loads(query_str)
    except:
        q= dict()
    q = BatchRecordSearchForm(q)

    if not q.is_valid():
        resp = rc.BAD_REQUEST
        resp.write(str(q.errors))
        return resp

    name = q.cleaned_data['name']
    batch_number = q.cleaned_data['batch_number']
    date_of_manufacture_from = q.cleaned_data['date_of_manufacture_from']
    date_of_manufacture_to = q.cleaned_data['date_of_manufacture_to']

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

    if date_of_manufacture_from:
        query['filters'].append(dict(field='date_of_manufacture',
                                     lookuptype='gte',
                                     value=date_of_manufacture_from,
                                     op='AND',
                                     exclude=False))

    if date_of_manufacture_to:
        query['filters'].append(dict(field='date_of_manufacture',
                                     lookuptype='lte',
                                     value=date_of_manufacture_to,
                                     op='AND',
                                     exclude=False))
    
    if not query['filters']:
        #Needs at least one filter
        resp = rc.BAD_REQUEST
        resp.write("At least one search criterion needs to be entered.")
        return resp

    else:
        result = build_query(query, BatchRecord)

        return result

            
class BatchRecordHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = BatchRecord
    fields = ('id','name', 'batch_number', 'date_of_manufacture', 'date_of_manufacture_in_minguo', 'location')

    def read(self, request, batchrecord_id=None):

        if batchrecord_id:
            #If batchrecord_id was specified, tries to return the requested object; otherwise, throws an error
            try:
                return BatchRecord.objects.get(id__exact=batchrecord_id)
            except BatchRecord.DoesNotExist:
                resp = rc.BAD_REQUEST
                resp.write('Invalid BatchRecord ID')
                return resp
        else:
            if request.GET.get('query', None):
                return get_batchrecords(request.GET.get('query'))
            else:
                resp = rc.BAD_REQUEST
                resp.write("No 'query' parameter was found.")
                return resp

