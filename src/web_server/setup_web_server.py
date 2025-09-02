import os
import secrets
import subprocess

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from pathlib import Path

@sync_to_async
def check_if_user_exists():
    return get_user_model().objects.exists()

async def setup_web_server() -> None:
    """
    Function to set up the initial web-server configuration.
    """

    if not await check_if_user_exists():

        # Create .env file with DJANGO_SECRET inside 'web_server/main'.
        main_path = Path(__file__).resolve() / 'main'
        os.chdir(main_path)

        django_secret = secrets.token_urlsafe(64)

        with open('.env', 'r') as env:
            env.write(f"DJANGO_SECRET='{django_secret}'")

        # Change to root project directory.
        root_path = Path(__file__).resolve().parents[2]
        os.chdir(root_path)

        # Make mcp_app migrations.
        subprocess.check_call('python manage.py makemigrations', shell=True)

        # Migrate everything.
        subprocess.check_call('python manage.py migrate', shell=True)

        # Create django-admin user.
        subprocess.check_call('python manage.py createsuperuser --noinput --username admin --email admin@tickets.local', shell=True)

        # Set django-admin user password.
        user = get_user_model().objects.get(username='admin')
        user.setpassword('admin')
        user.save()

        # Create static files.
        subprocess.check_call('python manage.py collectstatic --noinput', shell=True)
