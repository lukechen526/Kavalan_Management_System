#API for Stream
from piston.handler import BaseHandler
from piston.utils import *
from stream.models import StreamPost, StreamPostComment, StreamPostForm
from django.utils.translation import ugettext
import json



class StreamHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = StreamPost
    fields = ('id', ('groups',('id', 'name')), ('poster',('username', 'last_name', 'first_name')), 'time_posted', 'escaped_content', 'link', 'comment_count' )

    def read(self, request, post_id=None):
        user = request.user
        offset = request.GET.get('offset', 0)

        #Retrieves the user's group in a list
        groups = user.groups.all().values_list('id', flat=True).order_by('id')
        #Retrieves the posts accessible to those groups, sorted by rank.
        posts = StreamPost.objects.filter(groups__id__in=groups).distinct('id')
        if post_id:
            return posts.filter(id=post_id)
        else:
            #If no post_id was specified, returns 20 results, offset by 'offset'.
            return posts[offset:offset+20]


    def create(self,request, post_id=None):

        #Initialize post with user
        post = StreamPost(poster=request.user)

        #Checks if there is a parameter 'model' in the request, created by Backbone.js
        model = request.POST.get('model', '')

        if model:
            post = StreamPostForm(json.loads(model), instance=post)
        else:
            post = StreamPostForm(request.POST, instance=post)

        if post.is_valid():
            #Checks that either content or link is non-empty
            if not post.cleaned_data['content'] and not post.cleaned_data['link']:
                resp = rc.BAD_REQUEST
                resp.write(ugettext('Either content or link has to be non-empty'))
                return resp

            #If all fields are valid, save the post
            saved_post = post.save()
            return saved_post
        else:
            resp = rc.BAD_REQUEST
            resp.write(json.dumps(post.errors))
            return resp
        
    def update(self, request, post_id=None):
        if not post_id:
            resp = rc.BAD_REQUEST
            resp.write(ugettext('StreamPost ID must be supplied'))
            return resp

        try:
            post = StreamPost.objects.get(id=post_id)
        except StreamPost.DoesNotExist:
            resp = rc.NOT_FOUND
            resp.write(ugettext('No StreamPost with the specified ID was found'))
            return resp

        #Checks that the user is the poster
        if request.user != post.poster:
            resp = rc.FORBIDDEN
            resp.write(ugettext('Only the original poster can update the post'))
            return resp
        
        #Checks if there is a parameter 'model' in the request, created by Backbone.js
        model = request.POST.get('model', '')
        if model:
            post = StreamPostForm(json.loads(model), instance=post)
        else:
            post = StreamPostForm(request.POST, instance=post)

        if post.is_valid():
            #Checks that either content or link is non-empty
            if not post.cleaned_data['content'] and not post.cleaned_data['link']:
                resp = rc.BAD_REQUEST
                resp.write(ugettext('Either content or link has to be non-empty'))
                return resp

            #If all fields are valid, update the post
            updated_post = post.save()
            return updated_post
        else:
            resp = rc.BAD_REQUEST
            resp.write(json.dumps(post.errors))
            return resp

    def delete(self, request, post_id=None):
        if not post_id:
            resp = rc.BAD_REQUEST
            resp.write(ugettext('StreamPost ID must be supplied'))
            return resp

        try:
            post = StreamPost.objects.get(id=post_id)
        except StreamPost.DoesNotExist:
            resp = rc.NOT_FOUND
            resp.write(ugettext('No StreamPost with the specified ID was found'))
            return resp

        #Checks that the user is the poster
        if request.user != post.poster:
            resp = rc.FORBIDDEN
            resp.write(ugettext('Only the original poster can delete the post'))
            return resp

        post.delete()
        return rc.DELETED
