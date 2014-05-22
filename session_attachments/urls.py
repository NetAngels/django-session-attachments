# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('session_attachments.views',
    url(r'^(?P<bundle_id>[^/]+)/$', 'bundle_attachments', name='bundle-attachments'),
    url(r'^(?P<bundle_id>[^/]+)/delete/$', 'delete_bundle_attachments', name='delete-bundle-attachments'),
    url(r'^(?P<bundle_id>[^/]+)/(?P<file_name>[^/]+)/$', 'get_filename_attachment', name='get-filename-attachment'),
    url(r'^(?P<bundle_id>[^/]+)/(?P<file_name>[^/]+)/delete/$', 'delete_filename_attachment', name='delete-filename-attachment'),
)
