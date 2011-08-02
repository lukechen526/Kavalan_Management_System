from django.views.generic import TemplateView
from django import forms
from django.contrib.auth.models import Group



class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):

        class UserGroupSelectForm(forms.Form):
            groups = forms.ModelMultipleChoiceField(queryset=self.request.user.groups.all())
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user_group_select_form'] = UserGroupSelectForm()
        return context



    
  