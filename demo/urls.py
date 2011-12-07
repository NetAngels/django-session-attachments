from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        (r'^%s(?P<path>.*)$' % settings.ADMIN_MEDIA_PREFIX[1:], 'django.views.static.serve',
            {'document_root': settings.ADMIN_MEDIA_ROOT}),
    )
    urlpatterns += patterns('',
                            url(r'^', include('session_attachments.urls')),
                            )
else:
    urlpatterns = patterns('',
                            url(r'^', include('session_attachments.urls')),
                            )
