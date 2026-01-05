from flask import request


def reflected_xss():
    q = request.args.get("q", "")
    return f"<h2>Echo: {q}</h2><a href='/'>Main Menu</a>"

