from piston.handler import BaseHandler
from piston.utils import *
from doc_engine.models import StoredDocument, BatchRecord
from django.db.models import Q
from dynamo.core import build_query
from doc_engine.forms import DocumentSearchForm, BatchRecordSearchForm
import json
from django.core.cache import cache
import pickle

def get_documents(query_str):

    #Tries to load the result from cache first, using the query string as
    result = cache.get(query_str.replace(' ', '')) #To be compatible with Memcached, all whitespaces have to be removed from the cache key
    if result:
        return pickle.loads(result) #Memcached returns a pickled QuerySet that needs to be unpickled before returning to the client

    #If not result is in the cache, then retrieves Documents from the database
    try:
        query = json.loads(query_str)
    except:
        query = dict()

    query = DocumentSearchForm(query)

    if not query.is_valid():
        resp = rc.BAD_REQUEST
        resp.write(str(query.errors))
        return resp

    sn_title = query.cleaned_data['sn_title']
    document_level = query.cleaned_data['document_level']
    tags = query.cleaned_data['tags']

    result = StoredDocument.objects.filter(searchable=True)

    if sn_title:
        q = Q()
        keywords = sn_title.split() #split the query string into keywords

        for kw in keywords:
            #For every keyword, looks it up in either serial number or title.
            #A document is included in the result if EVERY keyword in the query string is present in either
            #its serial number OR title.
            q = q & (Q(serial_number__icontains=kw)|Q(title__icontains=kw))

        result = result.filter(q)

    if document_level:
        result = result.filter(document_level__exact=document_level)

    if tags:
        for label in tags:
            #Apply AND operation to labels
            result = result.filter(labels__in=[label])

        result = result.distinct()

    if sn_title is None and document_level is None and tags is None:
        #If no search criteria were specified, results an empty list.
        result = []

    #Caches the result before returning it to the client
    cache.set(query_str.replace(' ',''), pickle.dumps(result))
    
    return result

class DocumentHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = StoredDocument
    fields = ('id','title', 'serial_number', 'version', 'file_url', 'location', ('labels',('content',)))

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

    #Tries to load the result from cache first, using the query string as
    result = cache.get(query_str.replace(' ', '')) #To be compatible with Memcached, all whitespaces have to be removed from the cache key
    if result:
        return pickle.loads(result) #Memcached returns a pickled QuerySet that needs to be unpickled before returning to the client

    #If not result is in the cache, then retrieves Documents from the database
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
        query['filters'].append(dict(field='date_of_manufacture',
                                     lookuptype='gte',
                                     value=date_manufactured_from,
                                     op='AND',
                                     exclude=False))

    if date_manufactured_to:
        query['filters'].append(dict(field='date_of_manufacture',
                                     lookuptype='lte',
                                     value=date_manufactured_to,
                                     op='AND',
                                     exclude=False))
    
    if not query['filters']:
        #Needs at least one filter
        resp = rc.BAD_REQUEST
        resp.write("At least one search criterion needs to be entered.")
        return resp

    else:
        result = build_query(query, BatchRecord)

        #Caches the result before returning it to the client
        cache.set(query_str.replace(' ',''), pickle.dumps(result))
        
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

