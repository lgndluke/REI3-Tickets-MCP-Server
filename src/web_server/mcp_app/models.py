from django.core.exceptions import ValidationError
from django.db import models
from src.common.config_handler import get_config_value, set_config_value, save_config, reload_config

class TicketsMCPServerConfig(models.Model):

    # [general] section.
    host = models.TextField()
    port = models.PositiveIntegerField()

    # [mcp-server] section.
    transport = models.TextField()

    # [web-server] section.
    enable = models.BooleanField()
    allowed_hosts = models.TextField()
    secure_ssl_redirect = models.BooleanField()
    secure_hsts_seconds = models.PositiveIntegerField()
    secure_hsts_include_subdomains = models.BooleanField()
    secure_hsts_preload = models.BooleanField()
    session_cookie_secure = models.BooleanField()
    csrf_cookie_secure = models.BooleanField()

    # [rei3-tickets-api] section.
    username = models.CharField(
        max_length=128,
    )

    password = models.CharField(
        max_length=128,
    )

    email = models.EmailField(
        max_length=128,
    )

    profile = models.PositiveIntegerField()

    key_format = models.CharField(
        max_length=128,
    )

    base_url = models.URLField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'REI3 Tickets MCP Server Configuration'
        verbose_name_plural = 'REI3 Tickets MCP Server Configurations'

    def save(self, *args, **kwargs):
        """
        Ensure only one instance of this class exists in the database.
        """
        if not self.pk and TicketsMCPServerConfig.objects.exists():
            raise ValidationError('Only one Tickets MCP Server Configuration is allowed.')

        # Persist changes to database first.
        super().save(*args, **kwargs)

        # Sync changes to config.ini file.
        set_config_value('rei3-tickets-api', 'username', str(self.username))
        set_config_value('rei3-tickets-api', 'password', str(self.password))
        set_config_value('rei3-tickets-api', 'email', str(self.email))
        set_config_value('rei3-tickets-api', 'profile', str(self.profile))
        set_config_value('rei3-tickets-api', 'key_format', str(self.key_format))
        set_config_value('rei3-tickets-api', 'base_url', str(self.base_url))
        save_config()

    @classmethod
    def load(cls):
        """
        Always sync the configuration from config.ini to the database.
        - If no DB entry exists -> create it from config.ini.
        - If DB entry exists but differs -> update DB values with config.ini.
        - Always return the up-to-date DB entry.
        """

        reload_config()

        # Read config.ini file values.
        config_values = {
            'host': get_config_value('general', 'host'),
            'port': int(get_config_value('general', 'port')),
            'transport': get_config_value('mcp-server', 'transport'),
            'enable': True if get_config_value('web-server', 'enable').lower() == 'true' else False,
            'allowed_hosts': get_config_value('web-server', 'allowed_hosts'),
            'secure_ssl_redirect': True if get_config_value('web-server', 'secure_ssl_redirect').lower() == 'true' else False,
            'secure_hsts_seconds': int(get_config_value('web-server', 'secure_hsts_seconds')),
            'secure_hsts_include_subdomains': True if get_config_value('web-server', 'secure_hsts_include_subdomains').lower() == 'true' else False,
            'secure_hsts_preload': True if get_config_value('web-server', 'secure_hsts_preload').lower() == 'true' else False,
            'session_cookie_secure': True if get_config_value('web-server', 'session_cookie_secure').lower() == 'true' else False,
            'csrf_cookie_secure': True if get_config_value('web-server', 'csrf_cookie_secure').lower() == 'true' else False,
            'username': get_config_value('rei3-tickets-api', 'username'),
            'password': get_config_value('rei3-tickets-api', 'password'),
            'email': get_config_value('rei3-tickets-api', 'email'),
            'profile': int(get_config_value('rei3-tickets-api', 'profile')),
            'key_format': get_config_value('rei3-tickets-api', 'key_format'),
            'base_url': get_config_value('rei3-tickets-api', 'base_url'),
        }

        # Fetch singleton instance.
        obj, created = cls.objects.get_or_create(pk=1, defaults=config_values)

        if not created:
            # Compare DB with config.ini and update if different.
            updated = False
            for field, value in config_values.items():
                if getattr(obj, field) != value:
                    setattr(obj, field, value)
                    updated = True
            if updated:
                obj.save_base(update_fields=config_values.keys())

        return obj

    def __str__(self):
        return f'REI3 Tickets MCP Server Configuration ({self.host}:{self.port}, transport={self.transport})'
