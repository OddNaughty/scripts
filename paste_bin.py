#!/usr/bin/python3

import requests
import os
import sys

API_KEY = "72438207e343e6c8a489a7ff2e0506fe"
API_URL = "http://pastebin.com/api"


def manage_extensions(ext):
    extensions = {
        ".py": "Python"
    }
    return (extensions[ext])


def post_file(file_path):
    endpoint = API_URL + "/api_post.php"
    complete_path = os.path.join(os.getcwd(), file_path)
    payload = {
        "api_dev_key": API_KEY,
        "api_option": "paste",
        "api_paste_name": os.path.basename(file_path),
        "api_paste_format": manage_extensions(os.path.splitext(file_path)[1])
    }
    with open(file_path) as f:
        payload["api_paste_code"] = f.read()
        res = requests.post(endpoint, payload)
        print(res.text)


if __name__ == '__main__':
    """
        Usage: ./paste_bin.py file
        Why not ls -s paste_bin.py /usr/local/bin/pastebin ? :)
    """
    # TODO: ArgumentParser...
    post_file(os.path.join(os.getcwd(), sys.argv[1]))
