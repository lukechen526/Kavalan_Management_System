#API for Stream
from piston.handler import BaseHandler
from piston.utils import *
from stream.models import StreamPost, StreamPostComment


class StreamHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = StreamPost
    fields = ('id', ('poster',('username', 'last_name', 'first_name')), 'time_posted', 'content', 'link', 'comment_count' )


    def read(self, request):
        user = request.user
        offset = request.GET.get('offset', 0)

        #Retrieves the user's group in a list
        groups = user.groups.all().values_list('id', flat=True).order_by('id')
        #Retrieves the posts accessible to those groups, sorted by rank. Limits the number of results to 10.
        return StreamPost.objects.filter(groups__id__in=groups)[offset: offset+10]

    def create(self,request):
        pass

    def update(self, request):
        pass

    def delete(self, request):
        pass
