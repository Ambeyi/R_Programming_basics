"""Command-line report generation."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from alignment import load_prices, align, summarize

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left")
    parser.add_argument("right")
    parser.add_argument("--output", default="output")
    args = parser.parse_args()
    left, la = load_prices(args.left)
    right, ra = load_prices(args.right)
    intervals = align(left, right)
    summary = summarize(intervals)
    summary["left_quality"] = la
    summary["right_quality"] = ra
    summary["common_valid_dates"] = len(left.keys() & right.keys())
    summary["left_only_valid_dates"] = len(left.keys() - right.keys())
    summary["right_only_valid_dates"] = len(right.keys() - left.keys())
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output/"summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n")
    with (output/"interval_lengths.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["days", "interval_count"])
        writer.writerows(sorted(Counter(r["days"] for r in intervals).items()))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
