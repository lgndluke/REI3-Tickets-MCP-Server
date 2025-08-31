from django.core.exceptions import ValidationError
from django.db import models

class TicketsMCPServerConfig(models.Model):

    # [general] section.
    host = models.GenericIPAddressField(
        default='127.0.0.1',
    )

    port = models.PositiveIntegerField(
        default=54321
    )

    # [mcp-server] section.
    TRANSPORT_CHOICES = (
        ('http', 'http'),
        ('stdio', 'stdio'),
    )

    transport = models.CharField(
        max_length=10,
        choices=TRANSPORT_CHOICES,
        default='http',
    )

    # [web-server] section.
    enable = models.BooleanField(
        default=True,
    )

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
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Get the configuration instance, or create a default one.
        """
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'host': '127.0.0.1',
                'port': 54321,
                'transport': 'http',
                'enable': True,
                'username': 'admin',
                'password': 'admin',
                'email': 'tickets-mcp-server@mcp.local',
                'profile': 1,
                'key_format': '{key:06d}',
                'base_url': 'http://localhost:21918',
            }
        )
        return obj

    def __str__(self):
        return f'REI3 Tickets MCP Server Configuration ({self.host}:{self.port}, transport={self.transport})'
