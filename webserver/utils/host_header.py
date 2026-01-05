from flask import request


def host_header():
    host = request.headers.get("Host", "")
    return f"<h2>Host: {host}</h2><a href='/'>Main Menu</a>"
