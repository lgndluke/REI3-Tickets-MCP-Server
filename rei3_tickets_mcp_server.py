import asyncio
import signal
import threading

from fastmcp import settings
from src.common.config_handler import get_config_value
from src.rei3.tickets.mcp.server import REI3TicketsMCPServer
from src.web_server.setup_web_server import setup_web_server
from uvicorn.main import Config, Server

# ----------------------------
# Private functions
# ----------------------------

async def _run_mcp_server(server: REI3TicketsMCPServer, transport: str):
    """
    Private helper function for starting up the REI3 tickets MCP server.

    :param server: The REI3 tickets MCP server instance to start.
    :param transport: The transport mode of the MCP server.
    """

    stop = threading.Event()

    def runner():
        server.get_fastmcp().run(transport=transport)

    thread = threading.Thread(target=runner, daemon=True)
    thread.start()

    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        stop.set()
        raise

# ----------------------------
# Main Function
# ----------------------------

async def main():

    tickets_mcp   = None

    # [general] values.
    host          = get_config_value('general', 'host', fallback='localhost')
    port          = int(get_config_value('general', 'port', fallback=54321))

    # [mcp-server] values.
    mcp_transport = get_config_value('mcp-server', 'transport', fallback='http')

    # [web-server] values.
    web_enable    = get_config_value('web-server', 'enable', fallback='true')
    ssl_key_file  = get_config_value('web-server', 'ssl_key_file', fallback=None)
    ssl_cert_file = get_config_value('web-server', 'ssl_cert_file', fallback=None)

    tasks = []

    if mcp_transport == 'stdio' and web_enable.lower() == 'false':
        tickets_mcp = REI3TicketsMCPServer()
        tasks.append(asyncio.create_task(_run_mcp_server(tickets_mcp, 'stdio')))

    if mcp_transport == 'http' and web_enable.lower() == 'false':
        settings.host = host
        settings.port = port
        tickets_mcp = REI3TicketsMCPServer()
        tasks.append(asyncio.create_task(_run_mcp_server(tickets_mcp, 'streamable-http')))

    if mcp_transport == 'stdio' and web_enable.lower() == 'true':
        print('The web-server does not support "stdio" transport. Please either change transport or disable the web-server.')

    if mcp_transport == 'http' and web_enable.lower() == 'true':
        await setup_web_server()
        config = Config('src.web_server.main.asgi:application', host=host, port=port, ssl_certfile=ssl_cert_file, ssl_keyfile=ssl_key_file, loop='asyncio')
        server = Server(config)
        tasks.append(asyncio.create_task(server.serve()))

    if not tasks:
        print("No server configured to run.")
        return

    # Graceful showdown
    loop       = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def shutdown_event():
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, shutdown_event)
        except NotImplementedError:
            # Windows does not support SIGTERM
            pass

    try:
        await stop_event.wait()
    except asyncio.CancelledError:
        print('REI3 Tickets MCP server has been shutdown.')

    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

# ----------------------------
# Entry Point
# ----------------------------

if __name__ == "__main__":
    asyncio.run(main())
