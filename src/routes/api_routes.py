"""All API routes — single Blueprint replaces all PHP endpoint files."""

from flask import Blueprint
from src.controllers import (
    auth_controller,
    registration_controller,
    evaluation_controller,
    location_controller,
    dashboard_controller,
    master_controller,
    report_controller,
)
from src.middlewares.auth import admin_required
from src.utils.otp_service import send_otp
from flask import request
from src.utils.helpers import success_response, error_response

api_bp = Blueprint("api", __name__)

# ──────────────────────── Auth ────────────────────────
api_bp.add_url_rule("/auth/login", view_func=auth_controller.login, methods=["GET", "POST"])
api_bp.add_url_rule("/auth/logout", view_func=auth_controller.logout, methods=["POST"])
api_bp.add_url_rule("/auth/session", view_func=auth_controller.check_session, methods=["GET"])

# ──────────────────────── Mobile API (matches original PHP endpoints) ────────────────────────
api_bp.add_url_rule("/check-mobile", view_func=registration_controller.check_mobile, methods=["GET"])
api_bp.add_url_rule("/register", view_func=registration_controller.register_child, methods=["POST"])
api_bp.add_url_rule("/get-term", view_func=evaluation_controller.get_term, methods=["GET"])
api_bp.add_url_rule("/update-score", view_func=evaluation_controller.update_score, methods=["GET"])
api_bp.add_url_rule("/get-panchayats", view_func=location_controller.get_panchayats, methods=["GET"])
api_bp.add_url_rule("/get-childcare", view_func=location_controller.get_childcare_centres, methods=["GET"])


@api_bp.route("/send-otp", methods=["POST"])
def send_otp_route():
    data = request.get_json(silent=True) or {}
    mobile = data.get("mobile", "").strip()
    otp = data.get("otp", "").strip()
    if not mobile or not otp:
        return error_response("mobile and otp are required", 400)
    result = send_otp(mobile, otp)
    return success_response(result)


# ──────────────────────── Dashboard ────────────────────────
api_bp.add_url_rule("/dashboard/stats", view_func=dashboard_controller.get_dashboard_stats, methods=["GET"])
api_bp.add_url_rule("/dashboard/chart-age", view_func=dashboard_controller.get_chart_age_data, methods=["GET"])
api_bp.add_url_rule("/dashboard/chart-gender", view_func=dashboard_controller.get_chart_gender_data, methods=["GET"])

# ──────────────────────── Reports ────────────────────────
api_bp.add_url_rule("/entries", view_func=report_controller.get_entries, methods=["GET"])
api_bp.add_url_rule("/child-wise-data", view_func=report_controller.get_child_wise_data, methods=["GET"])


# ──────────────────────── Master CRUD (admin) ────────────────────────
ENTITIES = ["city", "union", "panchayat", "centre", "cluster", "employee", "evaluationmonth"]

for entity in ENTITIES:
    # GET  /api/<entity>          → list
    # POST /api/<entity>          → create
    # GET  /api/<entity>/<id>     → read
    # PUT  /api/<entity>/<id>     → update
    # DELETE /api/<entity>/<id>   → delete
    api_bp.add_url_rule(
        f"/{entity}",
        endpoint=f"{entity}_list",
        view_func=lambda e=entity: master_controller.list_items(e),
        methods=["GET"],
    )
    api_bp.add_url_rule(
        f"/{entity}",
        endpoint=f"{entity}_create",
        view_func=lambda e=entity: master_controller.create_item(e),
        methods=["POST"],
    )
    api_bp.add_url_rule(
        f"/{entity}/<int:item_id>",
        endpoint=f"{entity}_get",
        view_func=lambda item_id, e=entity: master_controller.get_item(e, item_id),
        methods=["GET"],
    )
    api_bp.add_url_rule(
        f"/{entity}/<int:item_id>",
        endpoint=f"{entity}_update",
        view_func=lambda item_id, e=entity: master_controller.update_item(e, item_id),
        methods=["PUT"],
    )
    api_bp.add_url_rule(
        f"/{entity}/<int:item_id>",
        endpoint=f"{entity}_delete",
        view_func=lambda item_id, e=entity: master_controller.delete_item(e, item_id),
        methods=["DELETE"],
    )
