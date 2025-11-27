import asyncio

from src.common.config_handler import get_config_value
from src.rei3.tickets.mcp.server import REI3TicketsMCPServer
from uvicorn.main import Config, Server

async def main():

    host = get_config_value('general', 'host', fallback='localhost')
    port = int(get_config_value('general', 'port', fallback=54321))

    ssl_crt_file = get_config_value('general', 'ssl_crt_file', fallback=None)
    ssl_key_file = get_config_value('general', 'ssl_key_file', fallback=None)

    rei3_tickets_mcp = REI3TicketsMCPServer()

    config = Config(
        rei3_tickets_mcp.get_fastmcp().http_app(),
        host         = host,
        port         = port,
        ssl_certfile = ssl_crt_file,
        ssl_keyfile  = ssl_key_file,
        loop         = 'asyncio',
        ws           = "websockets-sansio",
        use_colors   = True
    )

    server = Server(config=config).serve()
    await asyncio.gather(server)

if __name__ == "__main__":
    asyncio.run(main())
