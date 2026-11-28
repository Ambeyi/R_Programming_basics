"""Audit CSV left joins using one or more exact key columns."""
import argparse
import csv
import json
from pathlib import Path
from audit import audit


def read_csv(path, keys):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        if len(headers) != len(set(headers)) or not set(keys).issubset(headers):
            raise ValueError('CSV requires unique headers and all key columns')
        rows = list(reader)
        if any(None in row or any(v is None for v in row.values()) for row in rows):
            raise ValueError('CSV row width does not match header')
        return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('left', type=Path)
    parser.add_argument('right', type=Path)
    parser.add_argument('--keys', nargs='+', required=True)
    parser.add_argument('--output', type=Path, default=Path('results/audit.json'))
    args = parser.parse_args()
    result = audit(read_csv(args.left,args.keys), read_csv(args.right,args.keys), args.keys)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__ == '__main__': main()
