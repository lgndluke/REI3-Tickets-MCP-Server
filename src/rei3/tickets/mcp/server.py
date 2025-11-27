import src.rei3.tickets.api.requests as tickets_api

from cryptography.fernet import Fernet
from fastmcp import FastMCP
from fastmcp.server.auth import OIDCProxy
from key_value.aio.stores.disk import DiskStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from src.common.config_handler import get_config_value

# ----------------------------
# Class definition
# ----------------------------

class REI3TicketsMCPServer:
    """
    The main REI3 Tickets MCP Server class.
    """

    # ----------------------------
    # Initialize MCP Server
    # ----------------------------
    def __init__(self):
        self.OIDCProxy = None

        if get_config_value('oidc_proxy', 'enable_oidc_proxy').lower() == 'true':

            config_url = get_config_value('oidc_proxy', 'config_url')
            if not config_url:
                raise ValueError('Error: OIDC Proxy enabled in config, but no "config_url" value was provided.')

            client_id = get_config_value('oidc_proxy', 'client_id')
            if not client_id:
                raise ValueError('Error: OIDC Proxy enabled in config, but no "client_id" value was provided.')

            client_secret = get_config_value('oidc_proxy', 'client_secret')
            if not client_secret:
                raise ValueError('Error: OIDC Proxy enabled in config, but no "client_secret" value was provided.')

            base_url = get_config_value('oidc_proxy', 'base_url')
            if not base_url:
                raise ValueError('Error: OIDC Proxy enabled in config, but no "base_url" value was provided.')

            jwt_signing_key = get_config_value('oidc_proxy', 'jwt_signing_key')
            if not jwt_signing_key:
                raise ValueError('Error: OIDC Proxy enabled in config, but no "jwt_signing_key" value was provided.')

            disk_store_directory = get_config_value('oidc_proxy', 'disk_store_directory')
            if not disk_store_directory:
                raise ValueError('Error: OIDC Proxy enabled in config, but no "disk_store_directory" value was provided.')
            disk_store = DiskStore(directory=disk_store_directory)

            storage_encryption_key = get_config_value('oidc_proxy', 'storage_encryption_key')
            if not storage_encryption_key:
                raise ValueError('Error: OIDC Proxy enabled in config, but no "storage_encryption_key" value was provided.')

            self.OIDCProxy = OIDCProxy(
                config_url      = config_url,
                client_id       = client_id,
                client_secret   = client_secret,
                base_url        = base_url,
                jwt_signing_key = None,
                client_storage  = FernetEncryptionWrapper(
                    key_value = disk_store,
                    fernet    = Fernet(key=storage_encryption_key)
                )
            )

        self.FastMCP   = FastMCP(
            name="REI3 Tickets MCP Server",
            auth=self.OIDCProxy if not self.OIDCProxy is None else None
        )

        # ----------------------------
        # Register MCP Server tools.
        # ----------------------------
        @self.FastMCP.tool()
        async def close_ticket_by_key(key: str, closing_text: str) -> str:
            """
            Close a ticket specified by its ticket key inside the REI3 Tickets application.

            Args:
                key: The ticket key. (e.g.: '000015' or '15')
                closing_text: The closing text of the ticket.

            :returns:
                A success message including the closed ticket ID or an error message.
            """
            return await tickets_api.close_ticket_by_key(key=key, closing_text=closing_text)

        @self.FastMCP.tool()
        async def create_ticket(subject: str, description: str) -> str:
            """
            Create a ticket inside the REI3 Tickets application.

            Args:
                subject: The subject of the ticket.
                description: The description of the ticket.

            :returns:
                A success message including the created ticket ID or an error message.
            """
            return await tickets_api.create_ticket(subject=subject, description=description)

        @self.FastMCP.tool()
        async def create_worklog(note: str, key: str) -> str:
            """
            Create a worklog entry for a specific ticket inside the REI3 Tickets application.

            Args:
                note: The content or note to include in the worklog.
                key:  The ticket key. (e.g.: '15')

            :returns:
                A success message including the created worklog ID or an error message.
            """
            return await tickets_api.create_worklog(note=note, key=key)

        @self.FastMCP.tool()
        async def get_worklogs_by_key(key: str) -> str:
            """
            Fetch all public worklogs of a ticket specific by its key value.

            Args:
                key: The ticket key. (e.g.: '000015' or '15')

            :returns:
                The fetched public worklog entries or an error message.
            """
            return await tickets_api.get_worklogs_by_key(key=key)

        @self.FastMCP.tool()
        async def get_ticket_by_key(key: str) -> str:
            """
            Fetches ticket information of a ticket specified by its key value.

            Args:
                key:  The ticket key. (e.g.: '000015' or '15')

            :returns:
                The fetched ticket information or an error message.
            """
            return await tickets_api.get_ticket_by_key(key=key)

    def get_fastmcp(self) -> FastMCP:
        return self.FastMCP