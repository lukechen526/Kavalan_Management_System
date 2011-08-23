from django.contrib import admin
from doc_engine.models import DocumentLabel, Document, FileObject, AccessRecord, BatchRecord
from doc_engine.forms import DocumentInputForm, BatchRecordInputForm

class FileObjectInline(admin.TabularInline):
    model = FileObject
    readonly_fields = ('file', 'version', 'revision_comment')

class DocumentAdmin(admin.ModelAdmin):
    form = DocumentInputForm
    inlines = [FileObjectInline,]

    list_display = ('serial_number', 'title', 'searchable')
    search_fields = ('serial_number', 'title')
    readonly_fields = ('searchable',)

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
            
            #Save revision comment if it is present
            if form.cleaned_data['revision_comment']:
                file_obj.revision_comment = form.cleaned_data['revision_comment']

            #Save the FileObject
            file_obj.save()

            #Make the Document searchable
            obj.searchable = True
            obj.save()

        else:
            #If no file was uploaded (i.e. only the metadata of the document were changed), then ensure that the version
            #number stored in the document points to an existing FileObject. Otherwise, change the version number to point to the
            #most recently uploaded FileObject. If the Document has no associated FileObjects, then store the version number
            #according to the input. 
            try:
                file_obj = obj.versions.get(version__exact=obj.version)

                #Save revision comment if it is present
                if form.cleaned_data['revision_comment']:
                    file_obj.revision_comment = form.cleaned_data['revision_comment']
                    file_obj.save()
                    
            except FileObject.DoesNotExist:
                #Sets the Document's version to the latest one
                try:
                    file_obj_recent = obj.versions.latest('uploaded_date')
                    obj.version = file_obj_recent.version
                    obj.save()
                except FileObject.DoesNotExist:
                    #If the Document has no FileObject associated with it, then simply ignores the issue and save the
                    #Document as is.
                    pass


class BatchRecordAdmin(admin.ModelAdmin):
    form = BatchRecordInputForm

    class Media:
        js = ('jquery-1.6.1.min.js', 'jquery-ui-1.8.14.custom.min.js','jquery.tmpl.min.js','base.js', 'doc-engine.js')
        css ={'all':('custom-theme/jquery-ui-1.8.14.custom.css',)}

admin.site.register(DocumentLabel)
admin.site.register(Document, DocumentAdmin)
admin.site.register(AccessRecord)
admin.site.register(BatchRecord, BatchRecordAdmin)
  