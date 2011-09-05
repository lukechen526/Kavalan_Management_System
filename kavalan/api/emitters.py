from piston.emitters import JSONEmitter, DateTimeAwareJSONEncoder, Emitter
from django.core.paginator import Paginator, EmptyPage
from piston.validate_jsonp import is_valid_jsonp_callback_value
import json

class PageJSONEmitter(JSONEmitter):
    """
    A JSONEmitter supporting DjangoPagination by adding two parameters, num_pages and page_number (of the current page)
    """
    def render(self, request):
        cb = request.GET.get('callback', None)
        try:
            per_page = int(request.GET.get('per_page', 10))
        except ValueError:
            per_page = 10
        try:
            page_number = int(request.GET.get('page_number', 1))
        except ValueError:
            page_number = 1
            
        pages = Paginator(self.construct(), per_page)
        
        try:
            page = pages.page(page_number)
        except EmptyPage:
            page = pages.page(1)

        data = {'num_pages': pages.num_pages,
                'page_number': page_number,
                'data': page.object_list
                }

        serial = json.dumps(data, cls=DateTimeAwareJSONEncoder, ensure_ascii=False, indent=4)

        # Callback
        if cb and is_valid_jsonp_callback_value(cb):
            return '%s(%s)' % (cb, serial)

        return serial

Emitter.register('page_json', PageJSONEmitter, 'application/json; charset=utf-8')
  