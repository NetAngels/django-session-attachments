# -*- coding: utf-8 -*-
import mimetypes
from django.http import HttpResponse, HttpResponseNotFound
from django.utils import simplejson as json
from django.views.decorators.http import require_POST, require_GET
from .models import Attachment
from .utils import get_attachments, get_attachment, delete_attachments, delete_attachment, delete_and_clean
from .decorators import enforce_session
from .config import SESSION_ATTACHMENTS_MAX_FILE_SIZE


@enforce_session
def bundle_attachments(request, bundle_id):
    """ Return the list of attachments in the bundle on GET (list of JSON
    objects), insert new attachments in the bundle on POST """
    data = []
    session_id = request.session.session_key
    if request.method == 'GET':  # get the list of attachments
        if bundle_id:
            attachment_list = get_attachments(session_id=session_id, bundle_id=bundle_id)
            for attach in attachment_list:
                data.append(attach.__json__())
    elif request.method == 'POST':
        if bundle_id:
            for upload_file, file_name in request.FILES.iteritems():
                # check max size
                file_size = request.FILES[upload_file].size / (1024 * 1024)
                if file_size > SESSION_ATTACHMENTS_MAX_FILE_SIZE:
                    return HttpResponse(status=413)

                try:
                    attach = Attachment.objects.get(filename=file_name, bundle=bundle_id)
                except Attachment.DoesNotExist:
                    pass
                else:
                    delete_and_clean(attach)
                attach = Attachment.objects.create(
                    session_id=session_id,
                    bundle=bundle_id,
                    file=request.FILES[upload_file]
                    )
                data.append(attach.__json__())
    json_result = u'%s\r\n' % json.dumps(data)
    return HttpResponse(json_result, 'text/plain; charset=utf-8')


@require_GET
@enforce_session
def get_filename_attachment(request, bundle_id, file_name):
    session_id = request.session.session_key
    attach = get_attachment(session_id=session_id, bundle_id=bundle_id, file_name=file_name)
    if not attach:
        return HttpResponseNotFound()
    response = HttpResponse(attach.file.read())
    response['mimetype'] = mimetypes.guess_type(attach.file.path)[0] or 'octet/stream'
    response['content_disposition'] = 'attachment; filename=%s' % attach.filename
    return response


@require_POST
@enforce_session
def delete_bundle_attachments(request, bundle_id):
    session_id = request.session.session_key
    result = delete_attachments(session_id=session_id, bundle_id=bundle_id)
    json_result = u'%s\r\n' % json.dumps(result)
    return HttpResponse(json_result, 'text/plain; charset=utf-8')


@require_POST
@enforce_session
def delete_filename_attachment(request, bundle_id, file_name):
    session_id = request.session.session_key
    result = delete_attachment(session_id=session_id, bundle_id=bundle_id, file_name=file_name)
    json_result = u'%s\r\n' % json.dumps(result)
    return HttpResponse(json_result, 'text/plain; charset=utf-8')
