import django
import os
import secrets
import subprocess

from django.contrib.auth import get_user_model
from pathlib import Path

# Configure Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.web_server.main.settings")
django.setup()

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
        user.set_password('admin')
        user.save()

        # Create static files.
        subprocess.check_call('python manage.py collectstatic --noinput', shell=True)

        # Create setup file.
        setup_file.touch()
