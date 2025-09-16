from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse

from .models import TicketsMCPServerConfig

@admin.register(TicketsMCPServerConfig)
class TicketsMCPServerConfigAdmin(admin.ModelAdmin):

    readonly_fields = ['host', 'port', 'transport', 'enable', 'allowed_hosts', 'secure_ssl_redirect', 'secure_hsts_seconds', 'secure_hsts_preload', 'session_cookie_secure', 'csrf_cookie_secure']

    fieldsets = (
        ('General', {
            'fields': ('host', 'port'),
        }),
        ('MCP Server', {
            'fields': ('transport',),
        }),
        ('Web Server', {
            'fields': ('enable', 'allowed_hosts', 'secure_ssl_redirect', 'secure_hsts_seconds', 'secure_hsts_preload', 'session_cookie_secure', 'csrf_cookie_secure',),
        }),
        ('REI3 Tickets API', {
            'fields': ('username', 'password', 'email', 'profile', 'key_format', 'base_url'),
        }),
    )

    def has_add_permission(self, request):
        """
        Prevent adding more than one config via the admin interface.
        """
        return not TicketsMCPServerConfig.objects.exists()

    def changelist_view(self, request, extra_context=None):
        """
        Redirect directly to the singleton instance of TicketsMCPServerConfig if it exists.
        """
        config = TicketsMCPServerConfig.load()
        return HttpResponseRedirect(
            reverse('admin:mcp_app_ticketsmcpserverconfig_change', args=[config.pk])
        )

    def get_urls(self):
        """
        Make sure the singleton redirect works properly.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "",
                self.changelist_view,
                name="mcp_app_ticketsmcpserverconfig_change"
            )
        ]
        return custom_urls + urls

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        """
        Customize the change form page to look more like 'Settings'.
        """
        extra_context = extra_context or {}
        extra_context['title'] = "Edit MCP Server Configuration"
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields
