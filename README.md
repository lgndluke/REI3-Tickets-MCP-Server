
<h1 align="center">
  <br>
  <a href="https://github.com/lgndluke/REI3-Tickets-MCP-Server"><img width="200" alt="REI3_MCP_Server_Logo" src="https://github.com/user-attachments/assets/dfac4e23-ddeb-4fdd-a1fe-8af413fb2c60" /></a>
  <br>
  REI3 Tickets MCP Server
  <br>
</h1>

<h4 align="center">A simple FastMCP server for the REI3 Tickets application.</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#credits">Credits</a>
</p>

## Key Features

* Create tickets.
* Create ticket worklog entries.

## Installation

#### Installation instructions

1. Install [Python 3.13.5](https://www.python.org/downloads/release/python-3135/).

2. Install [uv](https://docs.astral.sh/uv/) Python package manager. 

3. Add uv to PATH.

4. Set up an API Profile in your REI3 tickets instance. <br> You can create one under: Tickets > Admin Tab > API profiles 

5. Download/Clone and extract this repository and adjust the .env file variables.

6. Ensure you have an MCP Client with the capability to run MCP tools at your disposal. <br> I used [AnythingLLM](https://anythingllm.com/)

7. Configure the MCP-Server JSON configuration to include the REI3-Tickets-MCP-Server.

#### MCP-Server JSON configuration

```json
{
  "mcpServers": {
	"REI3-Tickets-MCP-Server" : {
		"command": "uv",
		"args": [
			"--directory",
			"ABSOLUTE\\PATH\\TO\\PARENT\\FOLDER\\REI3-Tickets-MCP-Server-main",
			"run",
			"rei3_tickets_mcp_server.py"
		]
	}
  }
}
```

## Credits

This software utilizes:

- [REI3](https://github.com/r3-team/r3)
