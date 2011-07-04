from django.contrib import admin
from doc_engine.models import Document, BatchRecord, BatchRecordInputForm

class BatchRecordAdmin(admin.ModelAdmin):
    form = BatchRecordInputForm
    
admin.site.register(Document)
admin.site.register(BatchRecord, BatchRecordAdmin)
  