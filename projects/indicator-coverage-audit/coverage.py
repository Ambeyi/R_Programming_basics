"""Audit long-format indicator data without filling missing observations."""
import math
from collections import defaultdict, Counter
REQUIRED = {"Country Code", "Indicator Code", "Year", "Value"}

def audit(rows):
    groups = defaultdict(set)
    keys = Counter()
    invalid = Counter()
    total = 0
    for row in rows:
        total += 1
        if not REQUIRED.issubset(row):
            raise ValueError("Missing required columns")
        country = (row["Country Code"] or "").strip()
        indicator = (row["Indicator Code"] or "").strip()
        if not country or not indicator:
            invalid["missing_key"] += 1
            continue
        try:
            year = int(row["Year"])
            if not 1 <= year <= 9999: raise ValueError()
        except (ValueError, TypeError):
            invalid["invalid_year"] += 1
            continue
        keys[country, indicator, year] += 1
        groups[country,indicator]  # Retain series with no valid values.
        try:
            value = float(row["Value"])
            if not math.isfinite(value): raise ValueError()
        except (ValueError, TypeError):
            invalid["invalid_value"] += 1
            continue
        groups[country,indicator].add(year)
    if not total: raise ValueError("Input contains no records")
    summaries, gaps = [], []
    yearly = Counter()
    for (country,indicator), years in sorted(groups.items()):
        first, last = (min(years),max(years)) if years else (None,None)
        absent = sorted(set(range(first,last+1))-years) if years else []
        summaries.append({"country":country,"indicator":indicator,"valid_years":len(years),
                          "first_year":first,"last_year":last,"internal_missing_years":len(absent),
                          "coverage_percent":100*len(years)/(last-first+1) if years else None})
        gaps.extend({"country":country,"indicator":indicator,"year":y} for y in absent)
        yearly.update((country,y) for y in years)
    duplicates = [{"country":c,"indicator":i,"year":y,"rows":n}
                  for (c,i,y),n in sorted(keys.items()) if n>1]
    annual = [{"country":c,"year":y,"indicators_with_valid_value":n}
              for (c,y),n in sorted(yearly.items())]
    report = {"input_rows":total,"series":len(groups),"valid_series_years":sum(map(len,groups.values())),
              "duplicate_keys":len(duplicates),"duplicate_rows_beyond_first":sum(d["rows"]-1 for d in duplicates),
              "rejected_rows":sum(invalid.values()),"rejection_reasons":dict(invalid),
              "series_with_internal_gaps":sum(s["internal_missing_years"]>0 for s in summaries)}
    return summaries,gaps,duplicates,annual,report
