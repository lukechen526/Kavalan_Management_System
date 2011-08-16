#API for Stream
from piston.handler import BaseHandler
from piston.utils import *
from stream.models import StreamPost, StreamPostComment
from stream.forms import StreamPostValidationForm, StreamPostCommentValidationForm
from django.utils.translation import ugettext
import json



class StreamHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = StreamPost
    fields = ('id', ('groups',('id', 'name')), ('poster',('username', ('profile', ('full_name',)))),
              'processed_content', 'formatted_time_posted', 'link', 'comment_count', 'rank'  )

    def read(self, request, post_id=None):
        user = request.user
        offset = int(request.GET.get('offset', 0))
        num_posts = int(request.GET.get('num_posts', 10))

        #Retrieves the user's group in a list
        groups = user.groups.all().values_list('id', flat=True).order_by('id')
        #Retrieves the posts accessible to those groups, sorted by rank.
        posts = StreamPost.objects.filter(groups__id__in=groups).distinct('id')
        if post_id:
            try:
                return posts.get(id__exact=post_id)
            
            except StreamPost.DoesNotExist:
                resp = rc.BAD_REQUEST
                resp.write('Invalid Post ID')
                return resp
        else:
            #If no post_id was specified, returns 'num_posts' results, offset by 'offset'.
            return posts[offset:offset+num_posts]


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


class StreamCommentHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = StreamPostComment
    fields = ('id',
              ('poster',('username', 'last_name', 'first_name')),
              'formatted_time_posted',
              'processed_content')

    def read(self, request, post_id=None, comment_id=None):
        user = request.user
        groups = user.groups.all().values_list('id', flat=True).order_by('id')

        #Find a post that matches the given post_id and belongs to one of the request
        #user's groups
        if post_id:
            try:
                post = StreamPost.objects.get(id__exact=int(post_id), groups__id__in=groups)
                return post.comments.all()
            except StreamPost.DoesNotExist:
                resp = rc.BAD_REQUEST
                resp.write(ugettext('No post has the specified ID, or the user has no permission to access it'))
                return resp
        else:
            resp = rc.BAD_REQUEST
            resp.write(ugettext('No Post ID was supplied!'))
            return resp

    def create(self, request, post_id=None, comment_id=None):
        user = request.user
        groups = user.groups.all().values_list('id', flat=True).order_by('id')

        model = request.POST.get('model', '')
        if model:
            comment = StreamPostCommentValidationForm(json.loads(model))
        else:
            comment = StreamPostCommentValidationForm(request.POST)

        #Find a post that matches the given post_id and belongs to one of the request
        #user's groups
        if post_id:
            try:
                post = StreamPost.objects.get(id__exact=int(post_id), groups__id__in=groups)
                if comment.is_valid():
                    comment = StreamPostComment.objects.create(poster=request.user,
                                                           stream_post=post,
                                                           content=comment.cleaned_data['content'])
                    return comment
                else:
                    resp = rc.BAD_REQUEST
                    resp.write(ugettext('Invalid content'))
                    return resp
            except StreamPost.DoesNotExist:
                resp = rc.BAD_REQUEST
                resp.write(ugettext('No post has the specified ID, or the user has no permission to access it'))
                return resp

        else:
            resp = rc.BAD_REQUEST
            resp.write(ugettext('No Post ID was supplied!'))
            return resp

    def update(self, request, post_id=None, comment_id=None):
        user = request.user
        if not (post_id and comment_id):
            resp = rc.BAD_REQUEST
            resp.write(ugettext('Both Post and Comment IDs must be supplied!'))
            return resp

        model = request.POST.get('model', '')
        if model:
            comment_update = StreamPostCommentValidationForm(json.loads(model))
        else:
            comment_update = StreamPostCommentValidationForm(request.POST)
        
        try:
            comment = StreamPostComment.objects.get(stream_post__id__exact=int(post_id),
                                                    id__exact=int(comment_id))
            if user != comment.poster:
                resp = rc.FORBIDDEN
                resp.write(ugettext('Only the original poster can update the comment!'))
                return resp
            
            if comment_update.is_valid():
                comment.content = comment_update.cleaned_data['content']
                comment.save()
                return comment
            else:
                resp = rc.BAD_REQUEST
                resp.write(ugettext('Invalid content'))
                return resp
            
        except StreamPostComment.DoesNotExist:
            resp = rc.BAD_REQUEST
            resp.write(ugettext('Invalid Post or Comment ID'))
            return resp
        
    def delete(self, request, post_id=None, comment_id=None):
        user = request.user
        if not (post_id and comment_id):
            resp = rc.BAD_REQUEST
            resp.write(ugettext('Both Post and Comment IDs must be supplied!'))
            return resp

        try:
            comment = StreamPostComment.objects.get(stream_post__id__exact=int(post_id),
                                                    id__exact=int(comment_id))
            if user != comment.poster:
                resp = rc.FORBIDDEN
                resp.write(ugettext('Only the original poster can delete the comment!'))
                return resp
            
            comment.delete()
            return rc.DELETED
        
        except StreamPostComment.DoesNotExist:
            resp = rc.BAD_REQUEST
            resp.write(ugettext('Invalid Post or Comment ID'))
            return resp



        
        



        

    