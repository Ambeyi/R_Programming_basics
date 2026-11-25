"""Discount dated cash flows measured in years from a common origin."""
import math
from collections import defaultdict

def calculate(rows,rate):
    if not math.isfinite(rate) or rate<=-1:raise ValueError("Rate must be finite and greater than -1")
    details=[];totals=defaultdict(float)
    for row in rows:
        if not {"scenario","year","amount"}.issubset(row):raise ValueError("Missing required columns")
        scenario=row["scenario"].strip();year=float(row["year"]);amount=float(row["amount"])
        if not scenario or not math.isfinite(year) or year<0 or not math.isfinite(amount):raise ValueError("Invalid cash flow")
        try:pv=amount*math.exp(-year*math.log1p(rate))
        except OverflowError:raise ValueError("Discounted value overflow") from None
        if not math.isfinite(pv):raise ValueError("Discounted value must be finite")
        details.append({"scenario":scenario,"year":year,"amount":amount,"rate":rate,"present_value":pv})
        totals[scenario]+=pv
    if not details:raise ValueError("No cash flows")
    if not all(math.isfinite(v) for v in totals.values()):raise ValueError("Total overflow")
    return details,[{"scenario":s,"rate":rate,"present_value":v} for s,v in sorted(totals.items())]
