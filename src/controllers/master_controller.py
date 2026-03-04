"""Master data controller — CRUD for City, Union, Panchayat, Centre, Cluster, Employee.

Replaces all the *_methods.php files (employees_methods.php, centre_methods.php,
panchayat_methods.php, union_methods.php, cluster_methods.php) and their
corresponding *_action.php files with a single generic CRUD pattern.
"""

from flask import request
from src import db
from src.models.city import City
from src.models.union import Union
from src.models.panchayat import Panchayat
from src.models.childcare_centre import ChildcareCentre
from src.models.cluster import Cluster
from src.models.employee import Employee
from src.models.evaluation_month import EvaluationMonth
from src.utils.helpers import success_response, error_response

# ──────────────────────── Generic CRUD helper ────────────────────────

_MODEL_MAP = {
    "city": (City, "cityID"),
    "union": (Union, "unionID"),
    "panchayat": (Panchayat, "panchayatID"),
    "centre": (ChildcareCentre, "centreID"),
    "cluster": (Cluster, "clusterID"),
    "employee": (Employee, "employeeID"),
    "evaluationmonth": (EvaluationMonth, "id"),
}

# Fields allowed for each entity create/update
_FIELDS = {
    "city": ["cityName"],
    "union": ["unionName", "cityID"],
    "panchayat": ["panchayatName", "unionID", "cityID"],
    "centre": ["centreName", "panchayatID", "cityID", "unionID"],
    "cluster": ["clusterName", "centreID"],
    "employee": ["cityID", "clusterID", "userName", "userPassword", "otherInfo"],
    "evaluationmonth": ["evaluationMonthEnd"],
}


def list_items(entity: str):
    """List all items with optional search and pagination (DataTables compatible)."""
    if entity not in _MODEL_MAP:
        return error_response(f"Unknown entity: {entity}", 400)

    Model, pk = _MODEL_MAP[entity]
    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)

    query = Model.query
    if search:
        # Search across all string columns
        filters = []
        for col in Model.__table__.columns:
            if str(col.type) in ("VARCHAR", "TEXT", "String(255)", "String(20)"):
                filters.append(col.ilike(f"%{search}%"))
        if filters:
            query = query.filter(db.or_(*filters))

    query = query.order_by(getattr(Model, pk).desc())
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return success_response({
        "records": [item.to_dict() for item in items],
        "total": total,
        "page": page,
        "per_page": per_page,
    })


def get_item(entity: str, item_id: int):
    """Get single item by ID."""
    if entity not in _MODEL_MAP:
        return error_response(f"Unknown entity: {entity}", 400)

    Model, pk = _MODEL_MAP[entity]
    item = Model.query.get(item_id)
    if not item:
        return error_response("Record not found", 404)

    return success_response(item.to_dict())


def create_item(entity: str):
    """Create a new item."""
    if entity not in _MODEL_MAP:
        return error_response(f"Unknown entity: {entity}", 400)

    Model, pk = _MODEL_MAP[entity]
    data = request.get_json(silent=True) or {}
    allowed = _FIELDS.get(entity, [])

    item = Model()
    # Auto-set status to "yes" on creation
    if hasattr(item, "status"):
        item.status = "yes"
    for field in allowed:
        if field in data:
            setattr(item, field, data[field])

    try:
        db.session.add(item)
        db.session.commit()
        return success_response(item.to_dict(), "Created successfully", 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f"Create failed: {str(e)}", 500)


def update_item(entity: str, item_id: int):
    """Update an existing item."""
    if entity not in _MODEL_MAP:
        return error_response(f"Unknown entity: {entity}", 400)

    Model, pk = _MODEL_MAP[entity]
    item = Model.query.get(item_id)
    if not item:
        return error_response("Record not found", 404)

    data = request.get_json(silent=True) or {}
    allowed = _FIELDS.get(entity, [])

    for field in allowed:
        if field in data:
            setattr(item, field, data[field])

    try:
        db.session.commit()
        return success_response(item.to_dict(), "Updated successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Update failed: {str(e)}", 500)


def delete_item(entity: str, item_id: int):
    """Delete an item."""
    if entity not in _MODEL_MAP:
        return error_response(f"Unknown entity: {entity}", 400)

    Model, pk = _MODEL_MAP[entity]
    item = Model.query.get(item_id)
    if not item:
        return error_response("Record not found", 404)

    try:
        db.session.delete(item)
        db.session.commit()
        return success_response(message="Deleted successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Delete failed: {str(e)}", 500)
