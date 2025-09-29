import httpx

from src.common.config_handler import get_config_value
from src.common.formatter import format_ticket_key
from typing import Any

# ----------------------------
# Constants
# ----------------------------

USER_AGENT = "rei3-tickets-mcp-server/1.0"

API_AUTH_ENDPOINT = "/api/auth"
API_BASE_ENDPOINT = "/api/lsw_tickets"

CLOSE_TICKET_EXTENSION        = "/close_ticket/v1"
CREATE_TICKET_EXTENSION       = "/create_ticket/v1"
CREATE_WORKLOG_EXTENSION      = "/create_worklog/v1"
GET_WORKLOGS_BY_KEY_EXTENSION = "/get_public_worklogs_by_ticket_key/v1"
GET_TICKET_INFO_EXTENSION     = "/get_ticket_info_by_key/v1"

# ----------------------------
# Private Config Accessors
# ----------------------------

def _get_base_url() -> str:
    return get_config_value('rei3-tickets-api', 'base_url')

def _get_tickets_api_username() -> str:
    return get_config_value('rei3-tickets-api', 'username')

def _get_tickets_api_password() -> str:
    return get_config_value('rei3-tickets-api', 'password')

def _get_tickets_api_email() -> str:
    return get_config_value('rei3-tickets-api', 'email')

def _get_tickets_api_profile_id() -> str:
    return get_config_value('rei3-tickets-api', 'profile')

# ----------------------------
# Private Functions
# ----------------------------

async def _tickets_api_auth() -> dict[str, Any] | None:
    """
    Authenticate with the REI3 Tickets API to retrieve a bearer token.

    :returns:
        A dictionary containing the bearer token if successful, otherwise None.
    """
    url = f"{_get_base_url()}{API_AUTH_ENDPOINT}"

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }

    payload = {
        "username": _get_tickets_api_username(),
        "password": _get_tickets_api_password(),
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return None

async def _get_bearer_token() -> str | None:
    """
    Fetch the bearer token from the REI3 Tickets API authentication process and return it as string value.

    :returns:
        The bearer token as string value if successful, otherwise None.
    """
    response = await _tickets_api_auth()

    if not response:
        return "Failed to authenticate with REI3 tickets API!"

    return response["token"]

# ----------------------------
# Public Functions
# ----------------------------

async def close_ticket_by_key(key: str, closing_text: str) -> str:
    """
    Close a ticket specified by its ticket key inside the REI3 Tickets application.

    Args:
        key: The ticket key. (e.g.: '000015' or '15')
        closing_text: The closing text of the ticket.

    :returns:
        A success message including the closed ticket ID or an error message.
    """
    bearer_token = await _get_bearer_token()

    url = f"{_get_base_url()}{API_BASE_ENDPOINT}{CLOSE_TICKET_EXTENSION}"

    formatted_key = format_ticket_key(key)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Authorization": f"Bearer {bearer_token}",
    }

    payload = {
        "0(ticket)": {
            "key": formatted_key,
            "closing_text": closing_text,
            "is_api": True
        },
        "1(state)": {
            "state": "Closed",
        }
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            ticket_id = response.json()["0"]
            return f"Ticket key {formatted_key} corresponded to ticket id #{ticket_id}. The ticket with id #{ticket_id} was closed successfully."
        except httpx.HTTPStatusError as e:
            return f"Failed to close ticket: {e.response.text if e.response else 'Unknown Error'}"

async def create_ticket(subject: str, description: str) -> str:
    """
    Create a ticket inside the REI3 Tickets application.

    Args:
        subject: The subject of the ticket.
        description: The description of the ticket.

    :returns:
        A success message including the created ticket ID or an error message.
    """
    bearer_token = await _get_bearer_token()

    url = f"{_get_base_url()}{API_BASE_ENDPOINT}{CREATE_TICKET_EXTENSION}"

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }

    payload = {
        "0(ticket)": {
            "subject": subject,
            "description": description,
            "api_requested_for": _get_tickets_api_email()
        },
        "2(api_profile)": {
            "id": _get_tickets_api_profile_id()
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

async def create_worklog(note: str, key: str) -> str:
    """
    Create a worklog entry for a specific ticket inside the REI3 Tickets application.

    Args:
        note: The content or note to include in the worklog.
        key: The numeric ID of the ticket.

    :returns:
        A success message including the created worklog ID or an error message.
    """
    bearer_token = await _get_bearer_token()

    url = f"{_get_base_url()}{API_BASE_ENDPOINT}{CREATE_WORKLOG_EXTENSION}"

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
            "email": _get_tickets_api_email(),
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

async def get_public_worklogs_by_ticket_key(key: str) -> str:
    """
    Fetches all public worklog entries of a ticket specified by its ticket key.

    Args:
        key: The ticket key. (e.g.: '000015')

    :returns:
        The fetched public worklog entries or an error message.
    """
    bearer_token = await _get_bearer_token()

    url = f"{_get_base_url()}{API_BASE_ENDPOINT}{CLOSE_TICKET_EXTENSION}"

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Authorization": f"Bearer {bearer_token}",
    }

    payload = {
        # TODO Insert when API is available.
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            # TODO
            return ""
        except httpx.HTTPStatusError as e:
            return f"Failed to fetch ticket worklogs: {e.response.text if e.response else 'Unknown Error'}"

async def get_ticket_info_by_key(key: str) -> str:
    """
    Fetches all ticket information of a ticket specified by its ticket key.

    Args:
        key: The ticket key. (e.g.: '000015')

    :returns:
        The fetched ticket information or an error message.
    """
    bearer_token = await _get_bearer_token()

    url = f"{_get_base_url()}{API_BASE_ENDPOINT}{CLOSE_TICKET_EXTENSION}"

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Authorization": f"Bearer {bearer_token}",
    }

    payload = {
        # TODO Insert when API is available.
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            # TODO
            return ""
        except httpx.HTTPStatusError as e:
            return f"Failed to fetch ticket worklogs: {e.response.text if e.response else 'Unknown Error'}"