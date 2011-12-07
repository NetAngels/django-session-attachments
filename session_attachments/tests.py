# -*- coding: utf-8 -*-
import os
from django.utils import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.importlib import import_module
from .models import Attachment
from .utils import delete_and_clean


class AttachmentsTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

        filepath = open(u'/tmp/test.png', 'w')
        filepath.write('123456\n')
        filepath.close()
        self.filepath = (u'/tmp/test.png')

        filepath1 = open(u'/tmp/test.doc', 'w')
        filepath1.write('7890\n')
        filepath1.close()
        self.filepath1 = (u'/tmp/test.doc')

        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store

        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def testBundleAttachment(self):
        '''test for one attachment'''
        client = self.client
        filepath = self.filepath
        attachment = open(filepath)
        url = reverse('bundle-attachments', kwargs={'bundle_id': 'test'})
        client.post(url, {'attachment': attachment})
        attachment.seek(0)
        upload_file = attachment.read()
        attachment.close()
        Attachment.objects.get(bundle='test', filename='test.png')
        attachments_count = Attachment.objects.all().count()
        response = client.get(url)
        self.assertTrue('test.png' in response._container[0])
        url = reverse('get-filename-attachment', kwargs={'bundle_id': 'test', 'file_name': 'test.png'})
        response = client.get(url)
        download_file = response.content
        self.assertEqual(upload_file, download_file)
        url = reverse('delete-filename-attachment', kwargs={'bundle_id': 'test', 'file_name': 'test.png'})
        client.post(url)
        new_attachment_count = Attachment.objects.all().count()
        self.assertTrue(new_attachment_count == (attachments_count - 1))

    def testBundleAttachments(self):
        '''test for many attachments'''
        client = self.client
        filepath = self.filepath
        filepath1 = self.filepath1
        attachment = open(filepath)
        attachment1 = open(filepath1)
        url = reverse('bundle-attachments', kwargs={'bundle_id': 'test'})
        client.post(url, {'attachment': attachment, 'attachment1': attachment1})
        attachments_count = Attachment.objects.all().count()
        self.assertEqual(attachments_count, 2)
        url = reverse('delete-bundle-attachments', kwargs={'bundle_id': 'test'})
        response = client.post(url)
        self.assertEqual(response.content, '[[true], [true]]\r\n')
        attachments_count = Attachment.objects.all().count()
        self.assertEqual(attachments_count, 0)

    def testRepeatAttachment(self):
        client = self.client
        filepath = self.filepath
        attachment = open(filepath)
        url = reverse('bundle-attachments', kwargs={'bundle_id': 'test'})
        client.post(url, {'attachment': attachment})
        attachment.close()
        attachment = Attachment.objects.get(bundle='test', filename='test.png')
        created = attachment.created
        attachment = open(filepath)
        client.post(url, {'attachment': attachment})
        attachment.close()
        attachment = Attachment.objects.get(bundle='test', filename='test.png')
        recreated = attachment.created
        self.assertNotEqual(created, recreated)
        delete_and_clean(attachment)

    def tearDown(self):
        os.unlink(self.filepath)
        os.unlink(self.filepath1)
        os.rmdir('./media/session_attachments')
