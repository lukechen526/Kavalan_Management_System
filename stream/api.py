#API for Stream
from piston.handler import BaseHandler
from piston.utils import *
from stream.models import StreamPost, StreamPostComment

class StreamHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = StreamPost
    fields = ('poster', 'time_posted', 'content', 'link', 'comment_count' )


    def read(self, request):
        user = request.user
        offset = request.GET.get('offset', 0)
        
