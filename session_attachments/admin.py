# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Attachment


admin.site.register(Attachment, admin.ModelAdmin)
