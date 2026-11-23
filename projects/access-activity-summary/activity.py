"""Aggregate access events without retaining identifiers or URLs."""
from collections import Counter
from datetime import datetime

def summarize(rows):
    daily=Counter();hours=Counter();categories=Counter();total=invalid=missing=0
    first=last=None
    for row in rows:
        if not {"Date","Category"}.issubset(row):raise ValueError("Date and Category columns required")
        total+=1
        try:stamp=datetime.strptime(row["Date"],"%m/%d/%Y %H:%M")
        except (ValueError,TypeError):invalid+=1;continue
        label=(row["Category"] or "").strip().lower()
        if not label:missing+=1;label="(missing)"
        daily[stamp.date().isoformat()]+=1;hours[stamp.hour]+=1;categories[label]+=1
        first=stamp if first is None else min(first,stamp)
        last=stamp if last is None else max(last,stamp)
    if not total:raise ValueError("No records")
    return ({"input_rows":total,"accepted_rows":total-invalid,"invalid_dates":invalid,
             "missing_category_among_accepted":missing,"active_days":len(daily),
             "first_timestamp":first.isoformat() if first else None,"last_timestamp":last.isoformat() if last else None},
            [{"date":k,"events":v} for k,v in sorted(daily.items())],
            [{"hour":h,"events":hours[h]} for h in range(24)],
            [{"category":k,"events":v} for k,v in sorted(categories.items(),key=lambda x:(-x[1],x[0]))])
