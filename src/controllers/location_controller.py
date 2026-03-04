"""Location controller — replaces getChildcare.php, getPanchayat.php."""

from flask import request
from src.models.panchayat import Panchayat
from src.models.childcare_centre import ChildcareCentre
from src.utils.helpers import success_response, error_response


def get_panchayats():
    """Get panchayats by unionID — mirrors getPanchayat.php."""
    union_id = request.args.get("unionID", "").strip()
    if not union_id:
        return error_response("unionID is required", 400)

    items = Panchayat.query.filter_by(unionID=union_id).all()
    return success_response([
        {"panchayatID": p.panchayatID, "panchayatName": p.panchayatName}
        for p in items
    ])


def get_childcare_centres():
    """Get childcare centres by panchayatID — mirrors getChildcare.php."""
    panchayat_id = request.args.get("panchayatID", "").strip()
    if not panchayat_id:
        return error_response("panchayatID is required", 400)

    items = ChildcareCentre.query.filter_by(panchayatID=panchayat_id).all()
    return success_response([
        {"centreID": c.centreID, "centreName": c.centreName}
        for c in items
    ])
