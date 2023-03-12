import requests
import os
from IPython.display import display, clear_output, Markdown

from dotenv import load_dotenv

load_dotenv(override=True)

def get_new_token(username, url=None):
    if url is None:
        url_base = os.getenv('IAG_SERVER_URL')
        url = f'{url_base}/token'
    print(url)

    data = {
        'username': username,
    }

    req = requests.post(url, json=data)
    clear_output()
    display(Markdown(req.text))