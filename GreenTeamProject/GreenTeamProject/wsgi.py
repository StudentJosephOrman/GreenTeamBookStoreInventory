"""
WSGI config for GreenTeamProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

# This python script is a built-in DJango script, but allows the app to view

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GreenTeamProject.settings')

application = get_wsgi_application()
