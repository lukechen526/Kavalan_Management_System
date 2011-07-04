# Create your views here.
from django.views.generic import TemplateView

class DocumentIndexView(TemplateView):

    template_name = "doc_engine/index.html"

    
    