# Create your views here.
from django.views.generic import TemplateView
from doc_engine.models import Document, BatchRecordSearchForm, AccessRecord
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from StringIO import StringIO
from reportlab.pdfgen import canvas
from pyPdf import PdfFileWriter, PdfFileReader
import os.path

class DocumentIndexView(TemplateView):
    template_name = "doc_engine/index.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DocumentIndexView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['batch_record_search_form'] = BatchRecordSearchForm(auto_id=True)
        return context

def createPDFHttpResponse(filename, user, access_time):
    #Add access watermark
    buffer = StringIO()
    p = canvas.Canvas(buffer)
    p.drawString(0,0, "Downloaded by %s at %s" %(user, access_time.isoformat(' ')))
    p.showPage()
    p.save()
    buffer.seek(0)

    watermark = PdfFileReader(buffer)
    attachment = PdfFileReader(open(filename, 'rb'))
    output = PdfFileWriter()

    for page in attachment.pages:
        page.mergePage(watermark.getPage(0))
        output.addPage(page)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % attachment.getDocumentInfo().title
    output.write(response)
    return response

def DocumentAccess(request, pk):
    MEDIA_ROOT = settings.MEDIA_ROOT
    user = request.user
    user_groups = user.groups.all()
    document = get_object_or_404(Document, pk=pk)
    document_groups = list(document.permitted_groups.all())

    #Check if the user has the necessary group permission to access the document or is a superuser

    if user.is_superuser:
        record= AccessRecord.objects.create(user=user, ip=request.META['REMOTE_ADDR'], document_accessed=document)
        return createPDFHttpResponse(filename=os.path.join(MEDIA_ROOT, document.file.name),
                                     user=user,
                                     access_time=record.access_time)

    elif user_groups:
        for group in user_groups:
            if group in document_groups:
                #Allows access if the user is in the permitted group
                record = AccessRecord.objects.create(user=user, ip=request.META['REMOTE_ADDR'], document_accessed=document)
                return createPDFHttpResponse(filename=os.path.join(MEDIA_ROOT, document.file.name),
                                            user=user,
                                            access_time=record.access_time)
            
    return HttpResponseForbidden("Access Denied")

    
