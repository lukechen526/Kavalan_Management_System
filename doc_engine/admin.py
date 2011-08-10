from django.contrib import admin
from doc_engine.models import Document, FileObject, DocumentForm, AccessRecord, BatchRecord, BatchRecordInputForm

class FileObjectInline(admin.TabularInline):
    model = FileObject

    readonly_fields = ('file', 'version')

class DocumentAdmin(admin.ModelAdmin):
    form = DocumentForm
    inlines = [FileObjectInline,]

    list_display = ('serial_number', 'title')
    search_fields = ('serial_number', 'title')

    def save_model(self, request, obj, form, change):
        obj.save()
        upload_file = request.FILES.get('file', '')
        
        if upload_file:
            #If a new version was uploaded, or a new file was uploaded to overwrite an old file for an existing version

            try:
                #Check if the version corresponds to an existing FileObject. If so, delete the old file from storage first.
                file_obj = obj.versions.get(version__exact=obj.version)
                file_obj.file.delete()

            except FileObject.DoesNotExist:
                #Otherwise, creates a new FileObject for the version
                file_obj = FileObject.objects.create(document=obj, version=obj.version)

            #Save the file to storage
            file_obj.file.save(upload_file.name, upload_file)
            file_obj.save()

        else:
            #If no file was uploaded (i.e. only the metadata of the document were changed), then ensure that the version
            #number stored in the document points to an existing FileObject. Otherwise, change the version number to point to the
            #most recently uploaded FileObject.
            try:
                file_obj = obj.versions.get(version__exact=obj.version)
                pass
            except FileObject.DoesNotExist:
                file_obj_recent = obj.versions.latest('uploaded_date')
                obj.version = file_obj_recent.version
                obj.save()

class BatchRecordAdmin(admin.ModelAdmin):
    form = BatchRecordInputForm

    class Media:
        js = ('js/jquery-1.6.1.min.js', 'js/jquery-ui-1.8.14.custom.min.js','js/jquery.tmpl.min.js','js/main.js')
        css ={'all':('css/custom-theme/jquery-ui-1.8.14.custom.css',)}


admin.site.register(Document, DocumentAdmin)
admin.site.register(AccessRecord)
admin.site.register(BatchRecord, BatchRecordAdmin)
  