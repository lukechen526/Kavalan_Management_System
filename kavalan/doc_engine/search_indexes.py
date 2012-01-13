# _*_ coding: UTF-8 _*_
from doc_engine.models import StoredDocument
from haystack import indexes
from django.conf import settings
from django.template import loader, Context
import mimetypes
import os
from django.utils.encoding import smart_str
from django.core.files import File
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

BaseSearch = indexes.RealTimeSearchIndex if getattr(settings, 'HAYSTACK_USE_REALTIME_SEARCH', False) else indexes.SearchIndex


class StoredDocumentIndex(indexes.Indexable, BaseSearch):

    text = indexes.CharField(document=True, use_template=True)
    tags = indexes.MultiValueField()
    document_level = indexes.CharField(model_attr='document_level')
    name_auto = indexes.NgramField()

    def get_model(self):
        return StoredDocument

    def prepare_tags(self, obj):
        return [tag.tag for tag in obj.tags.all()]

    def prepare_name_auto(self, obj):
        return "%s %s" %(obj.serial_number, obj.name)

    def prepare(self, obj):
        data = super(StoredDocumentIndex, self).prepare(obj)

        # This could also be a regular Python open() call, a StringIO instance
        # or the result of opening a URL. Note that due to a library limitation
        # file_obj must have a .name attribute even if you need to set one
        # manually before calling extract_file_contents:

        filepath = obj.file.name
        
        try:
            if filepath :
                mimetype = mimetypes.guess_type(filepath)

                if mimetype[0] == 'application/pdf' or mimetype[0] == 'application/msword':
                    with open(os.path.join(settings.MEDIA_ROOT, filepath), 'rb') as file_obj:

                        file_obj = File(file_obj)

                        # Create a unique file name containing only ASCII characters
                        extension = os.path.splitext(file_obj.name)[1]
                        file_obj.name = "".join([x for x in "%sv%s" %(smart_str(obj.serial_number), smart_str(obj.version)) if x.isalpha() or x.isdigit()]) + extension

                        # Extract the file content
                        extracted_data = self._get_backend(None).extract_file_contents(file_obj)
                else:
                    extracted_data = dict()
            else:
                extracted_data = dict()
        except Exception as e:
            print e
            extracted_data = dict()
        # Now we'll finally perform the template processing to render the
        # text field with *all* of our metadata visible for templating:
        t = loader.select_template(('search/indexes/doc_engine/storeddocument_text.txt', ))
        data['text'] = t.render(Context({'object': obj,
                                         'extracted': extracted_data}))

        return data
