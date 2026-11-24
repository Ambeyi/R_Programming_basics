import argparse,csv,json
from collections import Counter
from pathlib import Path
from resolver import prepare,resolve

def read(path):
    with open(path,newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))

def main():
    parser=argparse.ArgumentParser(description="Resolve names using dated alias mappings")
    parser.add_argument("mappings");parser.add_argument("events");parser.add_argument("--output",default="output")
    args=parser.parse_args();rules=prepare(read(args.mappings));rows=[]
    for event in read(args.events):
        if not {"name","date"}.issubset(event):raise ValueError("Events require name and date")
        rows.append(resolve(event["name"],event["date"],rules))
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    with (out/"resolved.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["name","date","status","canonical","candidate_count"]);w.writeheader();w.writerows(rows)
    counts=Counter(r["status"] for r in rows)
    summary={"mapping_rows":len(rules),"events":len(rows),**{s:counts[s] for s in ["matched","ambiguous","unmatched"]}}
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n");print(json.dumps(summary))
if __name__=="__main__":main()
