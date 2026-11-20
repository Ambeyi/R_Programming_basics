"""Expanding-window evaluation of annual forecasting baselines."""
import csv
import math
from statistics import mean

def load_series(path):
    with open(path,newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        if not {"Year","Birth Number"}.issubset(reader.fieldnames or []):
            raise ValueError("Required columns: Year, Birth Number")
        rows=[]
        for r in reader:
            year=int(r["Year"])
            value=float(r["Birth Number"].replace(",",""))
            if not 1<=year<=9999 or not math.isfinite(value) or value<0:
                raise ValueError("Invalid year or value")
            rows.append((year,value))
    rows.sort()
    if len(rows)<2 or any(b[0]-a[0]!=1 for a,b in zip(rows,rows[1:])):
        raise ValueError("At least two unique consecutive annual observations required")
    return rows

def predict(values):
    if len(values)<2 or not all(math.isfinite(v) for v in values):
        raise ValueError("At least two finite values required")
    n=len(values);xbar=(n-1)/2; ybar=mean(values)
    slope=sum((i-xbar)*(v-ybar) for i,v in enumerate(values))/sum((i-xbar)**2 for i in range(n))
    return {"last_value":values[-1],"drift":values[-1]+(values[-1]-values[0])/(n-1),
            "linear_trend":ybar+slope*(n-xbar)}

def evaluate(series,min_train=4):
    if not isinstance(min_train,int) or min_train<2 or min_train>=len(series):
        raise ValueError("Training window must be at least 2 and leave a test observation")
    if any(b[0]-a[0]!=1 for a,b in zip(series,series[1:])):
        raise ValueError("Series must have consecutive ascending years")
    if not all(math.isfinite(v) for _,v in series):raise ValueError("Nonfinite value")
    folds=[]
    for stop in range(min_train,len(series)):
        year,actual=series[stop]
        for model,estimate in predict([v for _,v in series[:stop]]).items():
            folds.append({"year":year,"training_years":stop,"model":model,"actual":actual,
                          "prediction":estimate,"error":estimate-actual})
    metrics=[]
    for model in predict([v for _,v in series[:min_train]]):
        errors=[r["error"] for r in folds if r["model"]==model]
        metrics.append({"model":model,"folds":len(errors),"mae":mean(abs(e) for e in errors),
                        "rmse":math.sqrt(mean(e*e for e in errors)),"mean_error":mean(errors)})
    return folds,sorted(metrics,key=lambda r:(r["mae"],r["model"]))
