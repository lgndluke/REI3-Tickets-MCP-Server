import src.rei3.tickets.api.requests as tickets_api

from fastmcp import FastMCP

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
        self.FastMCP   = FastMCP(name="REI3 Tickets MCP Server")

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
        async def get_public_worklogs_by_ticket_key(key: str) -> str:
            """
            Fetch all public worklogs of a specific ticket by its key value.

            Args:
                key:  The ticket key. (e.g.: '15')

            :returns:
                A success message including X or an error message.
            """
            return await tickets_api.get_public_worklogs_by_ticket_key(key=key)

        @self.FastMCP.tool()
        async def get_ticket_info_by_key(key: str) -> str:
            """
            Fetch ticket information of a specific ticket by its key value.

            Args:
                key:  The ticket key. (e.g.: '15')

            :returns:
                A success message including X or an error message.
            """
            return await tickets_api.get_ticket_info_by_key(key=key)

    def get_fastmcp(self) -> FastMCP:
        return self.FastMCP