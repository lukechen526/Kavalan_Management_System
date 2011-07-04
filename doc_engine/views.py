# Create your views here.
from django.views.generic import TemplateView
from doc_engine.models import BatchRecordSearchForm

class DocumentIndexView(TemplateView):
    template_name = "doc_engine/index.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DocumentIndexView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['batch_record_search_form'] = BatchRecordSearchForm(auto_id=True)
        return context

    
    