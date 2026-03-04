"""Authentication middleware — replaces the missing auth in the PHP version."""

from functools import wraps
from flask import request, session
from src.utils.helpers import error_response


def admin_required(f):
    """Decorator: require admin session for web/admin endpoints."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return error_response("Unauthorized — admin login required", 401)
        return f(*args, **kwargs)
    return decorated


def mobile_auth_optional(f):
    """Decorator: mobile API endpoints — no strict auth (matches original PHP behaviour)."""
    @wraps(f)
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated
