# -*- coding: utf-8 -*-
from .config import SESSION_ATTACHMENTS_MAX_FILE_SIZE


def filesize(request):
    return {
        'SESSION_ATTACHMENTS_MAX_FILE_SIZE': SESSION_ATTACHMENTS_MAX_FILE_SIZE
    }
