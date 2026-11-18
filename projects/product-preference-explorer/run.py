import argparse
import csv
import json
from pathlib import Path
from preferences import analyze

def main():
    parser = argparse.ArgumentParser(description="Summarise product importance ratings (1–7).")
    parser.add_argument("input")
    parser.add_argument("--output", default="output")
    args = parser.parse_args()
    with open(args.input, newline="", encoding="utf-8-sig") as handle:
        summary, distribution, audit = analyze(list(csv.DictReader(handle)))
    folder = Path(args.output)
    folder.mkdir(parents=True, exist_ok=True)
    for name, rows in [("attributes",summary),("distribution",distribution)]:
        with (folder/(name+".csv")).open("w",newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    (folder/"audit.json").write_text(json.dumps(audit,indent=2)+"\n")
    print(json.dumps(audit))

if __name__ == "__main__": main()
