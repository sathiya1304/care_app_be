"""Auth controller — replaces login.php and admin session management."""

from flask import request, session, current_app
from src.models.registration import Registration
from src.utils.helpers import success_response, error_response


def login():
    """Mobile login by mobile number (GET) — mirrors login.php.
    Also handles admin web login (POST with username/password).
    """
    if request.method == "POST":
        # Admin web login
        data = request.get_json(silent=True) or {}
        username = data.get("username", "")
        password = data.get("password", "")
        admin_mobile = current_app.config["ADMIN_MOBILE"]
        admin_password = current_app.config["ADMIN_PASSWORD"]

        if username == admin_mobile and password == admin_password:
            session["is_admin"] = True
            session["username"] = "admin"
            return success_response({"role": "admin"}, "Login successful")
        return error_response("Invalid credentials", 401)

    # Mobile app login (GET ?mobile=...)
    mobile = request.args.get("mobile", "").strip()
    if not mobile:
        return error_response("Mobile number is required", 400)

    admin_mobile = current_app.config["ADMIN_MOBILE"]
    if mobile == admin_mobile:
        return success_response({"records": [{"childName": "admin"}]})

    children = Registration.query.filter_by(mobile=mobile).all()
    if not children:
        return error_response("No records found.", 404)

    records = [{"childName": c.childName} for c in children]
    return success_response({"records": records})


def logout():
    session.clear()
    return success_response(message="Logged out")


def check_session():
    if session.get("is_admin"):
        return success_response({"role": "admin", "username": session.get("username")})
    return error_response("Not authenticated", 401)
