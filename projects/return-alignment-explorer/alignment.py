"""Validate price series and compare returns across identical intervals."""
import csv
import math
from datetime import date
from statistics import mean, stdev, correlation

def load_prices(path):
    prices = {}
    rejected = 0
    rows = 0
    seen = set()
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not {"Date", "Close"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV requires Date and Close columns")
        for row in reader:
            rows += 1
            try:
                day = date.fromisoformat(row["Date"])
            except (ValueError, TypeError):
                rejected += 1
                continue
            if day in seen:
                raise ValueError(f"Duplicate date: {day}")
            seen.add(day)
            try:
                value = float(row["Close"])
                if not math.isfinite(value) or value <= 0:
                    raise ValueError("Nonpositive or nonfinite close")
            except (ValueError, TypeError):
                rejected += 1
                continue
            prices[day] = value
    return prices, {"input_rows": rows, "valid_rows": len(prices), "rejected_rows": rejected}

def align(left, right):
    days = sorted(left.keys() & right.keys())
    if len(days) < 3:
        raise ValueError("At least three common valid dates are required")
    intervals = []
    for start, end in zip(days, days[1:]):
        intervals.append({"start": start.isoformat(), "end": end.isoformat(),
                          "days": (end-start).days,
                          "left_return": math.log(left[end])-math.log(left[start]),
                          "right_return": math.log(right[end])-math.log(right[start])})
    return intervals

def summarize(intervals):
    left = [r["left_return"] for r in intervals]
    right = [r["right_return"] for r in intervals]
    result = {"intervals": len(intervals), "start": intervals[0]["start"],
              "end": intervals[-1]["end"], "min_interval_days": min(r["days"] for r in intervals),
              "max_interval_days": max(r["days"] for r in intervals)}
    for label, values in [("left", left), ("right", right)]:
        result[label] = {"mean_log_return": mean(values), "sample_sd": stdev(values),
                         "negative_intervals": sum(v < 0 for v in values)}
    result["pearson_correlation"] = correlation(left, right) if stdev(left)>0 and stdev(right)>0 else None
    return result
