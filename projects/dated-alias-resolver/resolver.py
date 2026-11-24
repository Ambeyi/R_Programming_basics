"""Resolve exact aliases within inclusive date intervals."""
from datetime import date

def prepare(rows):
    rules=[]
    for row in rows:
        if not {"current","former","start_date","end_date"}.issubset(row):raise ValueError("Invalid mapping schema")
        current,former=row["current"].strip(),row["former"].strip()
        start,end=date.fromisoformat(row["start_date"]),date.fromisoformat(row["end_date"])
        if not current or not former or start>end:raise ValueError("Invalid alias interval")
        rules.append((former,current,start,end))
    return rules

def resolve(name,day,rules):
    name=name.strip();when=date.fromisoformat(day)
    if not name:raise ValueError("Name must be nonblank")
    candidates=sorted({current for former,current,start,end in rules if former==name and start<=when<=end})
    return {"name":name,"date":when.isoformat(),"status":"matched" if len(candidates)==1 else "ambiguous" if candidates else "unmatched",
            "canonical":candidates[0] if len(candidates)==1 else "","candidate_count":len(candidates)}
