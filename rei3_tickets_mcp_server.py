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

    tickets_mcp   = REI3TicketsMCPServer()

    # [general] values.
    host          = get_config_value('general', 'host', fallback='localhost')
    port          = int(get_config_value('general', 'port', fallback=54321))

    # [mcp-server] values.
    mcp_transport = get_config_value('mcp-server', 'transport', fallback='http')

    # [web-server] values.
    web_enable    = get_config_value('web-server', 'enable', fallback='true')

    tasks = []

    if mcp_transport == 'stdio' and web_enable.lower() == 'false':
        tasks.append(asyncio.create_task(_run_mcp_server(tickets_mcp, 'stdio')))

    if mcp_transport == 'http' and web_enable.lower() == 'false':
        settings.host = host
        settings.port = port
        tasks.append(asyncio.create_task(_run_mcp_server(tickets_mcp, 'streamable-http')))

    if mcp_transport == 'stdio' and web_enable.lower() == 'true':
        print('The web-server does not support "stdio" transport. Please either change transport or disable the web-server.')

    if mcp_transport == 'http' and web_enable.lower() == 'true':
        await setup_web_server()
        config = Config('src.web_server.main.asgi:application', host=host, port=port, loop='asyncio')
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

    await stop_event.wait()

    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

# ----------------------------
# Entry Point
# ----------------------------

if __name__ == "__main__":
    asyncio.run(main())
