# -*- coding: utf-8 -*-
from django.conf import settings

SESSION_ATTACHMENTS_MAX_FILE_SIZE = getattr(settings, "SESSION_ATTACHMENTS_MAX_FILE_SIZE", 50)

NFS_WAIT_TIME = getattr(settings, "NFS_WAIT_TIME", 1) # in seconds
