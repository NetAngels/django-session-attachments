# -*- coding: utf-8 -*-
import datetime
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from session_attachments.models import Attachment
from session_attachments.utils import delete_and_clean


class Command(BaseCommand):
    args = '--older-than=N'
    help = 'Remove attachments older than N days'
    option_list = BaseCommand.option_list + (make_option('--older-than',
                                                         dest='date_threshold',
                                                         type='int',
                                                         ),
                                             make_option('--verbose',
                                                         dest='verbose',
                                                         action='store_true',
                                                         default=False,
                                                         help='verbose mode'
                                                         ))

    def handle(self, **options):
        now = datetime.datetime.now()
        date_threshold = options.get('date_threshold')
        if date_threshold is None:
            raise CommandError('--older-than=DAYS option is required')
        delta = datetime.timedelta(days=date_threshold)
        threshold_time = now - delta
        verbose = options.get('verbose')
        attachment_list = Attachment.objects.filter(created__lt=threshold_time)
        for attach in attachment_list:
            if verbose:
                print(u'delete %s' % attach.filename)
            delete_and_clean(attach)
