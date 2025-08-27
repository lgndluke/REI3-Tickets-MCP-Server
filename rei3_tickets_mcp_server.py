import configparser

from src.rei3_tickets_mcp_server import REI3TicketsMCPServer

# ----------------------------
# Load configuration file
# ----------------------------

config = configparser.ConfigParser()
config.read('config.ini')

# ----------------------------
# Entry Point
# ----------------------------

if __name__ == "__main__":

    transport = config.get('server', 'transport')
    tickets_mcp = REI3TicketsMCPServer()

    if transport == 'stdio':
        tickets_mcp.get_fastmcp().run(
            transport='stdio'
        )

    if transport == 'http':
        tickets_mcp.get_fastmcp().settings.host = config.get('server', 'host', fallback='localhost')
        tickets_mcp.get_fastmcp().settings.port = config.getint('server', 'port', fallback=3000)

        tickets_mcp.get_fastmcp().run(
            transport='streamable-http'
        )
