# -*- coding: utf-8 -*-
import os
from .models import Attachment


def get_attachments(session_id, bundle_id):
    return Attachment.objects.filter(session_id=session_id, bundle=bundle_id)


def delete_attachments(session_id, bundle_id):
    attachment_list = get_attachments(session_id=session_id, bundle_id=bundle_id)
    result = []
    for attach in attachment_list:
        result.append(delete_and_clean(attach))
    return result


def get_attachment(session_id, bundle_id, file_name):
    attachment_list = get_attachments(session_id=session_id, bundle_id=bundle_id)
    try:
        attach = attachment_list.get(filename=file_name)
    except Attachment.DoesNotExist:
        return None
    return attach


def delete_attachment(session_id, bundle_id, file_name):
    attach = get_attachment(session_id=session_id, bundle_id=bundle_id, file_name=file_name)
    result = delete_and_clean(attach)
    return result


def delete_and_clean(attach=None):
    result = []
    if attach:
        os.unlink(attach.file.path)
        first_parent, second_parent = _get_parents(attach)
        os.rmdir(first_parent)  # it must not happen
        try:
            os.rmdir(second_parent)  # probably, there are other attachments in the same bundle
        except OSError:
            pass
        attach.delete()
        result.append(True)
    else:
        result.append(False)
    return result


def _get_parents(attach):
    first_parent = os.path.dirname(attach.file.path)
    second_parent = os.path.dirname(first_parent)
    return (first_parent, second_parent)
