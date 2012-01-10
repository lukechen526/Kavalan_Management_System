from django.contrib import admin
from doc_engine.models import StoredDocument, AccessRecord, BatchRecord, Tag
from doc_engine.forms import BatchRecordInputForm
import reversion

class StoredDocumentAdmin(reversion.VersionAdmin):
    pass


class BatchRecordAdmin(reversion.VersionAdmin):
    form = BatchRecordInputForm

    class Media:
        js = ('js/jquery-1.6.2.min.js', 'js/jquery-ui-1.8.14.custom.min.js', 'js/chosen.jquery.min.js', 'doc_engine/js/doc-engine.js')
        css ={'all':('css/custom-theme/jquery-ui-1.8.14.custom.css',)}

admin.site.register(Tag)
admin.site.register(StoredDocument, StoredDocumentAdmin)
admin.site.register(AccessRecord)
admin.site.register(BatchRecord, BatchRecordAdmin)
  