import datetime
import django
import json
import os
import secrets
import subprocess

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from pathlib import Path
from src.common.config_handler import get_config_value

@sync_to_async
def _set_default_admin_password():
    # Set django-admin user password.
    user = get_user_model().objects.get(username='admin')
    user.set_password('admin')
    user.save()

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
        subprocess.check_call('python manage.py makemigrations', shell=True)

        # Migrate everything.
        subprocess.check_call('python manage.py migrate', shell=True)

        # Load MCP server fixture as initial data.
        subprocess.check_call('python manage.py loaddata initial_mcp_server_config.json', shell=True)

        # Create django-admin user.
        subprocess.check_call('python manage.py createsuperuser --noinput --username admin --email admin@tickets.local', shell=True)

        # Set django-admin password.
        await _set_default_admin_password()

        # Create static files.
        subprocess.check_call('python manage.py collectstatic --noinput', shell=True)

        # Create setup file.
        setup_file.touch()
