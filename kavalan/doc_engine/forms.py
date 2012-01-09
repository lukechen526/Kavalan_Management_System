from django import forms
from django.utils.translation import ugettext_lazy
from doc_engine.models import Document, BatchRecord, DocumentLabel

class DocumentInputForm(forms.ModelForm):
    file = forms.FileField(label=ugettext_lazy('File'), required=False,
                           help_text=ugettext_lazy("Upload a new version of the document, or keep the same version number but\
                           upload a new file to overwrite the old one. \
                           If you are just changing the version number, do not upload any file." ))

    version = forms.CharField(label=ugettext_lazy('Active Version'),
                              initial='1.0',
                              help_text=ugettext_lazy('Enter a new version number, or pick a previous version number to make it active.'))

    revision_comment = forms.CharField(label=ugettext_lazy('Revision Comment'), widget=forms.Textarea, required=False)

    class Meta:
        model = Document

class DocumentSearchForm(forms.Form):
    sn_title = forms.CharField(label=ugettext_lazy('Enter Serial Number/Document Title'), required=False)

    document_level = forms.ChoiceField(label=ugettext_lazy('Document Level'), required=False, choices=(('',ugettext_lazy('All results')),)+Document.DOCUMENT_LEVELS,
                                       widget = forms.Select(attrs={'data-placeholder':ugettext_lazy('Filter by document level')}))

    labels = forms.ModelMultipleChoiceField(label=ugettext_lazy('Labels'), required=False, queryset=DocumentLabel.objects.all(),
                                            widget = forms.SelectMultiple(attrs={'data-placeholder':ugettext_lazy('Filter by labels')}))

class BatchRecordInputForm(forms.ModelForm):
    date_manufactured = forms.DateField(label=ugettext_lazy('Date of Manufacture'))
    class Meta:
        model = BatchRecord



class HTML5DateInput(forms.widgets.DateInput):
    input_type = 'date'



class BatchRecordSearchForm(forms.Form):
    name = forms.CharField(label=ugettext_lazy('Product Name'), required=False)
    batch_number = forms.CharField(label=ugettext_lazy('Batch Number'), required=False)
    date_manufactured_from = forms.DateField(
        label=ugettext_lazy('From'),
#        widget=HTML5DateInput,
        required=False)
    date_manufactured_to = forms.DateField(
        label=ugettext_lazy('To'),
#        widget=HTML5DateInput,
        required=False)


