"""Term calculator — replaces the duplicated 70-line if/else blocks in register.php & update_evaluation.php."""

from datetime import date
from dateutil.relativedelta import relativedelta


def calculate_term_status(dob: date, evaluation_end: date) -> tuple[int, str]:
    """Calculate age in years and the term status string.

    Returns:
        (age_years, term_status)  e.g. (2, 'term1')
    """
    diff = relativedelta(evaluation_end, dob)
    age_years = diff.years
    months = diff.months

    # Map (age_year, month_quarter) → term string
    term_map = {
        2: {0: "term1", 1: "term2", 2: "term3", 3: "term4"},
        3: {0: "term5", 1: "term6", 2: "term7", 3: "term8"},
    }
    # Age 4+ defaults
    default_quarter_map = {0: "term9", 1: "term10", 2: "term11", 3: "term12"}

    quarter = months // 3  # 0-3 → Q0, 4-6 → Q1, 7-9 → Q2, 10-12 → Q3
    if quarter > 3:
        quarter = 3

    quarter_map = term_map.get(age_years, default_quarter_map)
    term_status = quarter_map.get(quarter, "term9")

    return age_years, term_status


def get_age_split_points(age: int) -> tuple[int, int, int, int]:
    """Return the split-point indices used for bucketing comma-separated scores
    into 5 developmental categories (Physical, Cognitive, Language, Social, Creative).

    Matches the PHP logic in getChartAgeData.php.
    """
    if age == 2:
        return 6, 12, 18, 23
    elif age == 3:
        return 4, 8, 12, 16
    else:  # age 4+
        return 4, 12, 18, 23


def get_term_columns_for_age(age: int) -> list[str]:
    """Return the 4 term column names relevant for a given age."""
    if age == 2:
        return ["term1", "term2", "term3", "term4"]
    elif age == 3:
        return ["term5", "term6", "term7", "term8"]
    else:
        return ["term9", "term10", "term11", "term12"]


def parse_scores_into_categories(
    score_strings: list[str], sp1: int, sp2: int, sp3: int, sp4: int
) -> list[int]:
    """Parse comma-separated score strings and count positive values in each
    of the 5 developmental categories.

    Returns [a1_count, a2_count, a3_count, a4_count, a5_count]
    """
    counts = [0, 0, 0, 0, 0]
    for score_str in score_strings:
        if not score_str:
            continue
        values = score_str.split(",")
        for i, val in enumerate(values):
            try:
                v = int(val.strip())
            except (ValueError, IndexError):
                continue
            if v <= 0:
                continue
            if i <= sp1:
                counts[0] += 1
            elif i < sp2:
                counts[1] += 1
            elif i < sp3:
                counts[2] += 1
            elif i < sp4:
                counts[3] += 1
            else:
                counts[4] += 1
    return counts
