from src.rei3.tickets.mcp.server import *

# ----------------------------
# Tests
# ----------------------------

def test_REI3TicketsMCPServer___init__():

    tickets_mcp = REI3TicketsMCPServer()

    assert tickets_mcp is not None

def test_REI3TicketsMCPSServer_get_fastmcp():

    tickets_mcp = REI3TicketsMCPServer()

    assert tickets_mcp.get_fastmcp() is not None
