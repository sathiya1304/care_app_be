"""Shared response helpers."""

from flask import jsonify


def success_response(data=None, message="Success", status_code=200):
    body = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    return jsonify(body), status_code


def error_response(message="Error", status_code=400, code=None):
    body = {"success": False, "message": message}
    if code:
        body["statusCode"] = code
    return jsonify(body), status_code
