from flask import redirect, request


def open_redirect():
    url = request.args.get("url", "/")
    return redirect(url)

