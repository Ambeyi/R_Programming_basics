"""Summarise grouped numeric scores and pairwise mean differences."""
import argparse,csv,math
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from statistics import mean,median,stdev

def summarize(rows):
    groups=defaultdict(list)
    for row in rows:
        if not {"group","y"}.issubset(row): raise ValueError("Required columns: group, y")
        label=(row["group"] or "").strip()
        if not label: raise ValueError("Group must be nonblank")
        value=float(row["y"])
        if not math.isfinite(value): raise ValueError("Score must be finite")
        groups[label].append(value)
    if not groups: raise ValueError("At least one observation required")
    summary=[]
    for label,values in sorted(groups.items()):
        summary.append({"group":label,"n":len(values),"mean":mean(values),"median":median(values),
                        "sample_sd":stdev(values) if len(values)>1 else None,
                        "minimum":min(values),"maximum":max(values)})
    pairs=[{"group_a":a["group"],"group_b":b["group"],"mean_a_minus_b":a["mean"]-b["mean"]}
           for a,b in combinations(summary,2)]
    return summary,pairs

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input");parser.add_argument("--output",default="output")
    args=parser.parse_args()
    with open(args.input,newline="",encoding="utf-8-sig") as f:summary,pairs=summarize(csv.DictReader(f))
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    for name,rows,fields in [("groups",summary,list(summary[0])),("differences",pairs,["group_a","group_b","mean_a_minus_b"])]:
        with (out/(name+".csv")).open("w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    print(f"Summarised {sum(r['n'] for r in summary)} observations in {len(summary)} groups")
if __name__=="__main__":main()
