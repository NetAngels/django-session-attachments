# -*- coding: utf-8 -*-
import os
import hashlib
import mimetypes
from django.db import models
from django.conf import settings


class Attachment(models.Model):

    def file_upload_to(instance, filename):
        md5 = hashlib.md5()
        md5.update(instance.session_id)
        md5.update(instance.bundle)
        md5.update(instance.session_id)
        md5.update(settings.SECRET_KEY)
        digest = md5.hexdigest()
        filename_digest = hashlib.md5(filename).hexdigest()
        return 'session_attachments/%s/%s/%s' % (digest, filename_digest, filename)

    created = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=40)
    bundle = models.CharField(max_length=256)
    file = models.FileField(upload_to=file_upload_to, max_length=1024)
    filename = models.CharField(max_length=100, editable=False)

    def save(self, *args, **kwargs):
        file_basename = os.path.basename(self.file.name)
        self.filename = file_basename
        super(Attachment, self).save(*args, **kwargs)


    @property
    def created_str(self):
        return self.created.strftime('%Y-%m-%d %H:%M')

    @property
    def mimetype(self):
        return mimetypes.guess_type(self.file.path)[0] or 'octet/stream'

    def __json__(self):
        return {
            'created': self.created_str,
            'name': self.filename,
            'size': self.file.size,
            'mimetype': self.mimetype
        }
