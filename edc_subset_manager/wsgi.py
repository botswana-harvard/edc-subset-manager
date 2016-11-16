"""
WSGI config for edc_subset_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edc_subset_manager.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
