"""Validate scenario CSV rows and evaluate each scenario independently."""
import csv
from model import calculate

FIELDS=['scenario','area_m2','irradiation_kwh_m2_year','efficiency','performance_factor','demand_kwh_year']

def load(path):
    rows=[];seen=set()
    with open(path,newline='') as handle:
        reader=csv.DictReader(handle)
        if reader.fieldnames != FIELDS:raise ValueError('Expected columns: '+','.join(FIELDS))
        for row in reader:
            name=row['scenario'].strip()
            if not name or name in seen or None in row:raise ValueError('Scenario names must be unique and nonempty; rows must match columns')
            try:values={k:float(row[k]) for k in FIELDS[1:]}
            except (TypeError,ValueError):raise ValueError('Scenario values must be numeric')
            calculate(**values)
            rows.append(dict(scenario=name,**values));seen.add(name)
    if not rows:raise ValueError('At least one scenario is required')
    return rows

def evaluate(rows):
    return [dict(**row,**calculate(**{k:row[k] for k in FIELDS[1:]})) for row in rows]

def sensitivity(base):
    rows=[]
    for efficiency in [.15,.18,.21]:
        for performance_factor in [.75,.85,.95]:
            values={k:base[k] for k in FIELDS[1:]}
            values.update(efficiency=efficiency,performance_factor=performance_factor)
            rows.append(dict(**values,**calculate(**values)))
    return rows
