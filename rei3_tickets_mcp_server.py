import os
from typing import Any

import dotenv
import httpx
from mcp.server.fastmcp import FastMCP

# Load .env and initialize FastMCP server.
dotenv.load_dotenv()
rei3_tickets_mcp_server = FastMCP(name="REI3 Tickets MCP Server")

# Constants
USER_AGENT        = "rei3-tickets-mcp-server/1.0"

BASE_URL          = os.getenv("REI3_BASE_URL")
API_AUTH_ENDPOINT = "/api/auth"
API_POST_ENDPOINT = "/api/lsw_tickets"

TICKETS_API_USERNAME   = os.getenv("REI3_TICKETS_API_USERNAME")
TICKETS_API_PASSWORD   = os.getenv("REI3_TICKETS_API_PASSWORD")
TICKETS_API_EMAIL      = os.getenv("REI3_TICKETS_API_EMAIL", "tickets-mcp-server@mcp.local") # Default email if not set.
TICKETS_API_PROFILE_ID = os.getenv("REI3_TICKETS_API_PROFILE_ID")
TICKETS_KEY_FORMAT     = os.getenv("REI3_TICKETS_KEY_FORMAT", "{key:06d}") # Default format if not set.

# ----------------------------
# Helper functions
# ----------------------------

async def make_api_auth_request() -> dict[str, Any] | None:
    """
    Authenticate with the REI3 Tickets API and retrieve a bearer token.

    :returns:
        A dictionary containing the bearer token if successful, otherwise None.
    """
    url = f"{BASE_URL}{API_AUTH_ENDPOINT}"

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }

    payload = {
        "username": TICKETS_API_USERNAME,
        "password": TICKETS_API_PASSWORD,
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return None

def format_ticket_key(key: str) -> str:
    """
    Format the ticket key using a customizable format from the .env file.

    Args:
        key: The ticket key to format. (e.g.: '15').

    :returns:
        The formatted ticket key. (e.g.: '000015'
    """
    try:
        return TICKETS_KEY_FORMAT.format(key=int(key))
    except (ValueError, KeyError):
        return key

# ----------------------------
# MCP Tools
# ----------------------------

@rei3_tickets_mcp_server.tool()
async def create_ticket(subject: str, description: str) -> str:
    """
    Create a ticket inside the REI3 Tickets application.

    Args:
        subject: The subject of the ticket.
        description: The description of the ticket.

    :returns:
        A success message including the created ticket ID or an error message.
    """
    response = await make_api_auth_request()
    if not response:
        return "Failed to authenticate with REI3 tickets API!"

    bearer_token = response["token"]

    tool_specific_endpoint_extension = "/create_ticket/v1"
    url = f"{BASE_URL}{API_POST_ENDPOINT}{tool_specific_endpoint_extension}"

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }

    payload = {
        "0(ticket)": {
            "subject": subject,
            "description": description,
            "api_requested_for": TICKETS_API_EMAIL
        },
        "2(api_profile)": {
            "id": TICKETS_API_PROFILE_ID
        }
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            ticket_id = response.json()["0"]
            return f"Ticket #{ticket_id} was successfully created."
        except httpx.HTTPStatusError as e:
            return f"Failed to create ticket: {e.response.text if e.response else 'Unknown Error'}"

@rei3_tickets_mcp_server.tool()
async def create_worklog(note: str, key: str) -> str:
    """
    Create a worklog entry for a specific ticket inside the REI3 Tickets application.

    Args:
        note: The content or note to include in the worklog.
        key: The numeric ID of the ticket.

    :returns:
        A success message including the created worklog ID or an error message.
    """
    response = await make_api_auth_request()
    if not response:
        return "Failed to authenticate with REI3 tickets API!"

    bearer_token = response["token"]

    tool_specific_endpoint_extension = "/create_worklog/v1"
    url = f"{BASE_URL}{API_POST_ENDPOINT}{tool_specific_endpoint_extension}"

    formatted_key = format_ticket_key(key)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }

    payload = {
        "0(worklog)": {
            "note": note,
            "is_api": True
        },
        "1(contact)": {
            "email": TICKETS_API_EMAIL,
        },
        "2(ticket)": {
            "key": formatted_key,
        }
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            worklog_id = response.json()["0"]
            return f"Worklog #{worklog_id} was successfully created."
        except httpx.HTTPStatusError as e:
            return f"Failed to create worklog: {e.response.text if e.response else 'Unknown Error'}"

# ----------------------------
# Entry Point
# ----------------------------

if __name__ == "__main__":
    rei3_tickets_mcp_server.run(transport='stdio')
