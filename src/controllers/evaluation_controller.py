"""Evaluation controller — replaces update_score.php, get_term.php."""

from flask import request
from src import db
from src.models.evaluate import Evaluate
from src.utils.helpers import success_response, error_response


def get_term():
    """Get term and age for a child — mirrors get_term.php."""
    mobile = request.args.get("mobile", "").strip()
    child_name = request.args.get("childName", "").strip()

    if not mobile or not child_name:
        return error_response("mobile and childName are required", 400)

    record = Evaluate.query.filter_by(mobile=mobile, childName=child_name).first()
    if not record:
        return error_response("Data not found", 404, "607")

    return success_response({
        "age": record.age,
        "termStatus": record.termStatus,
    })


def update_score():
    """Update evaluation score — mirrors update_score.php."""
    mobile = request.args.get("mobile", "").strip()
    child_name = request.args.get("childName", "").strip()
    result_score = request.args.get("result", "").strip()

    if not mobile or not child_name:
        return error_response("mobile and childName are required", 400)

    record = Evaluate.query.filter_by(mobile=mobile, childName=child_name).first()
    if not record:
        return error_response("Data not found", 400, "607")

    term_col = record.termStatus
    if not term_col or not hasattr(record, term_col):
        return error_response("Invalid term status", 400)

    setattr(record, term_col, result_score)

    try:
        db.session.commit()
        return success_response(message="Scores updated successfully.", status_code=201)
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to update: {str(e)}", 500)
