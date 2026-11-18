"""Aggregate seven product-importance attributes without imputing responses."""
import math
from statistics import mean, median
ATTRIBUTES = ["imp_price", "imp_brand", "imp_format", "imp_taste", "imp_nutrition", "imp_convenience", "imp_sportspecific"]

def analyze(rows):
    if not rows:
        raise ValueError("At least one response is required")
    values = {key: [] for key in ATTRIBUTES}
    missing = dict.fromkeys(ATTRIBUTES, 0)
    invalid = dict.fromkeys(ATTRIBUTES, 0)
    top = dict.fromkeys(ATTRIBUTES, 0)
    complete = tied = 0
    for row in rows:
        if not set(ATTRIBUTES).issubset(row):
            raise ValueError("All seven importance columns are required")
        current = {}
        for key in ATTRIBUTES:
            raw = row[key]
            if raw is None or str(raw).strip() == "":
                missing[key] += 1
                continue
            try:
                value = float(raw)
                if not math.isfinite(value) or not value.is_integer() or not 1 <= value <= 7:
                    raise ValueError("Rating must be an integer from 1 to 7")
            except (ValueError, TypeError):
                invalid[key] += 1
                continue
            value = int(value)
            values[key].append(value)
            current[key] = value
        if len(current) == len(ATTRIBUTES):
            complete += 1
            highest = max(current.values())
            winners = [key for key in ATTRIBUTES if current[key] == highest]
            tied += len(winners) > 1
            for key in winners: top[key] += 1
    summary = []
    distribution = []
    for key in ATTRIBUTES:
        observed = values[key]
        summary.append({"attribute": key, "valid": len(observed), "missing": missing[key],
                        "invalid": invalid[key], "mean": mean(observed) if observed else None,
                        "median": median(observed) if observed else None,
                        "top_choice_count": top[key],
                        "top_choice_percent": 100*top[key]/complete if complete else None})
        for rating in range(1,8):
            distribution.append({"attribute": key, "rating": rating, "count": observed.count(rating)})
    summary.sort(key=lambda row: (row["mean"] is None, -(row["mean"] or 0), row["attribute"]))
    return summary, distribution, {"responses": len(rows), "complete_responses": complete,
                                  "complete_responses_with_tied_top": tied}
