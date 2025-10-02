<h1 align="center">
  <br>
  <a href="https://github.com/lgndluke/REI3-Tickets-MCP-Server"><img width="128" alt="REI3_MCP_Server_Logo" src="https://github.com/user-attachments/assets/0b7f6c94-6ed3-4716-8fa0-f4d99437a851" /></a>
  <br>
  REI3 Tickets MCP Server
  <br>
</h1>

<h4 align="center">A simple FastMCP server for the REI3 Tickets application.</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#demonstration">Demonstration</a> •
  <a href="#credits">Credits</a> •
  <a href="#donate">Donate</a>
</p>

## Key Features

* Create tickets.
* Create ticket worklog entries.
* Close ticket by ticket key functionality.
* Get context by ticket key functionality.
* Get ticket info by ticket key functionality.

## Installation

#### Installation instructions (release)

1. Install [Python 3.13.5](https://www.python.org/downloads/release/python-3135/).

2. Create a designated user in REI3 with access to the Tickets API role. <br> This user will be used for authentication.

3. Set up an API Profile in your REI3 tickets instance. <br> You can create one under: Tickets > Admin Tab > API profiles 

4. Download the [latest release](https://github.com/lgndluke/REI3-Tickets-MCP-Server/releases/latest).

5. Set-ExecutionPolicy Bypass -> if you plan on using the shortcut 'open_config.ps1' script.

6. Adjust config.ini file variables.

7. Start the 'REI3 Tickets MCP Server.exe'

#### Installation instructions (manual)

1. Install [Python 3.13.5](https://www.python.org/downloads/release/python-3135/).

2. Install [uv](https://docs.astral.sh/uv/) Python package manager. 

3. Add uv to PATH.

4. Create a designated user in REI3 with access to the Tickets API role. <br> This user will be used for authentication.

5. Set up an API Profile in your REI3 tickets instance. <br> You can create one under: Tickets > Admin Tab > API profiles 

6. Download/Clone and extract this repository and adjust the config.ini file variables.

7. Ensure you have an MCP Client with the capability to run MCP tools at your disposal. <br> I used [AnythingLLM](https://anythingllm.com/)

8. Configure the MCP-Server JSON configuration to include the REI3-Tickets-MCP-Server.

#### Installation instruction (docker)

1. Install [docker](https://www.docker.com/).

2. Install [git](https://git-scm.com/downloads).

3. Create a designated user in REI3 with access to the Tickets API role. <br> This user will be used for authentication.

4. Set up an API Profile in your REI3 tickets instance. <br> You can create one under: Tickets > Admin Tab > API profiles.

5. Download/Clone and extract this repository and adjust the config.ini file variables.

6. Run the ```setup_docker.ps1``` script, it will create the docker image for you, as well as provide instructions on how to create the container.

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
		"url": "http://127.0.0.1:54321/mcp/",
		"type": "streamable"
	}
  }
}
```

## Demonstration

#### Creating a REI3 ticket using the REI3-Tickets-MCP-Server:

<img width="1309" height="248" alt="Create_Ticket_with_MCP_Server" src="https://github.com/user-attachments/assets/50b5294d-e4fe-4933-952b-bebeedce3176" />

#### Created ticket:

<img width="1918" height="947" alt="Created_Ticket_in_Not_Assigned" src="https://github.com/user-attachments/assets/db6524cc-be80-41d0-bbee-3efe66f71036" />

#### Created ticket worklog:

<img width="1876" height="806" alt="Created_Ticket_Worklog" src="https://github.com/user-attachments/assets/68ca765f-1ce9-42a4-804f-dddbbb190cea" />

#### Creating a worklog entry inside an existing ticket:

<img width="1320" height="398" alt="Create_Ticket_Worklog_with_MCP_Server" src="https://github.com/user-attachments/assets/ed0cd005-ee54-4f77-bc0f-3eff02cb6529" />

#### Created ticket worklog:

<img width="1877" height="810" alt="Create_Second_Ticket_Worklog" src="https://github.com/user-attachments/assets/a9c34eea-83b9-42bb-abff-a8c47faf3440" />

####

## Credits

This software utilizes:

- [REI3](https://github.com/r3-team/r3)

## Donate

<div align=center> 
    <a href='https://www.paypal.com/paypalme/lgndluke' target='_blank'><img height='50' src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/PayPal.svg/2560px-PayPal.svg.png' alt='Support Me via PayPal'/></a>
</div>
