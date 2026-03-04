"""Report controller — replaces reports.php / adminReports.php."""

from flask import request
from src import db
from src.models.registration import Registration
from src.models.evaluate import Evaluate
from src.utils.helpers import success_response


def get_entries():
    """List all registered children with pagination."""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)
    search = request.args.get("search", "").strip()

    query = Registration.query
    if search:
        query = query.filter(
            db.or_(
                Registration.childName.ilike(f"%{search}%"),
                Registration.mobile.ilike(f"%{search}%"),
                Registration.centreName.ilike(f"%{search}%"),
            )
        )

    total = query.count()
    items = query.order_by(Registration.sno.desc()) \
                 .offset((page - 1) * per_page) \
                 .limit(per_page) \
                 .all()

    return success_response({
        "records": [r.to_dict() for r in items],
        "total": total,
        "page": page,
        "per_page": per_page,
    })


def get_child_wise_data():
    """Get evaluation data for a specific age group."""
    age = request.args.get("age", type=int)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)

    query = Evaluate.query
    if age:
        query = query.filter_by(age=age)

    total = query.count()
    items = query.order_by(Evaluate.id.desc()) \
                 .offset((page - 1) * per_page) \
                 .limit(per_page) \
                 .all()

    return success_response({
        "records": [e.to_dict() for e in items],
        "total": total,
        "page": page,
        "per_page": per_page,
    })
