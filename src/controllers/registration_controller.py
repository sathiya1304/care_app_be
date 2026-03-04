"""Registration controller — replaces register.php, update_evaluation.php, check_mobile.php."""

from datetime import date, datetime
from flask import request
from src import db
from src.models.registration import Registration
from src.models.evaluate import Evaluate
from src.models.evaluation_month import EvaluationMonth
from src.utils.term_calculator import calculate_term_status
from src.utils.helpers import success_response, error_response


def check_mobile():
    """Check if mobile exists and return child details — mirrors check_mobile.php."""
    mobile = request.args.get("mobile", "").strip()
    if not mobile:
        return error_response("Mobile number is required", 400)

    children = Registration.query.filter_by(mobile=mobile).all()
    if not children:
        return success_response(
            {"message": "create new record", "statusCode": "601"}
        )

    records = [c.to_dict() for c in children]
    return success_response({"records": records})


def register_child():
    """Register a new child — replaces both register.php and update_evaluation.php."""
    data = request.get_json(silent=True) or {}

    required = ["childName", "dateofBirth", "fatherName", "motherName",
                 "mobile", "gender", "myunion", "city", "panchayat", "centreName"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return error_response(
            "Unable to create new registration. Data is incomplete.",
            400, "605"
        )

    # Get evaluation end date
    eval_month = EvaluationMonth.query.first()
    if not eval_month:
        return error_response("Evaluation month not configured", 500)

    evaluation_end = eval_month.evaluationMonthEnd
    dob = datetime.strptime(data["dateofBirth"], "%Y-%m-%d").date()
    age_years, term_status = calculate_term_status(dob, evaluation_end)

    # Age validation (2–4 years only)
    if age_years < 2 or age_years > 4:
        return error_response("Age criteria not satisfied", 400, "604")

    # Check duplicate
    existing = Registration.query.filter_by(
        mobile=data["mobile"], childName=data["childName"]
    ).first()
    if existing:
        return error_response(
            "Student already registered with same name and mobile number.",
            409, "603"
        )

    # Create registration
    reg = Registration(
        mobile=data["mobile"],
        childName=data["childName"],
        fatherName=data["fatherName"],
        motherName=data["motherName"],
        dateofRegistration=date.today(),
        dateofBirth=dob,
        gender=data["gender"],
        age=age_years,
        city=data["city"],
        myunion=data["myunion"],
        panchayat=data["panchayat"],
        centreName=data["centreName"],
        status="yes",
    )
    db.session.add(reg)

    # Create evaluate entry
    evaluate = Evaluate(
        mobile=data["mobile"],
        childName=data["childName"],
        centreName=data["centreName"],
        dateofBirth=dob,
        age=age_years,
        termStatus=term_status,
        status="yes",
    )
    db.session.add(evaluate)

    try:
        db.session.commit()
        return success_response(
            message="Student registered successfully.",
            status_code=201,
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to register: {str(e)}", 500)
