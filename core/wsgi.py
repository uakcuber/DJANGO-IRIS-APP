"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

# Bind the application to a specific host and port
host = '0.0.0.0'
port = '8000'
bind = f'{host}:{port}'

# Start the server
if __name__ == '__main__':
    from waitress import serve
    serve(application, host=host, port=port)
