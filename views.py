from django.views.generic import TemplateView
from stream.models import StreamPostForm

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['stream_post_form'] = StreamPostForm()
        return context



    
  