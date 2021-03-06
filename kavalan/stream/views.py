from django.views.generic import TemplateView
from django import forms
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy

class StreamIndexView(TemplateView):
    def get_context_data(self, **kwargs):

        if self.request.user.is_superuser:
        #Allows a superuser to broadcast to all groups
            class UserGroupSelectForm(forms.Form):
                groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                                        widget=forms.SelectMultiple(attrs={'data-placeholder':ugettext_lazy('Select one or more groups')}))
        else:
        #Otherwise, the user can only post to groups to which he/she belongs
            class UserGroupSelectForm(forms.Form):
                groups = forms.ModelMultipleChoiceField(queryset=self.request.user.groups.all(),
                                                        widget=forms.SelectMultiple(attrs={'data-placeholder':ugettext_lazy('Select one or more groups')}))
        context = super(StreamIndexView, self).get_context_data(**kwargs)
        context['user_group_select_form'] = UserGroupSelectForm()
        return context
