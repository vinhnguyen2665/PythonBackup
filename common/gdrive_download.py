import functools
import os
import shutil
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def download_file_from_google_drive(url, destination):
    session = requests.Session()
    response = session.get(url, stream=True)
    if response.url:
        with requests.get(response.url, stream=True) as r:
            if response.headers['Content-Type'].startswith('text/html'):
                soup = BeautifulSoup(r.content, features="html.parser")
                uc_download_link = soup.select_one('#uc-download-link')
                download_form = soup.select_one('#download-form')
                if download_form:
                    action = download_form['action']
                    response = session.post(action, stream=True)
                    total_length = response.headers.get('content-length')
                    response.raw.read = functools.partial(response.raw.read, decode_content=True)
                    with open(destination, 'wb') as f:
                        shutil.copyfileobj(response.raw, f)
                        return destination
            else:
                total_length = r.headers.get('content-length')
                r.raw.read = functools.partial(r.raw.read, decode_content=True)
                with open(destination, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                    return destination


    # response = session.post(url_download, stream=True)
    # token = get_confirm_token(response)
    #
    # if token:
    #     params = {'id': id, 'confirm': token}
    #     if os.path.isdir(destination):
    #         destination += url_download.split('/')[-1]
    #     with requests.get(url_download, params=params, stream=True) as r:
    #         r.raw.read = functools.partial(r.raw.read, decode_content=True)
    #         with open(destination, 'wb') as f:
    #             shutil.copyfileobj(r.raw, f)
    #     return destination


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None
