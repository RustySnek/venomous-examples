import requests


def request_server(host):
    resp = requests.get(host)
    return resp.text
