from django.views.generic import TemplateView
from doc_engine.models import StoredDocument,  AccessRecord
from doc_engine.forms import DocumentSearchForm, BatchRecordSearchForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from reportlab.pdfgen import canvas
from pyPdf import PdfFileWriter, PdfFileReader
from django.utils.translation import ugettext
from django.utils.encoding import smart_str
from django.conf import settings
import os
import mimetypes
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from haystack.query import SearchQuerySet
from haystack.inputs import Clean
import json

class DocumentIndexView(TemplateView):
    """

    Displays the index page for Doc Engine

    """
    template_name = "doc_engine/document_index.html"
    
    def get_context_data(self, **kwargs):
        context = super(DocumentIndexView, self).get_context_data(**kwargs)
        context['document_search_form'] = DocumentSearchForm(auto_id=True)
        context['batch_record_search_form'] = BatchRecordSearchForm(auto_id=True)
        return context

def create_file_http_response(filepath, output_filename, user, access_time):
    """
    Creates a HttpResponse from the file at *filepath*. If the MIMETYPE of the file is PDF, passes the request to
    create_pdf_http_response to add watermark.
    
    :param filepath: Path to the file
    :param output_filename: File name sent to the user
    :param user:
    :param access_time:
    :return: HttpResponse with the file content, or HttpResponseNotFound
    
    """
    
    #check if the file exists. Return 404 if not
    if not os.access(filepath, os.F_OK):
        return HttpResponseNotFound("File Not Found")

    #Check the mimetype of the file
    mimetype = mimetypes.guess_type(filepath)

    #Add access watermark to PDF if configured in settings. Otherwise, it will be rendered as a file.
    if mimetype[0] == 'application/pdf' and getattr(settings, 'PDF_WATERMARK', False):
       return create_pdf_http_response(filepath, output_filename, user, access_time)
    
    else:

        #Only serve file from Django in development mode; otherwise, use X-sendfile
        if settings.DEBUG:
            response = HttpResponse(mimetype=mimetype[0])
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(output_filename)

            with open(filepath, 'rb') as f:
                buffer = StringIO()
                for line in f.readlines():
                    buffer.write(line)
            attachment = buffer.getvalue()
            buffer.close()
            response.write(attachment)
            return response
        else:
            response = HttpResponse(mimetype='application/force-download')
            del response['content-type'] #Leave it to the server to decide
            response['X-Sendfile'] = smart_str(filepath)
            response['Content-Disposition'] = 'attachment; filename="%s"' % smart_str(output_filename)
            return response


def create_pdf_http_response(filepath, output_filename, user, access_time):
    """
    Creates a HttpResponse from a watermarked PDF file. Watermark contains the user who accessed the document
    and the time of access.

    :param filepath: Path to the file
    :param output_filename: File name sent to the user
    :param user:
    :param access_time:
    :return: HttpResponse with the file content, or HttpResponseNotFound
    
    """
    buffer = StringIO()
    p = canvas.Canvas(buffer)
    p.drawString(0,0, "Downloaded by %s at %s" %(user, access_time.isoformat(' ')))
    p.showPage()
    p.save()
    buffer.seek(0)
    watermark = PdfFileReader(buffer)

    #Read the PDF to be accessed
    attachment = PdfFileReader(open(filepath, 'rb'))
    output = PdfFileWriter()

    #Attach watermark to each page
    for page in attachment.pages:
        page.mergePage(watermark.getPage(0))
        output.addPage(page)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'inline; filename=%s' % smart_str(output_filename)
    output.write(response)
    return response


def document_access(request, pk):
    """
    Searches for the requested document with the given primary key, then checks if the user belongs to a group
    that has the permission to access the document. 
    :param request:
    :param pk: primary key of the document to be accessed
    :return: returns the requested document as a PDF file or raises Http errors
    
    """
    MEDIA_ROOT = settings.MEDIA_ROOT
    user = request.user
    user_groups = user.groups.all()
    document = get_object_or_404(StoredDocument, pk=pk)
    document_groups = list(document.permitted_groups.all())
    if not document.file.name:
        return HttpResponseNotFound(ugettext('No stored file found!'))

    filepath = os.path.join(MEDIA_ROOT, document.file.name)
    #Generate safe file names for output based on document's serial number and version; the extension should be preserved
    extension = os.path.splitext(filepath)[1]
    output_filename = "".join([x for x in u"%sv%s" %(document.serial_number, document.version) if x.isalpha() or x.isdigit()]) + extension

    #Check if the user has the necessary group permission to access the document or is a superuser
    if user.is_superuser:
        record= AccessRecord.objects.create(user=user, ip=request.META['REMOTE_ADDR'], item_accessed=document, success=True)
        return create_file_http_response(filepath=filepath,
                                      output_filename=output_filename,
                                      user=user,
                                      access_time=record.access_time)
    elif user_groups:
        for group in user_groups:
            if group in document_groups:
                #Allows access if the user is in the permitted group
                record = AccessRecord.objects.create(user=user, ip=request.META['REMOTE_ADDR'], item_accessed=document, success=True)
                return create_file_http_response(filepath=filepath,
                                              output_filename=output_filename,
                                              user=user,
                                              access_time=record.access_time)

    #If the user is not authorized, record the attempt, and then return error 403
    record = AccessRecord.objects.create(user=user, ip=request.META['REMOTE_ADDR'], item_accessed=document, success=False)
    return HttpResponseForbidden(ugettext("Access Denied"))

    
def autocomplete(request):
    term = request.GET.get('term', '')
    if term:
        sqs = SearchQuerySet().autocomplete(name_auto=term)
        keywords = [dict(id=sqr.pk, value=sqr.name_auto) for sqr in sqs]
    else:
        keywords = []

    return HttpResponse(json.dumps(keywords), mimetype='application/json')