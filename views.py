#Add the view functions here
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"


    
  