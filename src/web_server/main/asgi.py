"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from fastapi import FastAPI
from fastmcp import settings
from src.rei3.tickets.mcp.server import REI3TicketsMCPServer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.web_server.main.settings')

# Set FastMCP settings to expose server endpoint at '/'. Default would be '/mcp'.
settings.streamable_http_path = '/'

# Get ASGI applications.
django_asgi_application = ASGIStaticFilesHandler(get_asgi_application())
tickets_mcp_endpoint    = REI3TicketsMCPServer().get_fastmcp().http_app()

# Mount ASGI applications to root FastAPI application.
root = FastAPI(lifespan=tickets_mcp_endpoint.lifespan)
root.mount('/mcp', tickets_mcp_endpoint)
root.mount('/', django_asgi_application)

# Set application to root FastAPI application.
application = root
