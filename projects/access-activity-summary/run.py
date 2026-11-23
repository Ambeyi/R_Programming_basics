import argparse,csv,json
from pathlib import Path
from activity import summarize

def main():
    parser=argparse.ArgumentParser(description="Summarise access activity without exporting identifiers")
    parser.add_argument("input");parser.add_argument("--output",default="output");args=parser.parse_args()
    with open(args.input,newline="",encoding="utf-8-sig") as f:report,daily,hourly,categories=summarize(csv.DictReader(f))
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    for name,rows,fields in [("daily",daily,["date","events"]),("hourly",hourly,["hour","events"]),("categories",categories,["category","events"])]:
        with (out/(name+".csv")).open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    (out/"summary.json").write_text(json.dumps(report,indent=2)+"\n");print(json.dumps(report))
if __name__=="__main__":main()
