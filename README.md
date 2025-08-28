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
  <a href="#roadmap">Roadmap</a> •
  <a href="#installation">Installation</a> •
  <a href="#demonstration">Demonstration</a> •
  <a href="#credits">Credits</a>
</p>

## Key Features

* Create tickets.
* Create ticket worklog entries.

## Roadmap

- Close ticket by ticket key functionality.
- Get context by ticket key functionality.
- Get ticket info by ticket key functionality.
- Management Web-Interface.
- Docker Container for simpler deployment.

## Installation

#### Installation instructions

1. Install [Python 3.13.5](https://www.python.org/downloads/release/python-3135/).

2. Install [uv](https://docs.astral.sh/uv/) Python package manager. 

3. Add uv to PATH.

4. Create a designated user in REI3 with access to the Tickets API role. <br> This user will be used for authentication.

5. Set up an API Profile in your REI3 tickets instance. <br> You can create one under: Tickets > Admin Tab > API profiles 

6. Download/Clone and extract this repository and adjust the config.ini file variables.

7. Ensure you have an MCP Client with the capability to run MCP tools at your disposal. <br> I used [AnythingLLM](https://anythingllm.com/)

8. Configure the MCP-Server JSON configuration to include the REI3-Tickets-MCP-Server.

#### MCP-Server JSON configuration examples for AnythingLLM:

For transport mode 'stdio':

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

For transport mode 'http':

```json
{
  "mcpServers": {
	"REI3-Tickets-MCP-Server" : {
		"url": "http://127.0.0.1:54321/mcp",
		"type": "streamable"
	}
  }
}
```

## Demonstration

#### Creating a REI3 ticket using the REI3-Tickets-MCP-Server:

<img width="1309" height="248" alt="Create_Ticket_with_MCP_Server" src="https://github.com/user-attachments/assets/2dc69e13-e742-4376-8b29-821fa1ae298a" />

#### Created ticket:

<img width="1918" height="947" alt="Created_Ticket_in_Not_Assigned" src="https://github.com/user-attachments/assets/19a4cd47-067a-48c3-8617-ce14919f78e9" />

#### Created ticket worklog:

<img width="1876" height="806" alt="Created_Ticket_Worklog" src="https://github.com/user-attachments/assets/7f9baeab-8c46-44ad-8dce-0873d11ff3c2" />

#### Creating a worklog entry inside an existing ticket:

<img width="1320" height="398" alt="Create_Ticket_Worklog_with_MCP_Server" src="https://github.com/user-attachments/assets/abec409e-ff49-4867-8404-0f41ee669065" />

#### Created ticket worklog:

<img width="1877" height="810" alt="Create_Second_Ticket_Worklog" src="https://github.com/user-attachments/assets/dd4f9b10-7c16-47b6-9318-7e50bd14adeb" />

####

## Credits

This software utilizes:

- [REI3](https://github.com/r3-team/r3)

