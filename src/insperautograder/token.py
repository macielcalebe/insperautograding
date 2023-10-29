"""
Authentication token management
"""

import os
import requests
from IPython.display import display, clear_output, Markdown
from dotenv import load_dotenv
from . import config


load_dotenv(override=True)


def get_new_token(username, url=None):
    """Generate an authentication token for a given username.

    Args:
        username (str): Username.
        url (str, optional): Test server URL. Defaults to None, then the URL value is read from the `IAG_SERVER_URL` environment variable.
    """
    if url is None:
        url_base = os.getenv("IAG_SERVER_URL")
        url = f"{url_base}/token"

    data = {
        "username": username,
    }

    req = requests.post(url, json=data, timeout=config.GET_TOKEN_TIMEOUT)
    clear_output()
    display(Markdown(req.text))
