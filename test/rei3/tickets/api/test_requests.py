from flask import Flask, jsonify, request
from src.rei3.tickets.api.requests import *
from urllib.parse import urlparse

# ----------------------------
# Constants
# ----------------------------

BASE_URL          = get_config_value('rei3-tickets-api', 'base_url')

BASE_URL_HOST     = urlparse(BASE_URL).hostname
BASE_URL_PORT     = urlparse(BASE_URL).port

API_AUTH_ENDPOINT = "/api/auth"
API_BASE_ENDPOINT = "/api/lsw_tickets"

CLOSE_TICKET_EXTENSION        = "/close_ticket/v1"
CREATE_TICKET_EXTENSION       = "/create_ticket/v1"
CREATE_WORKLOG_EXTENSION      = "/create_worklog/v1"
GET_WORKLOGS_BY_KEY_EXTENSION = "/get_public_worklogs_by_ticket_key/v1"
GET_TICKET_INFO_EXTENSION     = "/get_ticket_info_by_key/v1"

# ----------------------------
# Setup of test endpoints
# ----------------------------

app = Flask(__name__)

default_auth = {
    'username': 'admin',
    'password': 'admin123'
}

@app.route(API_AUTH_ENDPOINT, methods=['POST'])
def auth():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if username in default_auth and default_auth[username] == password:
        return jsonify({"status": "success", "token": ""}), 200
    else:
        return jsonify({"status": "fail", "message": "Unauthorized"}), 401

@app.route(f"{API_BASE_ENDPOINT}{CLOSE_TICKET_EXTENSION}", methods=['POST'])
def close_ticket():

    # TODO implement once close_ticket API is implemented into REI3.
    return ""

@app.route(f"{API_BASE_ENDPOINT}{CREATE_TICKET_EXTENSION}", methods=['POST'])
def create_ticket():
    # TODO implement.
    return ""

@app.route(f"{API_BASE_ENDPOINT}{CREATE_WORKLOG_EXTENSION}", methods=['POST'])
def create_worklog():
    # TODO implement.
    return ""

@app.route(f"{API_BASE_ENDPOINT}{GET_WORKLOGS_BY_KEY_EXTENSION}", methods=['GET'])
def get_worklogs_by_key():
    # TODO implement once get_worklogs_by_key_extension API is implemented into REI3.
    return ""

@app.route(f"{API_BASE_ENDPOINT}{GET_TICKET_INFO_EXTENSION}", methods=['GET'])
def get_ticket_info():
    # TODO implement once get_ticket_info API is implemented into REI3.
    return ""

app.run(host=BASE_URL_HOST, port=BASE_URL_PORT, debug=True)

# ----------------------------
# Tests
# ----------------------------

def test_close_ticket():
    # TODO implement.
    return 0

def test_create_ticket():
    # TODO implement.
    return 0

def test_create_worklog():
    # TODO implement.
    return 0

def test_get_public_worklogs_by_ticket_key():
    # TODO implement.
    return 0

def test_get_ticket_info_by_key():
    # TODO implement.
    return 0
