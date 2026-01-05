from flask import make_response, request


def debug():
    resp = make_response(f"Debug info: {dict(request.headers)}")
    return resp

