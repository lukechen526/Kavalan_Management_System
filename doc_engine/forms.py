from django import forms
from django.utils.translation import ugettext_lazy
from doc_engine.models import Document, BatchRecord

class DocumentForm(forms.ModelForm):
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


class BatchRecordInputForm(forms.ModelForm):
    date_manufactured = forms.DateField(label=ugettext_lazy('Date of Manufacture'))
    class Meta:
        model = BatchRecord

class BatchRecordSearchForm(forms.Form):
    name = forms.CharField(label=ugettext_lazy('Product Name'), required=False)
    batch_number = forms.CharField(label=ugettext_lazy('Batch Number'), required=False)
    date_manufactured_from = forms.DateField(label=ugettext_lazy('From'), required=False)
    date_manufactured_to = forms.DateField(label=ugettext_lazy('To'), required=False)


