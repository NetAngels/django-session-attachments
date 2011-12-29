Django session attachments
=============================

This app aims to work with attachments in Django.

Basically working with attachments is the same as working with ordinary
uploads, except for a few distinctions:

- Attachments "belong" to clients they have uploaded. In other words,
  attachments must be private and inaccessible to public.
- Attachments are organized to "bundles". It makes sense if your client decides
  to work with different attachment sets in different parts of your application
  (for example, he/she writes several emails or requests simultaniously and
  obviously doesn't want to share his/her attachments between recipients.)
- Attachments are temporary. There must be easy methods to remove attachments
  manually or by expiration.
- Attachments must be usable even for unauthenticated users. It is due to our
  specifics. This is also the main reason why we created this app.
- It is impossible to store two attachments with the same name in the same
  bundle. New attachment overwrite previous one. It looks like sane
  restriction given application usecase.


Installation and configuration
----------------------------------

Install application from PyPI or GitHub::

    $ pip install django-session-attachments  # or
    $ pip install git://github.com/NetAngels/django-session-attachments.git#egg=django-session-attachments


Add a new application to your settings file::

    INSTALLED_APPS = [
        'django.contrib.staticfiles',
        ...
        'session_attachments',
        ...
    ]

Include a new line to your urlconf (urls.py)::

    urlpatterns = patterns('',
        ...
        url(r'^attachments/', include('session_attachments.urls')),
        ...
    )



There is a separate Django model to save attachments, so you should type::

    ./manage.py syncdb session_attachments



How to use it
----------------

Providing that your app is available at localhost:8000, you get following
number of URLs to work with from your frontend. It would probably be easier to
work with the backend asynchronously, using JQuery forms extension or something
similar.

Samples below use curl for the sake of simplicity. Because attachments are tied
with session, it is important to keep session cookies between curl invocations.
We do it by passing ``--cookie session.txt --cookie-jar session.txt`` options to
curl.

Please note that curl examples don't work unless the CSRF middleware is
disabled in settings.


Upload files to the the bundle
````````````````````````````````


To upload files POST data to ``/attachments/<bundle_id>/`` URL. The form must
contain at least one file field. The name of file fields can be arbitrary as they
are ignored by the app::

    $ echo spam > spam.txt
    $ echo egg > egg.txt
    $ curl --cookie session.txt --cookie-jar session.txt -F attach1=@spam.txt -F attach2=@egg.txt -X POST http://localhost:8000/attachments/foo/
    [{"name": "egg.txt", ...}, {"name": "spam.txt", ...}]


Get the list of attachments in the bundle
`````````````````````````````````````````````
::

    $ curl --cookie session.txt --cookie-jar session.txt -X GET http://localhost:8000/attachments/foo/
    $ [{"mimetype": "text/plain", "size": 4, "name": "egg.txt", "created": "2011-12-29 04:12"}, {"mimetype": "text/plain", "size": 5, "name": "spam.txt", "created": "2011-12-29 04:12"}]

The list of dicts in JSON format is returned.

Download the file from the bundle
``````````````````````````````````````

::

    $ curl --cookie session.txt --cookie-jar session.txt -X GET http://localhost:8000/attachments/foo/spam.txt/
    spam


Delete the attachment from the bundle
``````````````````````````````````````

::

    $ curl --cookie session.txt --cookie-jar session.txt -X POST http://localhost:8000/attachments/foo/spam.txt/delete/
    [true]


Clean up the whole bundle
``````````````````````````````````````

::

    $ curl --cookie session.txt --cookie-jar session.txt -X POST http://localhost:8000/attachments/foo/delete/
    [[true]]


Management command to cleanup outdated attachments
````````````````````````````````````````````````````

There is a management command which removes "outdated" attachments from the
bundle. To set up the threshold to remove You can pass the number of days::

    ./manage.py remove_outdated_attachments --older-than=3
