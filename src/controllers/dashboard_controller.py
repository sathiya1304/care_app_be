"""Dashboard controller — replaces the inline PHP queries in dashboard.php and getChartAge*.php."""

from flask import request
from src import db
from src.models.registration import Registration
from src.models.evaluate import Evaluate
from src.models.panchayat import Panchayat
from src.models.childcare_centre import ChildcareCentre
from src.utils.term_calculator import (
    get_age_split_points,
    get_term_columns_for_age,
    parse_scores_into_categories,
)
from src.utils.helpers import success_response


def get_dashboard_stats():
    """Return all dashboard summary counts — replaces the inline SQL in dashboard.php."""
    male_count = Registration.query.filter_by(gender="male").count()
    female_count = Registration.query.filter_by(gender="female").count()
    total_registered = Registration.query.count()
    panchayat_count = Panchayat.query.count()
    centre_count = ChildcareCentre.query.count()

    age2 = Registration.query.filter_by(age=2).count()
    age3 = Registration.query.filter_by(age=3).count()
    age4 = Registration.query.filter_by(age=4).count()

    # Evaluated count (children whose current term column has a value)
    all_evals = Evaluate.query.filter(Evaluate.termStatus != "NIL").all()
    unevaluated = sum(
        1 for e in all_evals
        if not getattr(e, e.termStatus, None)
    )
    evaluated_count = len(all_evals) - unevaluated
    total_eval = Evaluate.query.count()

    # Union-wise gender counts
    unions = db.session.query(Registration.myunion).distinct().all()
    union_stats = {}
    for (union_name,) in unions:
        m = Registration.query.filter_by(myunion=union_name, gender="male").count()
        f = Registration.query.filter_by(myunion=union_name, gender="female").count()
        union_stats[union_name] = {"male": m, "female": f}

    return success_response({
        "totalMale": male_count,
        "totalFemale": female_count,
        "totalRegistered": total_registered,
        "totalEvaluated": evaluated_count,
        "totalEvalRecords": total_eval,
        "panchayatCount": panchayat_count,
        "centreCount": centre_count,
        "ageWise": {"age2": age2, "age3": age3, "age4": age4},
        "unionStats": union_stats,
    })


def get_chart_age_data():
    """Return aggregated chart data by age & union — replaces getChartAgeData.php."""
    age = request.args.get("age", type=int)
    union = request.args.get("union", "").strip()
    if not age or not union:
        return success_response(_empty_chart_response())

    return success_response(_compute_chart_data(age, union))


def get_chart_gender_data():
    """Return chart data filtered by gender — replaces getChartAgeGenderData.php / getChartAgeFemaleData.php."""
    age = request.args.get("age", type=int)
    union = request.args.get("union", "").strip()
    gender = request.args.get("gender", "male").strip()
    if not age or not union:
        return success_response(_empty_chart_response())

    return success_response(_compute_chart_data(age, union, gender))


def _compute_chart_data(age: int, union: str, gender: str | None = None):
    """Core chart computation — shared by all 3 chart endpoints."""
    # Get the centre names belonging to this union
    centre_names_sub = (
        db.session.query(Registration.centreName)
        .filter(Registration.myunion == union)
    )
    if gender:
        mobiles_sub = (
            db.session.query(Registration.mobile)
            .filter(Registration.gender == gender, Registration.myunion == union)
        )
        evals = Evaluate.query.filter(
            Evaluate.age == age,
            Evaluate.mobile.in_(mobiles_sub),
        ).all()
    else:
        evals = Evaluate.query.filter(
            Evaluate.age == age,
            Evaluate.centreName.in_(centre_names_sub),
        ).all()

    term_cols = get_term_columns_for_age(age)
    sp1, sp2, sp3, sp4 = get_age_split_points(age)

    response = {}
    for idx, col in enumerate(term_cols, 1):
        scores = [getattr(e, col) for e in evals if getattr(e, col)]
        total = len(scores)
        cats = parse_scores_into_categories(scores, sp1, sp2, sp3, sp4)

        term_data = [
            round(cats[j] / total, 2) if total > 0 else 0 for j in range(5)
        ]
        response[f"t{idx}"] = term_data
        response[f"t{idx}Count"] = total
        for j in range(5):
            response[f"t{idx}A{j+1}"] = cats[j]

    return response


def _empty_chart_response():
    resp = {}
    for i in range(1, 5):
        resp[f"t{i}"] = [0, 0, 0, 0, 0]
        resp[f"t{i}Count"] = 0
        for j in range(1, 6):
            resp[f"t{i}A{j}"] = 0
    return resp
