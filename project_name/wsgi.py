import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      '{{ project_name }}.settings.production')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
