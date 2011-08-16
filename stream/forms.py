from stream.models import StreamPost, StreamPostComment
from django.forms import ModelForm

class StreamPostValidationForm(ModelForm):
    class Meta:
        model = StreamPost
        fields = ('groups', 'content', 'link')

class StreamPostCommentValidationForm(ModelForm):
    class Meta:
        model = StreamPostComment
        fields = ('content',)