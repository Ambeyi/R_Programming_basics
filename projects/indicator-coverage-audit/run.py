import argparse
import csv
import json
from pathlib import Path
from coverage import audit

def main():
    parser=argparse.ArgumentParser(description="Audit indicator coverage by country and year")
    parser.add_argument("input");parser.add_argument("--output",default="output")
    args=parser.parse_args()
    with open(args.input,newline="",encoding="utf-8-sig") as f:
        summaries,gaps,duplicates,annual,report=audit(csv.DictReader(f))
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    tables=[("series",summaries,["country","indicator","valid_years","first_year","last_year","internal_missing_years","coverage_percent"]),
            ("gaps",gaps,["country","indicator","year"]),
            ("duplicates",duplicates,["country","indicator","year","rows"]),
            ("annual",annual,["country","year","indicators_with_valid_value"])]
    for name,rows,fields in tables:
        with (out/(name+".csv")).open("w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    (out/"summary.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report))
if __name__=="__main__":main()
