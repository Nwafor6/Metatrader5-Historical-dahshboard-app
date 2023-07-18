import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

try:
    application = get_wsgi_application()
except:
    app = get_wsgi_application()
