from piston.handler import BaseHandler
from piston.utils import *
from doc_engine.models import StoredDocument, BatchRecord
from dynamo.core import build_query
from doc_engine.forms import DocumentSearchForm, BatchRecordSearchForm
from haystack.query import SearchQuerySet
from haystack.inputs import Clean, AutoQuery
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage
import json

def get_documents(query_json):

    try:
        query = json.loads(query_json)
    except:
        query = dict()

    query = DocumentSearchForm(query)

    if not query.is_valid():
        return []

    qw = query.cleaned_data['qw']
    document_level = query.cleaned_data['document_level']
    tags = query.cleaned_data['tags']

    if qw is None and document_level is None and tags is None:
        #If no search criteria were specified, results an empty list.
        return []
    else:
        sqs = SearchQuerySet().models(StoredDocument)

        if qw:
            sqs = sqs.filter(content=Clean(qw)).highlight()

        if document_level:
            sqs = sqs.filter(document_level=Clean(document_level))

        if tags:
            for tag in tags:
                #Apply AND operation to labels
                sqs = sqs.filter(tags__contains=Clean(tag.tag))

    return [
    dict(id=sqr.object.id,
        name=sqr.object.name,
        serial_number=sqr.object.serial_number,
        url=sqr.object.get_absolute_url(),
        version=sqr.object.version,
        location=sqr.object.location,
        tags=list(sqr.object.tags.all().values_list('tag', flat=True)),
        highlighted_text= sqr.highlighted['text'][0] if sqr.highlighted else ''
    ) for sqr in sqs.load_all()]


def paginate_results(results, per_page=20, page_number=1):

    try:
        #Checks whether self.construct() supports count() and __len__(); if it doesn't (i.e. it cannot be paginated),
        #returns it unchanged
        getattr(results, 'count'); getattr(results, '__len__')

        pages = Paginator(results, per_page)

        try:
            page = pages.page(page_number)
        except EmptyPage:
            page = pages.page(1)

        resp = {'num_pages': pages.num_pages,
                'page_number': page_number,
                'objects': page.object_list
                }

    except AttributeError:
            resp = {'objects':results}
    
    return resp

def document_search_view(request, document_id=None):
    if document_id:
        try:
            result = StoredDocument.objects.get(id__exact=document_id)
            response = HttpResponse(mimetype='application/json')
            json_serializer = serializers.get_serializer('json')()
            json_serializer.serialize(result, ensure_ascii=False, stream=response)
            return response
        except StoredDocument.DoesNotExist:
            return HttpResponseBadRequest('Invalid Document ID')
    else:
        try:
            per_page = int(request.GET.get('per_page', 20))
        except ValueError:
            per_page = 20
        try:
            page_number = int(request.GET.get('page_number', 1))
        except ValueError:
            page_number = 1

        if request.GET.get('query', None):
            result = paginate_results(get_documents(request.GET.get('query')), per_page, page_number)
        else:
            return HttpResponseBadRequest('Needs a query parameter')

    response = HttpResponse(content=json.dumps(result), mimetype='application/json')
    return response

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
                # Convert SearchQuerySet into a list of Model objects so they can be used by Piston
                return  [sqr.object for sqr in get_documents(request.GET.get('query'))]

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

