from django.contrib import admin
from doc_engine.models import Document, AccessRecord, BatchRecord, BatchRecordInputForm

class BatchRecordAdmin(admin.ModelAdmin):
    form = BatchRecordInputForm

    class Media:
        js = ('js/jquery-1.6.1.min.js', 'js/jquery-ui-1.8.14.custom.min.js','js/jquery.tmpl.min.js','js/main.js')
        css ={'all':('css/custom-theme/jquery-ui-1.8.14.custom.css',)}
    
admin.site.register(Document)
admin.site.register(AccessRecord)
admin.site.register(BatchRecord, BatchRecordAdmin)
  