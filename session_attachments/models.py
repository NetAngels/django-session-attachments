# -*- coding: utf-8 -*-
from django.db import models


class Attachment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=40)
    bundle = models.CharField(max_length=256)
    file = models.FileField(upload_to='session_attachments')
