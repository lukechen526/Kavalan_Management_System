from django import forms
from django.utils.translation import ugettext_lazy
from doc_engine.models import StoredDocument, BatchRecord, Tag


class DocumentSearchForm(forms.Form):

    qw = forms.CharField(label=ugettext_lazy('Enter a query word'), required=False)

    document_level = forms.ChoiceField(
        label=ugettext_lazy('Document Level'),
        required=False,
        choices=(('',ugettext_lazy('All results')),)+StoredDocument.DOCUMENT_LEVELS,
        widget = forms.Select(attrs={'data-placeholder':ugettext_lazy('Filter by document level')}))

    tags = forms.ModelMultipleChoiceField(
        label=ugettext_lazy('Tags'),
        required=False,
        queryset=Tag.objects.all(),
        widget = forms.SelectMultiple(attrs={'data-placeholder':ugettext_lazy('Filter by tags')}))

class BatchRecordInputForm(forms.ModelForm):

    date_of_manufacture = forms.DateField(label=ugettext_lazy('Date of Manufacture'))

    class Meta:
        model = BatchRecord

class HTML5DateInput(forms.widgets.DateInput):

    input_type = 'date'

class BatchRecordSearchForm(forms.Form):

    name = forms.CharField(label=ugettext_lazy('Product Name'), required=False)
    batch_number = forms.CharField(label=ugettext_lazy('Batch Number'), required=False)
    date_of_manufacture_from = forms.DateField(
        label=ugettext_lazy('From'),
#        widget=HTML5DateInput,
        required=False)
    date_of_manufacture_to = forms.DateField(
        label=ugettext_lazy('To'),
#        widget=HTML5DateInput,
        required=False)


