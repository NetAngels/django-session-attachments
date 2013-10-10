from django.conf import settings

DEFAULT_SIZE = 50 # mb

MAX_ATTACHMENT_SIZE = getattr(settings, "MAX_ATTACHMENT_SIZE", None)
if not MAX_ATTACHMENT_SIZE:
	MAX_ATTACHMENT_SIZE = DEFAULT_SIZE