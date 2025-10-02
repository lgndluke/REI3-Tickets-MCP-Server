import datetime
import django
import json
import os
import secrets

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.core import management
from pathlib import Path
from src.common.config_handler import get_config_value

@sync_to_async
def _django_make_migrations():
    management.call_command('makemigrations')

@sync_to_async
def _django_migrate():
    management.call_command('migrate')

@sync_to_async
def _django_load_data():
    management.call_command('loaddata', 'initial_mcp_server_config.json')

@sync_to_async
def _django_create_super_user():
    management.call_command('createsuperuser', username='admin', email='admin@tickets.local', interactive=False)

@sync_to_async
def _set_default_admin_password():
    user = get_user_model().objects.get(username='admin')
    user.set_password('admin')
    user.save()

@sync_to_async
def _django_collect_static():
    management.call_command('collectstatic', interactive=False)

async def setup_web_server() -> None:
    """
    Function to set up the initial web-server configuration.
    """

    setup_file = Path(__file__).resolve().parent / ".initialized"
    if not setup_file.exists():

        # Create .env file with DJANGO_SECRET inside 'web_server/main'.
        main_path = Path(__file__).resolve().parent / 'main'
        os.chdir(main_path)

        django_secret = secrets.token_urlsafe(64)

        with open('.env', 'w') as env:
            env.write(f"DJANGO_SECRET='{django_secret}'")

        # Create initial MCP server configuration fixture json.
        mcp_app_path = Path(__file__).resolve().parent / 'mcp_app'
        os.chdir(mcp_app_path)

        json_data = {
            'model': 'mcp_app.TicketsMCPServerConfig',
            'pk': 1,
            'fields': {
                'host': get_config_value('general', 'host'),
                'port': int(get_config_value('general', 'port')),
                'transport': get_config_value('mcp-server', 'transport'),
                'enable': True if get_config_value('web-server', 'enable').lower() == 'true' else False,
                'allowed_hosts': get_config_value('web-server', 'allowed_hosts'),
                'secure_ssl_redirect': True if get_config_value('web-server', 'secure_ssl_redirect').lower() == 'true' else False,
                'secure_hsts_seconds': int(get_config_value('web-server', 'secure_hsts_seconds')),
                'secure_hsts_include_subdomains': True if get_config_value('web-server','secure_hsts_include_subdomains').lower() == 'true' else False,
                'secure_hsts_preload': True if get_config_value('web-server', 'secure_hsts_preload').lower() == 'true' else False,
                'session_cookie_secure': True if get_config_value('web-server', 'session_cookie_secure').lower() == 'true' else False,
                'csrf_cookie_secure': True if get_config_value('web-server', 'csrf_cookie_secure').lower() == 'true' else False,
                'username': get_config_value('rei3-tickets-api', 'username'),
                'password': get_config_value('rei3-tickets-api', 'password'),
                'email': get_config_value('rei3-tickets-api', 'email'),
                'profile': int(get_config_value('rei3-tickets-api', 'profile')),
                'key_format': get_config_value('rei3-tickets-api', 'key_format'),
                'base_url': get_config_value('rei3-tickets-api', 'base_url'),
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat(),
            }
        }

        # Ensure fixtures directory exists.
        fixtures_path = mcp_app_path / 'fixtures'
        fixtures_path.mkdir(parents=True, exist_ok=True)

        json_file_path = fixtures_path / 'initial_mcp_server_config.json'

        with open(json_file_path, 'w') as json_file:
            json.dump([json_data], json_file)

        # Configure Django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.web_server.main.settings")
        django.setup()

        # Change to root project directory.
        root_path = Path(__file__).resolve().parents[2]
        os.chdir(root_path)

        # Make mcp_app migrations.
        await _django_make_migrations()

        # Migrate everything.
        await _django_migrate()

        # Load MCP server fixture as initial data.
        await _django_load_data()

        # Create django-admin user.
        await _django_create_super_user()

        # Set django-admin password.
        await _set_default_admin_password()

        # Create static files.
        await _django_collect_static()

        # Create setup file.
        setup_file.touch()
