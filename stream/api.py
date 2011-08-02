#API for Stream
from piston.handler import BaseHandler
from piston.utils import *
from stream.models import StreamPost, StreamPostComment, StreamPostValidationForm
from django.utils.translation import ugettext
import json



class StreamHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = StreamPost
    fields = ('id', ('groups',('id', 'name')), ('poster',('username', 'last_name', 'first_name')),
              'processed_content', 'formatted_time_posted', 'link', 'comment_count', 'rank'  )

    def read(self, request, post_id=None):
        user = request.user
        offset = int(request.GET.get('offset', 0))

        #Retrieves the user's group in a list
        groups = user.groups.all().values_list('id', flat=True).order_by('id')
        #Retrieves the posts accessible to those groups, sorted by rank.
        posts = StreamPost.objects.filter(groups__id__in=groups).distinct('id')
        if post_id:
            post_id = int(post_id)
            return posts.filter(id=post_id)
        else:
            #If no post_id was specified, returns 10 results, offset by 'offset'.
            return posts[offset:offset+10]


    def create(self,request, post_id=None):

        #Checks if there is a parameter 'model' in the request, created by Backbone.js
        model = request.POST.get('model', '')

        if model:
            post = StreamPostValidationForm(json.loads(model))
        else:
            post = StreamPostValidationForm(request.POST)

        if post.is_valid():
            #Checks that either content or link is non-empty
            if not post.cleaned_data['content'] and not post.cleaned_data['link']:
                resp = rc.BAD_REQUEST
                resp.write(ugettext('Either content or link has to be non-empty'))
                return resp

            #If all fields are valid, save the post
            saved_post = post.save(commit=False)
            saved_post.poster = request.user
            saved_post.save()
            post.save_m2m()
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
            post_id = int(post_id)
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
            post = StreamPostValidationForm(json.loads(model), instance=post)
        else:
            post = StreamPostValidationForm(request.POST, instance=post)

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
            post_id = int(post_id)
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
